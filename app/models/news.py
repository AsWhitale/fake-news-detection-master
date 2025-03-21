from sqlalchemy import Column, String, DateTime, Text

from app.database import Base


class News(Base):
    __tablename__ = "news_set"
    __table_args__ = {'extend_existing': True}

    news_id = Column(String, primary_key=True, index=True)
    publish_time = Column(DateTime)
    platform = Column(String)
    check_time = Column(DateTime)
    label = Column(String)
    url = Column(String)
    title = Column(String)
    content = Column(Text)
    pic_url = Column(String)
    hashtag = Column(String)
