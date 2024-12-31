@echo off
echo start translation service

REM 切换到当前批处理文件所在的目录
cd /d %~dp0

echo 激活虚拟环境...
call ..\.venv\Scripts\activate

echo 启动API...
python "api gateway with oauth2 authentication based on fastapi.py"

pause
