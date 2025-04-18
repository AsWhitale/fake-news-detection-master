from typing import Annotated

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.history import History
from app.schemas.news import NewsAnalysisResult


class HistoryService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    async def insert_history(self, results: list[NewsAnalysisResult]):
        try:
            group_id = self.db.query(func.max(History.group_id)).scalar()
            if group_id is None:
                group_id = 1
            else:
                group_id = group_id + 1
            for result in results:
                detail_json = result.detail.model_dump_json()
                news_analysis = History(
                    group_id=group_id,
                    news_id=result.news_id,
                    pred_label=result.pred_label,
                    pred_prob=result.pred_prob,
                    detail=detail_json,
                    analysis_time=result.analysis_time
                )
                self.db.add(news_analysis)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    async def group_data(self, grouped_data):
        result = []
        for group_id, count in grouped_data:
            group_records = self.db.query(History).filter(History.group_id == group_id).all()
            result.append({
                "group_id": group_id,
                "count": count,
                "records": [{
                    "news_id": record.news_id + 1,
                    "pred_label": record.pred_label,
                    "pred_prob": record.pred_prob,
                    "detail": record.detail,
                    "analysis_time": record.analysis_time
                } for record in group_records]
            })
        return result

    async def get_histories(self, page: int = 1, page_size: int = 1):
        offset = (page - 1) * page_size
        # 按 group_id 分组并统计每个组的记录数
        grouped_data = self.db.query(History.group_id, func.count(History.id).label('count')).group_by(
            History.group_id).offset(offset).limit(page_size).all()

        return await self.group_data(grouped_data)

    async def get_histories_by_filter(self, page, page_size, filter_condition):
        offset = (page - 1) * page_size
        # 按 group_id 分组并统计每个组的记录数
        query = self.db.query(History)

        # 根据筛选条件添加过滤
        if filter_condition == 'gt_08':
            query = query.filter(History.pred_prob > 0.8)
        elif filter_condition == 'lt_06':
            query = query.filter(History.pred_prob < 0.6)
        elif filter_condition == 'between_06_08':
            query = query.filter(History.pred_prob.between(0.6, 0.8))

        grouped_data = query.with_entities(History.group_id, func.count(History.id).label('count')).group_by(
            History.group_id).offset(offset).limit(page_size).all()

        return await self.group_data(grouped_data)
