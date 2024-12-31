@echo off
echo start translation service

REM 启动API网关和所有服务

REM 切换到当前批处理文件所在的目录
cd /d %~dp0

echo 激活虚拟环境...
call .venv\Scripts\activate

echo 启动翻译服务
start python "services\service translation\api.py"

echo 启动咨询服务
start python "services\service consulting\api.py"

echo 启动网关
start python "gateway\api gateway with oauth2 authentication based on fastapi.py"

pause