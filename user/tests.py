import json
import jwt
import bcrypt
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
        """
        회원가입 성공 테스트
        """
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
    
    def test_fail_SignUp_Serializer_Error_post(self):
        """
        회원가입 실패 테스트
        요청 데이터가 잘못된 경우
        """
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

    def test_fail_SignUp_Unique_email_invalid_post(self):
        """
        회원가입 실패 테스트
        이메일이 중복된 경우
        """
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
        """
        회원가입 실패 테스트
        이메일 형식을 잘못 입력한 경우
        """
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
        """
        회원가입 실패 테스트
        비밀번호 형식을 잘못 입력한 경우
        """
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

    
class LoginInAPITest(TestCase):
    def setUp(self):
        User.objects.create(id=1, name="kim",email="kim@naver.com",password=bcrypt.hashpw("kim12345!".encode("utf8"),bcrypt.gensalt()).decode("utf8"),plan_money=10000)

    def tearDown(self):
        User.objects.all().delete()
    
    def test_success_LogIn_post(self):
        """
        로그인 성공 테스트
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "id" :1,
                "email": "kim@naver.com",
                "password" : "kim12345!"
                }
        
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/login', json.dumps(data), content_type='application/json', **headers)
        # self.assertEqual(response.json(), {'access': 'access_token'})
        self.assertEqual(response.status_code, 201)
    
    def test_fail_LogIn_Serializer_Error_post(self):
        """
        로그인 실패 테스트
        로그인 요청 데이터가 잘못 된 경우
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "id" :1,
                "email": "kim@naver.com",
                # "password" : "kim12345!" # 요청데이터를 serialize에서 유효성 검사
                }
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/login', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.json(), {'msg': {'password': ['This field is required.']}})
        self.assertEqual(response.status_code, 400)
    
    def test_fail_Login_not_found_user_Error_post(self):
        """
        로그인 실패 테스트
        회원가입이 되지 않은 경우
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "id" :1,
                "email": "lee@naver.com", # 잘못된 이메일 주소
                "password" : "kim12345!" 
                }
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/login', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.json(), {'msg': 'Can Not Find User'})
        self.assertEqual(response.status_code, 400)
    
    def test_fail_Login_not_match_Password_Error_post(self):
        """
        로그인 실패 테스트
        패스워드를 잘못 입력한 경우
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "id" :1,
                "email": "kim@naver.com",
                "password" : "12345" # 잘못된 비밀번호 
                }
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/login', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.json(), {'msg': 'Please check your E-mail or Password'})
        self.assertEqual(response.status_code, 400)