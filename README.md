# Awesome game interview 


## Environment

Python 3.7.

This project is mainly based on the following libraries.

 - Django 2.2
 - django restframework 3.10.3 
 - django restframework jwt 1.11.0
 - ...etc.
 
For more detial, you can see the `requirements/dev.txt` and `requirements/prod.txt`


## Installation

```sh
pip install -r requirements/dev.txt # for dev 
```

### Customize 

adjust the `settings/dev.py` or `settings/prod.py` for your need. like installed_app or database connection settings or other things.


## Run Server

You can simply run the following commands to start a dev server

```sh
python manage.py runserver
```

then open http://127.0.0.1:8000 you will see it.
or you can use `docker-compose` to run server if you don't want to install the python or other depencies

```sh
docker-compose up # this will build image first time
docker-compose run app python manage.py collectstatic
docker-compose run app python makemigrations or migrate


docker-compose run app python manage.py createsuperuser # to create a super user if you want

docker-compose logs [service name] # can see the log for certain service
```

## Swagger Doc

After spinning up the server, you can get the swagger page by opening the http://127.0.0.1:8000/api


![](https://i.imgur.com/hVJQl1Z.png)


然後目前swagger不知道為啥api group沒切好...可能有bug，時間內找不到問題。

version 目前可以輸入 `v1`

- GET /api/{version}/messages/ 獲取目前訊息列表
- POST /api/{version}/messages/ po訊息
- POST /api/{version}/messages/{id}/ 回覆

上面幾個還沒確認是否ＯＫ

- POST /api/{version}/users/login/ 登入 確認ＯＫ有回傳token
- POSt /api/{version}/users/register/ 註冊 有小bug要處理


## Run Test

we use `pytest` with django.

coverage?

# DEPLOY


```sh
pip install -r requirements/prod.txt # or
```

prod.py

```py
DEBUG = False
```


## Design

### JWT auth

JWT auth, please put it in the header
Authorization: JWT <jwt_token>

### Request Response Cycle

1. request -> serialzier

2. model process

3. serialzier -> response


## Todo

 - regular expression for mobile
 - ajdust the response with a wrap to success.. code..
 - write test
 - fix some bugs..

