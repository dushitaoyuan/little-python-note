# python note 


python-note 是一个python 的markdown预览和发布小程序

工作场景:
1. typora+git  编写 markdown
2. python-note 发布文件

## note-front 启动

```shell
cd note-front
npm install cnpm -g
cnpm install
npm run dev

```

访问: 

http://localhost:8081/#/login

输入账户密码: dushitaoyuan/dushitaoyuan



## note-backend 启动

```shell
cd note-backend

pip install -r requirements.txt
cd src/main
uvicorn web.main:app --reload --port 8080
```

