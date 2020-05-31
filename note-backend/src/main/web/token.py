import hmac
import json

import time
from web.exception import AuthException
from web.bytes_string_util import *

from enum import Enum, unique

from config import GLOBAL_CONFIG

"""
token 类型定义 

"""


@unique
class TokenType(Enum):
    def __new__(cls, code, desc):
        obj = object.__new__(cls)
        obj._value_ = code
        obj.desc = desc
        return obj

    API_TOKEN = (0, "api_token")
    REFRESH = (1, "refresh_token")
    REMEMBER_ME = (2, "remember_me_token")

    @staticmethod
    def type(code):
        for v in TokenType.__members__.values():
            if v.value == code:
                return v
        return None


class Token(object):
    createTime: int = None
    endTime: int = None
    username: str = None
    type: int = None


"""
token 生成 

"""


class TokenManger(object):
    def __init__(self, key: bytes, encoding: str = "utf-8", digestmod: str = "SHA256", expire: int = 30 * 60,
                 str_type: StringType = StringType.BASE64_URL_SAFE):
        self.key = key
        self.encoding = encoding
        self.digestmod = digestmod
        self.expire = expire
        self.str_type = str_type

    def createToken(self, token: Token):
        if token.createTime is None:
            token.createTime = int(time.time())
        if token.endTime is None:
            token.endTime = token.createTime + self.expire
        bytes_data = json.dumps(token.__dict__).encode()
        bytes_sign = hmac.new(self.key, bytes_data, digestmod=self.digestmod).digest()
        return "{}.{}".format(to_str(bytes_data, self.str_type),
                              to_str(bytes_sign, self.str_type))

    def parseToken(self, token: str, token_type: TokenType = None):
        s = token.split(".")
        if len(s) != 2:
            raise AuthException(msg="token格式异常")
        bytes_data = to_bytes(s[0], self.str_type)
        bytes_sign = to_bytes(s[1], self.str_type)
        calc_sign = hmac.new(self.key, bytes_data, digestmod=self.digestmod).digest()

        if calc_sign != bytes_sign:
            raise AuthException(msg="token验证异常")
        token_dict = json.loads(str(bytes_data, encoding=self.encoding))
        now = int(time.time())
        if token_dict['createTime'] is not None and token_dict['createTime'] > now:
            raise AuthException(msg="token未生效")
        if token_dict['endTime'] < now:
            raise AuthException(msg="token已过期")
        if token_type is not None and 'type' in token_dict and token_dict['type'] != token_type.value:
            raise AuthException(msg="token类型非法")
        return token_dict


global_token_manger = TokenManger(key=GLOBAL_CONFIG.get("token_sign_key").encode(encoding='utf-8'))
