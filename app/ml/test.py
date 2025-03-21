import time

import joblib
import pandas as pd
from preprocessing import tokenize

loaded = joblib.load('models/news_classifier.pkl')

def predict_news(text):
    processed = tokenize(text)
    features = loaded['vectorizer'].transform([processed])
    proba = loaded['model'].predict_proba(features)[0]
    return f"真实概率：{proba[0]:.2%}，虚假概率：{proba[1]:.2%}"

def predict_test_news():
    column_names = ['news_id', 'label', 'title']
    df_test = pd.read_excel('../data/20250303153452_790.xls', names=column_names)
    print(f"数据维度：{df_test.shape}\n字段类型：\n{df_test.dtypes}")

    df_test = df_test[df_test['label'] != '尚无定论']

    # 将标签转换为数值
    df_test['label'] = df_test['label'].map({'谣言': 1, '事实': 0})

    df_test['title'] = df_test['title'].fillna('').apply(tokenize)

    X_test = loaded['vectorizer'].transform(df_test['title'])

    df_test['pred_label'] = loaded['model'].predict(X_test)
    df_test['pred_prob'] = loaded['model'].predict_proba(X_test).max(axis=1)

    from sklearn.metrics import classification_report

    if 'label' in df_test.columns:
        print(classification_report(df_test['label'], df_test['pred_label']))
    else:
        print("无真实标签，仅输出预测结果")

# print(predict_news("某地发现神秘病毒已致多人死亡"))  # 示例测试

start_time = time.time()
predict_test_news()
end_time = time.time()
run_time = end_time - start_time
print(f"函数运行时间: {run_time} 秒")