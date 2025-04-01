import os
from urllib.request import Request

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import user_controller, history_controller
from app.api import news_controller
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

from app.exceptions.base_exceptions import AppException
from app.schemas.response import error_response

app = FastAPI()
# app = FastAPI(docs_url=None, redoc_url=None)



# static_dir = os.path.dirname(os.path.abspath(__file__))
# app.mount("/static", StaticFiles(directory=f"{static_dir}/static"), name="static")
#
# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html():
#     return get_swagger_ui_html(
#         openapi_url=app.openapi_url,
#         title=app.title + " - Swagger UI",
#         oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
#         swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
#         swagger_css_url="/static/swagger-ui/swagger-ui.css",
#     )
#
#
# @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
# async def swagger_ui_redirect():
#     return get_swagger_ui_oauth2_redirect_html()
#
#
# @app.get("/redoc", include_in_schema=False)
# async def redoc_html():
#     return get_redoc_html(
#         openapi_url=app.openapi_url,
#         title=app.title + " - ReDoc",
#         redoc_js_url="/static/redoc/redoc.standalone.js",
#     )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # 精确匹配前端地址
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法（包括OPTIONS）
    allow_headers=["*"],  # 允许所有头部
)

app.include_router(user_controller.router, prefix="/auth")
app.include_router(news_controller.router, prefix="/analyze")
app.include_router(history_controller.router, prefix="/history")


@app.exception_handler(AppException)
async def handle_app_exception(request: Request, exc: AppException):
    return error_response(
        message=exc.message,
        error_code=exc.error_code,
        status_code=exc.status_code,
        details=exc.details
    )

@app.get("/")
async def root():
    return {"message": "系统已启动"}

# # 重写 openapi 方法以指定 OpenAPI 版本
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = {
#         "openapi": "3.0.1",
#         "info": {
#             "title": app.title,
#             "version": "1.0.0"
#         },
#         "paths": {}
#     }
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema
#
# app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000)
