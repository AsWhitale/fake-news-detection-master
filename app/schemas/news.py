from datetime import datetime

from pydantic import BaseModel

class NewsItem(BaseModel):
    username: str
    password: str
    news_id :str
    publish_time :datetime
    platform :str
    check_time :datetime
    label :str
    url :str
    title :str
    content :str
    pic_url :str
    hashtag :str

