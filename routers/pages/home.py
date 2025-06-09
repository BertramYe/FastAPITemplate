from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from Helper.LoggerHelper import Logger
from starlette.requests import Request
from ..Templater import templates

# 创建路由
HomeRouter = APIRouter()

# 创建日志记录器
logger = Logger()

# 路由返回 HTML 页面
@HomeRouter.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "name": "World"})
