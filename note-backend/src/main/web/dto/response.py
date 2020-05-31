from pydantic import BaseModel
from enum import Enum, unique


# 返回结果状态码
@unique
class ResultCode(Enum):
    def __new__(cls, code, msg):
        obj = object.__new__(cls)
        obj._value_ = code
        obj.msg = msg
        return obj

    SUCCESS = (1, "成功")
    FAILED = (0, "失败")
    PARAM_ERROR = (400, "参数异常")
    UNAUTHORIZED = (401, "权限异常")
    NOT_FOUND = (404, "request  not found")
    SERVER_ERROR = (500, "服务异常")
    TOO_MANY_REQUESTS = (429, "请求过于频繁,请稍后访问")
    # 1000+
    BUSINESS_ERROR = (1000, "业务异常")

    @staticmethod
    def code(code):
        for v in ResultCode.__members__.values():
            if v.value == code:
                return v
        return None


# 统一返回结果

"""
data：返回结果
code: 结果码 1成功 其他失败
str: 结果描述,错误描述
ext: 扩展结果
"""


class Result(BaseModel):
    data: BaseModel = None
    code: int = None
    msg: str = None
    ext: BaseModel = None


# 结果构造
class ResultBuilder(object):

    @staticmethod
    def success(data: BaseModel = None, ext: BaseModel = None):
        result = Result()
        result.code = ResultCode.SUCCESS.value
        result.data = data
        result.ext = ext
        return result

    @staticmethod
    def failed(code: int = ResultCode.FAILED.value, msg: str = None, ext: BaseModel = None):
        result = Result()
        result.code = code
        result.msg = msg
        result.ext = ext
        return result
