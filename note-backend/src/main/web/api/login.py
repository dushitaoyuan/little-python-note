from web.routers import router
from web.dto import *
from web.exception import *
from config import GLOBAL_CONFIG
from fastapi import Response, Cookie
from web.token import Token, global_token_manger, TokenType
from web.password_util import *

tokenManger = global_token_manger


@router.post("/login")
def login(login_form: LoginForm, response: Response):
    # 口令登录
    if login_form.loginType == 1:
        if login_form.username != GLOBAL_CONFIG.get("username") or not passwordEq(GLOBAL_CONFIG.get("password"),
                                                                                  login_form.password):
            raise ServiceException(msg="账户密码不匹配")
        token = Token()
        token.type = TokenType.API_TOKEN.value
        token.username = login_form.username
        common_token = tokenManger.createToken(token)
        token.endTime += tokenManger.expire
        token.type = TokenType.REFRESH.value
        refresh_token = tokenManger.createToken(token)
        result = {"username": login_form.username, "api_token": common_token, "expire": tokenManger.expire,
                  "refresh_token": refresh_token}
        # 一周免登录
        if login_form.remember:
            token.type = TokenType.REMEMBER_ME.value
            remember_me_time = int(GLOBAL_CONFIG.get("remember_me_min")) * 60
            token.endTime = token.createTime + remember_me_time
            result['remember_me_token'] = tokenManger.createToken(token)
            result['remember_me_expire'] = remember_me_time
            response.set_cookie(key="remember_me_token", value=result['remember_me_token'],
                                max_age=remember_me_time,
                                expires=remember_me_time)
        return result
    # remember_me登录
    if login_form.loginType == 2:
        remember_me_token = login_form.remember_me_token
        print(remember_me_token)
        if remember_me_token is None:
            raise ServiceException(msg="登录操作非法")
        token_dict = tokenManger.parseToken(remember_me_token, token_type=TokenType.REMEMBER_ME)
        if token_dict['username'] != GLOBAL_CONFIG.get("username"):
            raise ServiceException(msg="登录操作非法")
        token = Token()
        token.type = TokenType.API_TOKEN.value
        token.username = token_dict['username']
        common_token = tokenManger.createToken(token)
        token.endTime += tokenManger.expire
        token.type = TokenType.REFRESH.value
        refresh_token = tokenManger.createToken(token)
        result = {"api_token": common_token, "expire": tokenManger.expire, "refresh_token": refresh_token}
        return result


@router.post("/token/refresh")
def login(refreshToken: str):
    if refreshToken is None:
        raise ServiceException(msg="操作非法")
    token_dict = tokenManger.parseToken(refreshToken, token_type=TokenType.REFRESH)
    if token_dict['username'] != GLOBAL_CONFIG.get("username"):
        raise ServiceException(msg="操作非法")
    token = Token()
    token.type = TokenType.API_TOKEN.value
    token.username = token_dict['username']
    common_token = tokenManger.createToken(token)
    token.endTime += tokenManger.expire
    token.type = TokenType.REFRESH.value
    refresh_token = tokenManger.createToken(token)
    result = {"api_token": common_token, "expire": tokenManger.expire, "refresh_token": refresh_token}
    return result


@router.get("/logout")
def login_out():
    response = Response()
    response.set_cookie(key="remember_me_token", value="",
                        max_age=0,
                        expires=0)
    return response
