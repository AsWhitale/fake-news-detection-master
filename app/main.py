import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth
from app.api import news

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # 精确匹配前端地址
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法（包括OPTIONS）
    allow_headers=["*"],  # 允许所有头部
)

app.include_router(auth.router, prefix="/api")
app.include_router(news.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "系统已启动"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000)
