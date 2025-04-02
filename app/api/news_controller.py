from fastapi import APIRouter, UploadFile, File, Depends, Form

from app.schemas.news import AnalysisRequestUrl, AnalysisRequestItem
from app.schemas.response import success_response
from app.services.history_service import HistoryService
from app.services.news_service import NewsService

router = APIRouter(tags=["analyze"])


@router.post("/url")
async def analyze_data_url(request: AnalysisRequestUrl, news_service: NewsService = Depends(), history_service: HistoryService = Depends()):
    result = await news_service.analyze_url(request.model, request.url)
    await history_service.insert_history(result['items'])
    return success_response(
        data=result,
        message='分析完成',
    )


@router.post("/item")
async def analyze_data_item(request: AnalysisRequestItem, news_service: NewsService = Depends(), history_service: HistoryService = Depends()):
    result = await news_service.analyze_item(request.model, request.form_data)
    await history_service.insert_history(result['items'])
    return success_response(
        data=result,
        message='分析完成',
    )

@router.post("/file")
async def analyze_data_file(model: str = Form(...), file: UploadFile = File(...), news_service: NewsService = Depends(), history_service: HistoryService = Depends()):
    result = await news_service.analyze_file(model, file)
    await history_service.insert_history(result['items'])
    return success_response(
        data=result,
        message='分析完成',
    )
