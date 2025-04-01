from typing import Optional, List

from pydantic import BaseModel


# // 请求示例
# {
#   "data_type": "form",
#   "form_data": {
#     "title": "示例新闻",
#     "platform": ["wechat", "weibo"],
#     "publish_time": "2023-07-20 10:00:00"
#   }
# }
class NewsItem(BaseModel):
    publish_time: Optional[str] = None
    platform: Optional[str] = None
    url: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    pic_url: Optional[List[str]] = None
    hashtag: Optional[List[str]] = None


class AnalysisRequestUrl(BaseModel):
    model: str
    url: Optional[str] = None


class AnalysisRequestItem(BaseModel):
    model: str
    form_data: Optional[NewsItem] = None


class AnalysisRequestFile(BaseModel):
    model: str


class NewsAnalysisResult(BaseModel):
    news_id: int
    title: str
    pred_label: str
    pred_prob: float
    analysis_time: float
