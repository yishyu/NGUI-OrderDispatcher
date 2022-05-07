# NGUI-OrderDispatcher <img src ="https://orderdispatcher.chifuri.be/static/img/png/logo.png" width="40">
Repository for the "Order Checker" project for the "Next Generation User Interface" course given by Pr. Signer and Mr. Van de Wynckel. (2021-22)

## Setup your environment
1. Create a virtual environment
```
    virtualenv -p python ve/
or
    python -m venv ve/
```
2. Activate your virtual environment
```
    source ve/bin/activate
```
3. Install requirements
```
    pip install -r requirements.txt
```
4. Set Environment variables
```
    source .env
```
## Start Website Server
An instance of this is currently running on [orderdispatcher.chifuri.be](orderdispatcher.chifuri.be) so you don't need to have it running locally. However if you wish to test it locally, here are the steps to follow.
1. Change directory in NGUIOrderDispatcher/
2. Collect Static files & Start the server on 127.0.0.1:8000
```
    python manage.py collectstatic --no-input --clear
    python manage.py runserver
```
3. Connect using the test account
```
    email: test@test.com
    password: testtest
```
4. There is an admin panel on 127.0.0.1:8000/admin

## Start Local Application

Note: If you are running the web server locally, you need to change the variables in **credentials.json**
```json
"remote_url": "ip of running webserver"
"remote_port": "port of running webserver"
"shop_key": "TODO put localtest key here" // local shop api key in the database
```
- Launch App
```
    python main.py
```