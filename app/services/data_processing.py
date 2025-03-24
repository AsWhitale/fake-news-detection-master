# from sqlalchemy.orm import Session
# import pandas as pd
# from app.models.news import News
# from app.utils.preprocessing import DataPreprocessor
#
#
# class DataService:
#     def __init__(self, db: Session):
#         self.db = db
#
#     def get_raw_articles(self, limit: int = 1000) -> pd.DataFrame:
#         """从数据库获取原始数据"""
#         query = self.db.query(
#             News.news_id,
#             News.publish_time,
#             News.platform,
#             News.check_time,
#             News.label,
#             News.url,
#             News.title,
#             News.content,
#             News.pic_url,
#             News.hashtag
#         ).limit(limit)
#
#         return pd.read_sql(query.statement, self.db.bind)
#
#     def get_processed_articles(self, limit: int = 1000) -> pd.DataFrame:
#         """获取预处理后的数据"""
#         raw_df = self.get_raw_articles(limit)
#         return DataPreprocessor.clean_data(raw_df)
#
#     def save_processed_data(self, df: pd.DataFrame):
#         """保存处理后的数据到数据库"""
#         for _, row in df.iterrows():
#             self.db.query(News).filter(
#                 News.news_id == row['id']
#             ).update({
#                 'processed_content': row['processed_content'],
#                 'category': row['category'],
#                 'author': row['author']
#             })
#         self.db.commit()