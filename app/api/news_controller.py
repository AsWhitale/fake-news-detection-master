from fastapi import APIRouter, UploadFile, File, Depends, Form
from fastapi.responses import Response

from app.schemas.news import AnalysisUrlRequest, AnalysisItemRequest, DownloadRequest
from app.schemas.response import success_response
from app.services.history_service import HistoryService
from app.services.news_service import NewsService
from app.services.report_service import ReportService

router = APIRouter(tags=["analyze"])


@router.post("/url")
async def analyze_data_url(request: AnalysisUrlRequest, news_service: NewsService = Depends(),
                           history_service: HistoryService = Depends()):
    result = await news_service.analyze_url(request.model, request.url)
    await history_service.insert_history(result['items'])
    return success_response(
        data=result,
        message='分析完成',
    )


@router.post("/item")
async def analyze_data_item(request: AnalysisItemRequest, news_service: NewsService = Depends(),
                            history_service: HistoryService = Depends()):
    result = await news_service.analyze_item(request.model, request.form_data)
    await history_service.insert_history(result['items'])
    return success_response(
        data=result,
        message='分析完成',
    )


@router.post("/file")
async def analyze_data_file(model: str = Form(...), file: UploadFile = File(...), news_service: NewsService = Depends(),
                            history_service: HistoryService = Depends()):
    result = await news_service.analyze_file(model, file)
    await history_service.insert_history(result['items'])
    return success_response(
        data=result,
        message='分析完成',
    )


@router.post("/download")
async def download_pdf(request: DownloadRequest, report_service: ReportService = Depends()):
    pdf_stream = await report_service.get_pdf(request.text_id)
    return Response(
        content=pdf_stream.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=document.pdf"}
    )
