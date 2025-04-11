import joblib
import numpy as np
import pandas as pd
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from app.ml.utils import platform_tokenizer, hashtag_tokenizer


def train_and_save_model_lr_model(data):
    data['platform'] = data['platform'].fillna('unknown')
    data['hashtag'] = data['hashtag'].fillna('')

    # 1. 文本特征（TF-IDF）
    text_vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2))
    X_text = text_vectorizer.fit_transform(data['text'])

    # 2. 平台特征（词袋模型）
    platform_vectorizer = CountVectorizer(
        max_features=100,  # 控制特征维度
        tokenizer=platform_tokenizer,  # 将整个platform字段视为单个token
        token_pattern=None
    )
    X_platform = platform_vectorizer.fit_transform(data['platform'])

    # 3. 话题标签特征（多标签词袋）
    hashtag_vectorizer = CountVectorizer(
        tokenizer=hashtag_tokenizer,  # 按逗号分割标签
        max_features=200,
        binary=True,  # 使用二进制特征（存在性）
        token_pattern=None
    )
    X_hashtag = hashtag_vectorizer.fit_transform(data['hashtag'])

    # 特征矩阵合并
    X = hstack([X_text, X_platform, X_hashtag])

    y = data['label']

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 训练模型
    model = LogisticRegression(
        class_weight='balanced',  # 处理数据不平衡问题
        max_iter=1000,  # 确保模型收敛
        solver='saga',  # 支持弹性网络正则化
        penalty='elasticnet',  # 组合L1/L2正则化
        l1_ratio=0.5,  # 平衡正则化强度
        C=0.1  # 更强的正则化
    )
    model.fit(X_train, y_train)

    # 评估模型
    print("训练集准确率:", model.score(X_train, y_train))
    print("测试集准确率:", model.score(X_test, y_test))
    print(classification_report(y_test, model.predict(X_test)))
    # accuracy = model.score(X_test, y_test)
    # print(f"模型准确率: {accuracy}")

    # 保存模型和向量器
    # joblib.dump(model, 'models/news_classifier_model.joblib')
    # joblib.dump(vectorizer, 'models/tfidf_vectorizer.joblib')
    joblib.dump({
        'model': model,
        'text_vectorizer': text_vectorizer,
        'platform_vectorizer': platform_vectorizer,
        'hashtag_vectorizer': hashtag_vectorizer,
        'feature_names': np.concatenate([  # 保存完整特征名称列表
            text_vectorizer.get_feature_names_out(),
            platform_vectorizer.get_feature_names_out(),
            hashtag_vectorizer.get_feature_names_out()
        ])
    }, 'models/news_classifier.pkl')


def train_and_save_model_rf_model(data):
    pass


if __name__ == '__main__':
    preprocessed_data = pd.read_csv('../data/preprocessed_news_data.csv')
    train_and_save_model_lr_model(preprocessed_data)
