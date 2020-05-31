from fastapi import APIRouter
from fastapi.responses import JSONResponse
import typing
from web.dto import *
from web.json_util import JsonUtil


class ResponseWrapperResult(JSONResponse):
    def render(self, content: typing.Any) -> bytes:
        if content is not None:
            if not is_type_result(content):
                content = ResultBuilder.success(data=content)
            content = JsonUtil.toJsonString(content)
        return super().render(content)


def is_type_result(result: typing.Any):
    if type(result) == dict and 'code' in result:
        return True
    elif type(result) == Result:
        return True
    return False


router = APIRouter(default_response_class=ResponseWrapperResult)

from web.api import login
from web.api import note

