from fastapi import APIRouter, Depends

from app.schemas.history import HistoryQuery, HistoryQueryFilter
from app.schemas.response import success_response
from app.services.history_service import HistoryService

router = APIRouter(tags=["history"])


@router.post("/get")
async def get_history(request: HistoryQuery, history_service: HistoryService = Depends(HistoryService)):
    return success_response(
        data=await history_service.get_histories(request.page, request.page_size)
    )


@router.post("/filter")
async def get_history_by_filter(request: HistoryQueryFilter, history_service: HistoryService = Depends()):
    return success_response(
        data=await history_service.get_histories_by_filter(request.page, request.page_size, request.filter)
    )
