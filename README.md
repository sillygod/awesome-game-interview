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

````sh
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


## Run Test

we use `pytest` with django.

coverage?

# DEPLOY


```sh
pip install -r requirements/prod.txt # or

pipenv install
```

prod.py

```py
DEBUG = False
```


## Design

### JWT auth

JWT auth, please put it in the header
Authorization: JWT <jwt_token>

### Serializer

request -> serialzier
serialzier -> response


## Todo

 - regular expression for mobile
 - ajdust the response with a wrap to success.. code..
 - write test
 - fix some bugs..


1. 請使用python完成以下API

2. 資料庫可使用任意資料庫，包括mysql及sqlite等等

3. 時間為1小時，提早完成可提早交付

4. 程式碼請上傳至github，並將連結回信附上即可，如需編譯請將編譯方式寫入read.me

5. 以json為回傳格式

6. API

⁃ 使用者註冊

⁃ Route: [POST] /user/register

⁃ 參數

⁃ username: string 帳號，須為英文開頭，6~20位元

⁃ password: string 密碼，需同時有英數字，6~20位元

⁃ name: string 姓名

⁃ email: string Email

⁃ mobile: string 手機號碼，台灣手機

⁃ 回傳

⁃ success: 1|0 1:成功 0:失敗

⁃ errorCode: 錯誤代碼

⁃ errorMessage: 錯誤訊息，失敗原因

⁃ 使用者登入

⁃ Route: [POST] /user/login

⁃ 參數

⁃ username: string 帳號或手機皆可用來登入

⁃
 password: string 密碼

⁃ 回傳

⁃ success: 1|0 1:成功 0:失敗

⁃ token: 登入 auth token

⁃ errorCode: 錯誤代碼

⁃ errorMessage: 錯誤訊息，失敗原因

⁃ 使用者留言

⁃ Route: [POST] /user/message

⁃ 參數

⁃ token: string 使用者登入token

⁃ message: string 留言內容

⁃ 回傳

⁃ success: 1|0 1:成功 0:失敗

⁃ errorCode: 錯誤代碼

⁃ errorMessage: 錯誤訊息，失敗原因

⁃ 使用者回覆留言

⁃ 規則：僅可回覆留言(message)，不可回覆回覆(reply)

⁃ Route: [POST] /user/message/reply

⁃ 參數

⁃ token: string 使用者登入token

⁃ message_id: string Message ID

⁃ reply: string 回覆內容

⁃ 回傳

⁃ success: 1|0 1:成功 0:失敗

⁃ errorCode: 錯誤代碼

⁃ errorMessage: 錯誤訊息，失敗原因
