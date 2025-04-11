from typing import Optional, List

from pydantic import BaseModel


class NewsItem(BaseModel):
    publish_time: Optional[str] = None
    platform: Optional[str] = None
    url: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    pic_url: Optional[List[str]] = None
    hashtag: Optional[List[str]] = None


class NewsAnalysisDetail(BaseModel):
    explanation: str
    marked_text: str
    fake_ratio: float  # 应该为浮点数类型
    fake_distribution: list[float]  #虚假内容分布
    keywords: list[str]  # 应该为字符串列表
    contributions: str


class NewsAnalysisResult(BaseModel):
    news_id: int
    pred_label: str
    pred_prob: float
    detail: NewsAnalysisDetail
    analysis_time: float


class AnalysisUrlRequest(BaseModel):
    model: str
    url: Optional[str] = None


class AnalysisItemRequest(BaseModel):
    model: str
    form_data: Optional[NewsItem] = None


class AnalysisFileRequest(BaseModel):
    model: str


class DownloadRequest(BaseModel):
    text_id: int
