"""

字符与字节 相关转换


"""
from enum import Enum, unique
import base64


@unique
class StringType(Enum):
    BASE64 = 1
    BASE64_URL_SAFE = 2
    HEX = 3


encoding = 'utf-8'


def to_bytes(s: str, str_type: StringType = StringType.BASE64_URL_SAFE):
    if str_type == StringType.HEX:
        return bytes.fromhex(s)
    if str_type == StringType.BASE64:
        return base64.decodebytes(s.encode(encoding))
    if str_type == StringType.BASE64_URL_SAFE:
        return base64.urlsafe_b64decode(s.encode(encoding))
    raise Exception(msg="{} stringType not support".format(str_type.value))


def to_str(byte: bytes, str_type: StringType = StringType.BASE64_URL_SAFE):
    if str_type == StringType.BASE64:
        return str(base64.encodebytes(byte), encoding=encoding)
    if str_type == StringType.BASE64_URL_SAFE:
        return str(base64.urlsafe_b64encode(byte), encoding=encoding)
    if str_type == StringType.HEX:
        return byte.hex()
    raise Exception(msg="{} stringType not support".format(str_type.value))
