from pydantic import BaseModel


# 登录表单

class LoginForm(BaseModel):
    username: str = None
    password: str = None
    remember: bool = False
    loginType: int = 1
    remember_me_token: str = None
