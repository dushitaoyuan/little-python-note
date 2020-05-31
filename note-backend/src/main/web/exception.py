from web.dto import ResultCode;

"""
异常集合
"""


# 自定义异常
class CustomException(Exception):
    def __init__(self, code: int = ResultCode.BUSINESS_ERROR.value,
                 msg: str = ResultCode.BUSINESS_ERROR.msg, http_code: int = ResultCode.SERVER_ERROR.value):
        self.code = code
        self.msg = msg
        self.http_code = http_code


# 业务异常
class ServiceException(CustomException):
    def __init__(self, code: int = ResultCode.BUSINESS_ERROR.value,
                 msg: str = ResultCode.BUSINESS_ERROR.msg, http_code: int = ResultCode.SERVER_ERROR.value):
        self.code = code
        self.msg = msg
        self.http_code = http_code


# 授权异常
class AuthException(CustomException):
    def __init__(self, code: int = ResultCode.UNAUTHORIZED.value,
                 msg: str = ResultCode.UNAUTHORIZED.msg, http_code: int = 401):
        self.code = code
        self.msg = msg
        self.http_code = http_code


