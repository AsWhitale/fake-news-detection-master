import pandas as pd
from fastapi import UploadFile, HTTPException

from app.exceptions.base_exceptions import AppException
from app.schemas.news import NewsItem
from app.utils.model_analyzer import analyze_news
from app.utils.preprocessing import preprocess


class NewsService:
    async def easy_analyze(self,model:str, df: pd.DataFrame):
        # 预处理
        df = preprocess(df)
        # 分析
        return await analyze_news(model, df)

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
        # 文件处理逻辑
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        elif file.filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file.file)
        else:
            raise AppException(
                error_code="ERROR_INVALID_PARAMETER",
                message="格式错误",
                details={"filename": file.filename}
            )

        # 保存到临时文件或数据库
        temp_path = f"/tmp/{file.filename}"
        df.to_parquet(temp_path)

        return await self.easy_analyze(model, df)
