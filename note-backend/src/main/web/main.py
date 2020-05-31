from web.app import app
from web.routers import router
from log import LOG
from fastapi import Request
from .exception import *
from web.token import global_token_manger, TokenType

tokenManger = global_token_manger

from fastapi.middleware.cors import CORSMiddleware

"""
cd src/main uvicorn web.main:app --reload --port 8080
"""


def deploy_app():
    app.include_router(router, prefix="/api")
    cors_handler()
    LOG.info("deploy success")



"""

请求鉴权
"""
public_url_list = ['/login', '/logout', '/token/refresh']

@app.middleware("http")
async def tokenInterceptor(request: Request, call_next):
    if is_permit(request):
        return await call_next(request)
    token = request.headers.get("token")
    print(token)
    if token is not None and tokenManger.parseToken(token=token, token_type=TokenType.API_TOKEN):
        return await call_next(request)
    else:
        raise AuthException("请登录")


def is_permit(request: Request):
    request_url = request.url.path
    for public_url in public_url_list:
        if request_url.find(public_url) > 0:
            return True
    return False


"""
跨域处理

"""
cros_origins = [
    "https://*.taoyuanx.com",
    "http://*.taoyuanx.com",
    "http://localhost:8081"
]


def cors_handler():
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cros_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


deploy_app()