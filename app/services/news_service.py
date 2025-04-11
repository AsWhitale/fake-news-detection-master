import tempfile
from typing import Annotated

import tempfile
from typing import Annotated

import pandas as pd
from fastapi import UploadFile, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions.base_exceptions import AppException
from app.schemas.news import NewsItem
from app.utils.model_analyzer import analyze_news
from app.utils.preprocessing import preprocess


class NewsService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    async def easy_analyze(self, model: str, df: pd.DataFrame):
        # 预处理
        df = preprocess(df)
        # 分析
        result = await analyze_news(model, df)
        return result

    async def analyze_url(self, model: str, url: str):
        columns = list(NewsItem.model_fields.keys())  # 自动获取所有字段
        df = pd.DataFrame(
            NewsItem(url=url).model_dump(),
            columns=columns,
            index=[0]
        )
        return await self.easy_analyze(model, df)

    async def analyze_item(self, model: str, item: NewsItem):
        # 组装数据
        columns = list(NewsItem.model_fields.keys())  # 自动获取所有字段
        df = pd.DataFrame(
            item.model_dump(),
            columns=columns,
            index=[0]
        )
        return await self.easy_analyze(model, df)

    async def analyze_file(self, model: str, file: UploadFile):
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(file.file.read())
                tmp_path = tmp.name

            # 在这里进行你的分析逻辑
            if file.filename.endswith(".csv"):
                df = pd.read_csv(tmp_path)
            elif file.filename.endswith((".xls", ".xlsx")):
                df = pd.read_excel(tmp_path)
            else:
                raise AppException(
                    error_code="ERROR_INVALID_PARAMETER",
                    message="格式错误",
                    details={"filename": file.filename}
                )
            return await self.easy_analyze(model, df)
        finally:
            # 清理临时文件
            import os
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
