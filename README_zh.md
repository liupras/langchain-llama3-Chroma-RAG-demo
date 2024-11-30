# langchain+llama3+Chroma RAG demo

#### 介绍
使用langchain+本地大模型+本地矢量数据库搭建RAG系统的演示。  
目前已经基本实现后台网关和基于本地大模型的翻译服务。  
- 后端网关实现简单的请求转发及登录功能
![基本架构](image/arch.png)
- 前台将使用基于vue3的vuetify实现基本的登录以及翻译服务调用功能，敬请期待。


#### 安装教程

1. 安装依赖环境
- 后端
进入`backend`目录后，执行下面的命令：
```cmd
pip install -r requirements.txt
```

#### 使用说明

详细教程参见：🔗[从零搭建langchain+本地大模型+本地矢量数据库的RAG系统](http://www.wfcoding.com/articles/practice/01%E4%BB%8E%E9%9B%B6%E6%90%AD%E5%BB%BAlangchain+%E6%9C%AC%E5%9C%B0%E5%A4%A7%E6%A8%A1%E5%9E%8B+%E6%9C%AC%E5%9C%B0%E7%9F%A2%E9%87%8F%E6%95%B0%E6%8D%AE%E5%BA%93%E7%9A%84rag%E7%B3%BB%E7%BB%9F/)
