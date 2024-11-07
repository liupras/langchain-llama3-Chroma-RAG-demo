#coding=utf-8
#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : 刘立军
# @time    : 2024-11-07
# @Description: 使用fastapi-gateway实现简单的应用网关
# @version : V0.5

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests

# 创建一个FastAPI实例
app = FastAPI()

# 定义服务
'''
services的key是服务名称，客户端在请求时传入服务名称，本网关再根据服务名称找到对应的服务地址
'''
services = {
    "translation": "http://127.0.0.1:5001",
    # 可以在这里添加其它服务地址
}


# 接收客户端请求并转发到后端服务
'''
!注意：网关并未将header转发给后端服务，这样比较简单。
'''
@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(service: str, path: str, request: Request):
    if service not in services:
        return JSONResponse(status_code=404, content="未找到该服务！")

    #  根据服务名称找到对应的服务地址
    service_url = services[service]
    try:        
        body = await request.json() if request.method in ["POST", "PUT", "PATCH"] else None   
        url = f"{service_url}/{path}"

        # 同步调用，这里会阻塞
        response = requests.post(url, json = body)
        return response.json()
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content="非法请求。")    

 
# 启动网关
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)