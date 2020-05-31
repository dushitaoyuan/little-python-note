"""
密码工具
"""
import hashlib
from web.bytes_string_util import *


def passwordEncode(passord: str):
    return to_str(hashlib.sha256(passord.encode(encoding="utf-8")).digest(), StringType.HEX)


def passwordEq(password: str, hash_password: str):
    return hash_password == passwordEncode(password)
