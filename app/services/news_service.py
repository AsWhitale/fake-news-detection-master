import pandas as pd
from fastapi import UploadFile, HTTPException


class NewsService:
    async def analyze_url(self, db, model: str, url: str):
        pass

    async def analyze_item(self, db, url: str):
        pass

    async def analyze_file(self, model:str , file: UploadFile):
        # 文件处理逻辑
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        elif file.filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file.file)
        else:
            raise HTTPException(400, "不支持的格式")

        # 保存到临时文件或数据库
        temp_path = f"/tmp/{file.filename}"
        df.to_parquet(temp_path)

        # 执行分析逻辑
        result = {
            "label": '0',
            "explanation": '经过模型分析：'
                           '文本前后不一致性得分为：80；'
                           '平台可行度得分为：80；'
                           '话题可行度得分为：40；'
                           '综合得分为：70；'
                           '所以判断为真'
        }
        return {"message": "成功", "result": result}
