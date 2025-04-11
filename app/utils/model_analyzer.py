import os
import re
import time

import joblib
import pandas as pd
from scipy.sparse import hstack

from app.schemas.news import NewsAnalysisResult, NewsAnalysisDetail

script_dir = os.path.dirname(os.path.abspath(__file__))
# 构建模型文件的绝对路径
model_path = os.path.join(script_dir, '..', 'ml', 'models', 'news_classifier.pkl')
loaded_lr = joblib.load(model_path)


async def analyze_news(model: str, df_news: pd.DataFrame, page: int = 1, page_size: int = 10):
    if model not in ['lr_model', 'rf_model', 'bert_model']:
        raise ValueError(f"Invalid model: {model}")

    if model == 'lr_model' or model == 'rf_model' or model == 'bert_model':
        current_pkl = loaded_lr

    start_time = time.time()

    # ------------ 数据预处理 ------------
    df_news = df_news.copy()
    # 填充缺失值
    df_news['platform'] = df_news['platform'].fillna('unknown')
    df_news['hashtag'] = df_news['hashtag'].fillna('')
    # 保留原始文本
    df_news = df_news.copy()
    if 'title' in df_news.columns and 'content' in df_news.columns:
        df_news['original_text'] = df_news['title'].fillna('').astype(str) + " " + df_news['content'].fillna('').astype(
            str)
    elif 'title' in df_news.columns:
        df_news['original_text'] = df_news['title'].fillna('').astype(str)
    elif 'content' in df_news.columns:
        df_news['original_text'] = df_news['content'].fillna('').astype(str)
    else:
        df_news['original_text'] = ''

    # ------------ 加载LR模型和特征处理器 ------------
    model = current_pkl['model']
    text_vectorizer = current_pkl['text_vectorizer']
    platform_vectorizer = current_pkl['platform_vectorizer']
    hashtag_vectorizer = current_pkl['hashtag_vectorizer']
    feature_names = current_pkl['feature_names']

    # ------------ 特征工程 ------------
    X_text = text_vectorizer.transform(df_news['text'])
    X_platform = platform_vectorizer.transform(df_news['platform'])
    X_hashtag = hashtag_vectorizer.transform(df_news['hashtag'])
    X_test = hstack([X_text, X_platform, X_hashtag]).tocsr()

    # ------------ 模型预测 ------------
    df_news['pred_label'] = ["事实" if p == 0 else "谣言" for p in model.predict(X_test)]
    df_news['pred_prob'] = model.predict_proba(X_test).max(axis=1)
    df_news['news_id'] = range(len(df_news))

    process_time = time.time() - start_time

    # ------------ 特征贡献计算（LR专用）------------
    coef = model.coef_[0]  # 直接使用LR模型的系数

    def get_feature_contributions(row_index):
        row = X_test[row_index]
        contributions = []
        for idx, value in zip(row.indices, row.data):
            contribution = value * coef[idx]
            if contribution > 0:
                contributions.append({
                    "feature": feature_names[idx],
                    "value": float(value),
                    "weight": float(coef[idx]),
                    "contribution": float(contribution)
                })
        return sorted(contributions, key=lambda x: abs(x["contribution"]), reverse=True)[:15]

    def get_fake_keywords(row_index):
        """获取对虚假预测有贡献的正向特征词"""
        contributions = get_feature_contributions(row_index)
        return [
            feat
            for feat in contributions
            if feat["contribution"] > 0 and feat["feature"] != ''  # 只取正向贡献的特征
        ] or []

    def mark_fake_content(text, keywords):
        """标记虚假关键词并计算占比"""
        marked_text = text
        total_chars = len(text)
        fake_chars = 0
        fake_indices = set()

        # 按贡献度排序后从长到短匹配，避免短词优先匹配的问题
        for keyword in sorted(keywords, key=len, reverse=True):
            # 处理n-gram特征（如"疫情_爆发"转为"疫情 爆发"）
            search_term = keyword["feature"].replace("_", " ")

            # 统计原始文本中的匹配次数
            matches = list(re.finditer(re.escape(search_term), text))
            if not matches:
                continue

            # 累加匹配字符数（按原始文本长度计算）
            fake_chars += sum(len(m.group()) for m in matches)

            # 记录所有匹配的字符索引
            for m in matches:
                start, end = m.span()
                for i in range(start, end):
                    fake_indices.add(i)

            # 添加标记（避免重复标记）
            marked_text = re.sub(
                re.escape(search_term),
                lambda m: f"<fake>{m.group()}</fake>" if not m.group().startswith("<fake>") else m.group(),
                marked_text
            )

        # 计算虚假内容占比（基于原始文本长度）
        fake_ratio = (fake_chars / total_chars * 100) if total_chars > 0 else 0.0

        # 生成段落比例数组
        ratios = []
        if total_chars == 0:
            return marked_text, fake_ratio, ratios

        # 分割段落（真实/虚假交替）
        paragraphs = []
        current_is_fake = 0 in fake_indices  # 第一个字符是否为虚假
        current_length = 1

        for i in range(1, len(text)):
            char_is_fake = i in fake_indices
            if char_is_fake == current_is_fake:
                current_length += 1
            else:
                paragraphs.append((current_is_fake, current_length))
                current_is_fake = char_is_fake
                current_length = 1
        paragraphs.append((current_is_fake, current_length))

        # 如果第一个段落是虚假，插入长度为0的真实段落
        if paragraphs and paragraphs[0][0]:
            paragraphs.insert(0, (False, 0))

        # 计算各段落占比
        for is_fake, length in paragraphs:
            ratio = length / total_chars
            ratios.append(round(ratio, 2))

        return marked_text, fake_ratio, ratios

    # ------------ 分页处理 ------------
    total = len(df_news)
    start = max(0, (page - 1) * page_size)
    end = min(start + page_size, total)
    page_data = df_news.iloc[start:end]

    # ------------ 生成结果 ------------
    results = []
    for idx, row in page_data.iterrows():
        if row['pred_label'] == "谣言":
            # 获取正向贡献的关键词
            keywords = get_fake_keywords(idx)

            # 标记虚假内容并计算占比
            marked_text, fake_ratio, fake_distribution = mark_fake_content(
                row['original_text'],
                keywords
            )
            explanation = "关键谣言特征：" + "，".join(
                [f"{k['feature']}(贡献值+{k['contribution']:.2f})" for k in keywords]
            )
        else:
            marked_text = row['original_text']
            fake_ratio = 0.0
            fake_distribution = [0.0]
            explanation = "未检测到谣言特征"

        contributions = get_feature_contributions(idx)

        result = NewsAnalysisResult(
            news_id=row['news_id'],
            pred_label=row['pred_label'],
            pred_prob=round(row['pred_prob'], 4),
            detail=NewsAnalysisDetail(  # 使用嵌套模型
                explanation=explanation,
                marked_text=marked_text,
                fake_ratio=fake_ratio,  # float类型
                fake_distribution=fake_distribution,
                keywords=[k["feature"] for k in keywords] if row['pred_label'] == "谣言" else [],  # list[str]类型
                contributions=str(contributions)
            ),
            analysis_time=process_time
        )
        results.append(result)

    return {
        "items": results,
        "pagination": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    }

    # except FileNotFoundError as e:
    #     raise FileNotFoundError("Model file not found") from e
    #
    # except Exception as e:
    #     raise Exception("Analysis failed") from e


if __name__ == "__main__":
    print(analyze_news(
        model='lr_model',
        df_news=pd.read_excel('../data/simple_test.xlsx')
    ))
