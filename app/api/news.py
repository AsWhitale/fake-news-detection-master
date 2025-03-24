from fastapi import APIRouter, Depends

from app.schemas.news import NewsItem
from app.services.news_service import NewsService

router = APIRouter(prefix="/news", tags=["news"])


@router.get("/processed", response_model=list[NewsItem])
async def get_processed_news(
        limit: int = 100,
        service: NewsService = Depends(lambda db: NewsService(db))
):
    """获取预处理后的新闻数据"""
    processed_df = service.get_processed_articles(limit)
    return service.DataPreprocessor.df_to_dict_list(processed_df)
