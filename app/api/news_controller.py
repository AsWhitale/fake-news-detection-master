from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
import pandas as pd

from app.schemas.news import AnalysisRequestUrl, AnalysisRequestItem, AnalysisRequestFile
from app.services import news_service
from app.services.news_service import NewsService

router = APIRouter(tags=["analyze"])


@router.post("/url")
async def analyze_data_url(request: AnalysisRequestUrl, news_service: NewsService = Depends()):
    return await news_service.analyze_url(request.model, request.url)

    # 执行分析逻辑
    # result = {
    #     "label": '0',
    #     "explanation": '经过模型分析：'
    #                    '文本前后不一致性得分为：80；'
    #                    '平台可行度得分为：80；'
    #                    '话题可行度得分为：40；'
    #                    '综合得分为：70；'
    #                    '所以判断为真'
    # }


@router.post("/item")
async def analyze_data_item(request: AnalysisRequestItem, news_service: NewsService = Depends()):
    return await news_service.analyze_item(request.model, request.form_data)


@router.post("/file")
async def analyze_data_file(model: str, file: UploadFile = File(...), news_service: NewsService = Depends()):
    return news_service.analyze_file(model, file)
