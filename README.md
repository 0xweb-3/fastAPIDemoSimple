# 超简单的FastAPI使用

## 项目初始化
```shell
uv init fastAPIDemoSimple -p 3.13.9
cd fastAPIDemoSimple
uv venv # 建立虚拟环境

uv add fastapi uvicorn
```

## 启动
```shell
uvicorn main:app --reload
```
文档http://127.0.0.1:8000/docs 

## 进度
* v1.1.0 helloWorld✅
* v1.2.0 传参✅
* v1.3.0 异步-响应状态码
* v1.4.0 商品案例
* v1.5.0 ApIRouter路由
