from fastapi import APIRouter, Depends, Query

from app.schemas.history import HistoryQuery
from app.schemas.news import AnalysisRequestUrl
from app.schemas.response import success_response
from app.services.history_service import HistoryService

router = APIRouter(tags=["history"])


@router.post("/get")
async def history(request: HistoryQuery, history_service: HistoryService = Depends(HistoryService)):
    return success_response(
        data=history_service.get_histories(request.page, request.page_size)
    )
