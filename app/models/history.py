from sqlalchemy import Column, String, DateTime, Text, Float, Integer

from app.database import Base


class History(Base):
    __tablename__ = "history"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer)
    news_id = Column(Integer)
    pred_label = Column(String)
    pred_prob = Column(Float)
    detail = Column(String)
    analysis_time = Column(Float)