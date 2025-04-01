import re

import jieba
import pandas as pd

from app.utils.crawler import get_web_text


# 对标题和内容进行分词
def tokenize(text):
    # 去除特殊字符和数字
    text = re.sub(r'[^\u4e00-\u9fa5]', '', text)
    return " ".join(jieba.lcut(text))


# 训练时对列进行特征处理
def train_preprocess_column(data):
    data = data[data['label'] != '尚无定论'].copy()

    # 将标签转换为数值
    data['label'] = data['label'].map({'谣言': 1, '事实': 0})

    return preprocess_column(data)


# 训练时对列进行特征处理
def preprocess_column(data):
    data['title'] = data['title'].fillna('').apply(tokenize)
    data['content'] = data['content'].fillna('').apply(tokenize)

    # 合并标题和内容
    data['text'] = data['title'].fillna('').astype(str) + " " + data['content'].fillna('').astype(str)

    return data


# 通过url获取数据
def preprocess_url(data):
    data = data.copy()

    for index, row in data.iterrows():
        url = row['url']

        if pd.isna(url) or not url.strip():
            continue
        else:
            data.at[index, 'content'] = get_web_text(url)

    return data


# 训练时预处理
def train_preprocess(data):
    data = preprocess_url(data)
    data = train_preprocess_column(data)
    return data


# 应用时预处理
def preprocess(data):
    data = preprocess_url(data)
    data = preprocess_column(data)
    return data


# 示例使用
if __name__ == '__main__':
    file_path = '../data/train_data.csv'  # 替换为实际的数据文件路径
    data = pd.read_csv(file_path)
    preprocessed_data = train_preprocess(data)
    preprocessed_data.to_csv('../data/preprocessed_news_data.csv', index=False)
