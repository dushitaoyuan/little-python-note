"""

token 测试
"""
from web.token import TokenManger, Token, TokenType
import base64

key = b'dushitaoyuan'

token_manager = TokenManger(key=key)
t = Token()
t.type = TokenType.API_TOKEN.value
str_token = token_manager.createToken(t)
print("create token:", str_token)
print("verify token:", token_manager.parseToken(token=str_token))
print("verify token:", token_manager.parseToken(token=str_token, token_type=TokenType.API_TOKEN))

# 测试过期
# import time
#
# t.createTime = int(time.mktime(time.strptime("2020-06-25 00:00:00", "%Y-%m-%d %H:%M:%S")))
# str_token = token_manager.createToken(t)
# print(str_token)
# print(token_manager.parseToken(str_token))
#
#
# t.endTime = int(time.mktime(time.strptime("2020-05-24 00:00:00", "%Y-%m-%d %H:%M:%S")))
# str_token = token_manager.createToken(t)
# print(str_token)
# print(token_manager.parseToken(str_token))


import hashlib

h = hashlib.sha256(b"dushitaoyuan")
d = h.digest()
print(h, type(h), d)

print(str(base64.urlsafe_b64encode(d), encoding='utf-8'))

d = {'code': 1}
print('code' in d)
