from fastapi import APIRouter

from app.schemas.news import AnalysisRequestUrl

router = APIRouter(tags=["history"])


@router.post("/get")
async def history(request: AnalysisRequestUrl):
    pass
