import json
import jwt
from datetime import datetime
from django.conf import settings
from django.test import TestCase, Client
from user.models import User


class SignUpAPITest(TestCase):
    def setUp(self):
        User.objects.create(id=1, name="kim",email="kim@naver.com",password="kim12345!",plan_money=10000)

    def tearDown(self):
        User.objects.all().delete()

    def test_success_SignUp_post(self):
        client = Client()
        data = {
            "id" : 2,
            "name":"lee",
            "email":"lee@naver.com",
            "password":"lee12345!",
            "plan_money":100000
        }
        response = client.post("/signup", data=json.dumps(data), content_type='application/json') 

        body={
                "id": 2,
                "name": "lee",
                "email": "lee@naver.com",
                "plan_money": 100000
            }

        self.assertEqual(response.status_code, 201)
    
    def test_fail_SignUp_Unique_email_invalid_post(self):
        client = Client()
        data = {
            "id" : 1,
            "name":"kim",
            "email":"kim@naver.com",
            "password":"kim12345!",
            "plan_money":100000
        }
        response = client.post("/signup", data=json.dumps(data), content_type='application/json') 

        body={
                "msg": {
                    "email": [
                        "user with this email already exists."
                    ]
                }
            }
        self.assertEqual(response.json(), body)
        self.assertEqual(response.status_code, 400)
    
    def test_fail_SignUp_email_formatting_invalid_post(self):
        client = Client()
        data = {
            "id" : 1,
            "name":"kim",
            "email":"kimnaver.com", # 이멜일 형식이 잘못됬다.
            "password":"kim12345!", 
            "plan_money":100000
        }
        response = client.post("/signup", data=json.dumps(data), content_type='application/json') 

        body= {"msg": "Please check your Email Format" }
        self.assertEqual(response.json(), body)
        self.assertEqual(response.status_code, 400)
    
    def test_fail_SignUp_password_formatting_invalid_post(self):
        client = Client()
        data = {
            "id" : 1,
            "name":"kim",
            "email":"ki@naver.com",
            "password":"kim123", # 비밀번호 형식이 잘못됬다.
            "plan_money":100000
        }
        response = client.post("/signup", data=json.dumps(data), content_type='application/json') 

        body= {'msg': 'Please check your Password Format'}
        self.assertEqual(response.json(), body)
        self.assertEqual(response.status_code, 400)

    def test_fail_SignUp_Serializer_Error_post(self):
        client = Client()
        data = {
            "id" : 1,
            # "name":"kim", # serialize에서 정의한 모든 필드가 들어가지 않았다.
            "email":"ki@naver.com",
            "password":"kim12345!", 
            "plan_money":100000
        }
        response = client.post("/signup", data=json.dumps(data), content_type='application/json') 

        body= {'msg': {'name': ['This field is required.']}}
        self.assertEqual(response.json(), body)
        self.assertEqual(response.status_code, 400)


class LoginInAPITest(TestCase):
    def setUp(self):
        User.objects.create(id=1, name="kim",email="kim@naver.com",password="kim12345!",plan_money=10000)

    def tearDown(self):
        User.objects.all().delete()
    
    def test_success_LogIn_post(self):
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "id" :1,
                "email": "kim@naver.com",
                "password" : "kim12345!"
                }
        
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/login', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.json(), {"transfer_identifier": 3})
        self.assertEqual(response.status_code, 201)