from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib


def train_and_save_model(data):

    # 提取特征
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
    X = vectorizer.fit_transform(data['text'])
    y = data['label']

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 训练模型
    model = LogisticRegression(
        class_weight='balanced',  # 处理数据不平衡问题
        max_iter=1000,  # 确保模型收敛
        solver='liblinear'  # 适合小数据集
    )
    model.fit(X_train, y_train)

    # 评估模型
    print("训练集准确率:", model.score(X_train, y_train))
    print("测试集准确率:", model.score(X_test, y_test))
    print(classification_report(y_test, model.predict(X_test)))
    # accuracy = model.score(X_test, y_test)
    # print(f"模型准确率: {accuracy}")

    # 保存模型和向量器
    joblib.dump(model, 'models/news_classifier_model.joblib')
    joblib.dump(vectorizer, 'models/tfidf_vectorizer.joblib')
    joblib.dump({
        'model': model,
        'vectorizer': vectorizer
    }, 'models/news_classifier.pkl')


preprocessed_data = pd.read_csv('../data/preprocessed_news_data.csv')
train_and_save_model(preprocessed_data)