import os
import time

import joblib
import pandas as pd

from app.schemas.news import NewsAnalysisResult
from app.schemas.response import error_response

script_dir = os.path.dirname(os.path.abspath(__file__))
# 构建模型文件的绝对路径
model_path = os.path.join(script_dir, '..', 'ml', 'models', 'news_classifier.pkl')
loaded = joblib.load(model_path)


async def analyze_news(model: str, df_news: pd.DataFrame, page: int = 1, page_size: int = 10):
    # try:
    if model not in ['lr_model']:
        raise ValueError(f"Invalid model: {model}")

    if model == 'lr_model':
        current_pkl = loaded

    start_time = time.time()
    X_test = current_pkl['vectorizer'].transform(df_news['text'])
    predictions = current_pkl['model'].predict(X_test)
    df_news['pred_label'] = ["事实" if pred == 0 else "谣言" for pred in predictions]
    df_news['pred_prob'] = current_pkl['model'].predict_proba(X_test).max(axis=1)
    process_time = time.time() - start_time

    df_news['news_id'] = range(len(df_news))

    # 分页计算
    total = len(df_news)
    start = (page - 1) * page_size
    end = start + page_size
    page_data = df_news.iloc[start:end]

    results = [
        NewsAnalysisResult(
            news_id=row['news_id'],
            pred_label=row['pred_label'],
            pred_prob=round(row['pred_prob'], 4),
            analysis_time=round(process_time, 4)
        ) for _, row in page_data.iterrows()
    ]

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
