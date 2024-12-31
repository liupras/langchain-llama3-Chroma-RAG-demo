#coding=utf-8
#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : 刘立军
# @time    : 2024-12-26
# @Description: 基于fastapi实现的具有oauth2认证功能的api网关。
# @version : V0.5

from fastapi import Body, Depends, FastAPI, HTTPException,status,Request
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from config.config import config
ACCESS_TOKEN_EXPIRE_MINUTES = config["token"]["expires_time"]

# 创建一个FastAPI实例
app = FastAPI()

# 允许跨域访问
from fastapi.middleware.cors import CORSMiddleware
origins = config["origins"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 打印请求日志，可用于和客户端调试
async def log_request_details(request: Request):
    client_host = request.client.host
    client_port = request.client.port
    method = request.method
    url = request.url
    headers = request.headers
    body = None
    if request.form:    
        body = await request.form()
    elif request.body:
        body = await request.body()

    print(f"Client: {client_host}:{client_port}")
    print(f"Method: {method} URL: {url}")
    print(f"Headers: {headers}")
    print(f"Body: {body if body else 'No Body'}")

'''
用户认证服务
'''
from util.token import create_access_token
from common.user import authenticate_user,Token,User,get_current_active_user

# 登录方法
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),remember: bool|None=Body(None),log_details: None = Depends(log_request_details))-> Token:
    '''
    OAuth2PasswordRequestForm 是用以下几项内容声明表单请求体的类依赖项：

    username
    password
    scope、grant_type、client_id等可选字段。
    '''
    
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或者密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    m = 0
    if remember:
        m = ACCESS_TOKEN_EXPIRE_MINUTES
        
    # 在JWT 规范中，sub 键的值是令牌的主题。
    access_token = create_access_token(data={"sub": user.username},encrypted_text=user.userid, expire_minutes=m)

    # 响应返回的内容应该包含 token_type。本例中用的是BearerToken，因此， Token 类型应为bearer。
    return Token(access_token=access_token, token_type="bearer")


# 获取用户信息
@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    '''
    Depends 在依赖注入系统中处理安全机制。
    此处把 current_user 的类型声明为 Pydantic 的 User 模型，这有助于在函数内部使用代码补全和类型检查。
    get_current_user 依赖项从子依赖项 oauth2_scheme 中接收 str 类型的 toke。
    FastAPI 校验请求中的 Authorization 请求头，核对请求头的值是不是由 Bearer + 令牌组成， 并返回令牌字符串；如果没有找到 Authorization 请求头，或请求头的值不是 Bearer + 令牌。FastAPI 直接返回 401 错误状态码（UNAUTHORIZED）。
    '''
    return current_user

'''
API网关服务
'''

import httpx

time_out = config["time_out"]
services = config["services"]

'''
services的key是服务名称，客户端在请求时传入服务名称，本网关再根据服务名称找到对应的服务地址
'''

# 接收客户端请求并转发到后端服务
@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(service: str, path: str, request: Request,current_user: Annotated[User, Depends(get_current_active_user)]):
    '''
    !注意：网关并未将header转发给后端服务，这样比较简单。
    '''
    
    if service not in services:
        raise HTTPException(status_code=401, detail="未找到该服务")
    
    headers = {"userid":current_user.userid}

    # 从客户端请求中获取数据
    client_request_data = await request.json()
        
    service_url = services[service]
    url = f"{service_url}/{path}"   

    # 使用 httpx 将请求转发到后端服务，非阻塞，不过在我的配置一般的开发机上没有发现和阻塞式调用在性能上有多少区别。
    async with httpx.AsyncClient() as client:
        '''
        !注意：httpx.AsyncClient默认的timeout为5秒，在调用基于大模型的后端服务时经常超时，所以这里设置超时时间为30秒
        '''
        response = await client.post(url=url, json=client_request_data,headers=headers,timeout=time_out)
        #print(response)
        return response.json()

if __name__ == "__main__":
    import uvicorn

    # 交互式API文档地址：
    # http://127.0.0.1:5001/docs/ 
    # http://127.0.0.1:5001/redoc/
    uvicorn.run(app, host="0.0.0.0", port=8000)