from fastapi import (
    FastAPI, Request, HTTPException
)
from fastapi.responses import JSONResponse
from web.json_util import JsonUtil
from log import LOG
from web.dto import *
from web.exception import *

app = FastAPI()


@app.exception_handler(Exception)
async def exception_handler(request: Request, exception: Exception):
    if isinstance(exception, CustomException):
        _result = ResultBuilder.failed(code=exception.code, msg=exception.msg)
        LOG.debug("CustomException exception:{}", _result)
        return JSONResponse(
            status_code=exception.http_code,
            content=JsonUtil.toJsonString(_result)
        )
    elif isinstance(exception, HTTPException):
        LOG.warning("http exception:{}", exception)
        return JSONResponse(
            status_code=exception.status_code,
            content=exception.detail,
            headers=exception.headers
        )
    else:
        LOG.error("系统异常:{}", exception)
        _result = ResultBuilder.failed(code=ResultCode.SERVER_ERROR.value, msg=ResultCode.SERVER_ERROR.msg)
        return JSONResponse(
            status_code=500,
            content=JsonUtil.toJsonString(_result)
        )
