import bcrypt
import jwt
import json
from django.test import TestCase, Client
from django.conf import settings
from datetime import datetime
from user.models import User
from accountbook.models import AccountBook, Pay

class AccountBookAPITest(TestCase):
    def setUp(self) -> None:
        User.objects.create(
            id=1,
            name="kim",
            plan_money=10000,
            email="kim@gamil.com",
            password=bcrypt.hashpw("kim12345!".encode("utf8"),bcrypt.gensalt()).decode("utf8")
        )
        
        AccountBook.objects.bulk_create([
            AccountBook(id=100,user=User.objects.get(id=1),day="2022-11-01",day_total=0,delete_status=False),
            AccountBook(id=200,user=User.objects.get(id=1),day="2022-11-02",day_total=0,delete_status=False),
        ])
        
        Pay.objects.bulk_create([
            Pay(id=1,accountbook=AccountBook.objects.get(id=100),money=20000,title="외식비",memo="외식을했다.",delete_status=False),
            Pay(id=2,accountbook=AccountBook.objects.get(id=100),money=20000,title="활동비",memo="활동을했다.",delete_status=False),
            Pay(id=3,accountbook=AccountBook.objects.get(id=200),money=20000,title="출장비",memo="출장을갔다.",delete_status=False),
            Pay(id=4,accountbook=AccountBook.objects.get(id=200),money=20000,title="호텔비",memo="호텔에갔다.",delete_status=False),
        ])
                
    def tearDown(self) -> None:
        User.objects.all().delete()
        AccountBook.objects.all().delete()
        Pay.objects.all().delete()
    
    def test_Success_create_accountbook_post(self):
        """
        가계부 Create API
        성공
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "day":"2022-11-01",
                "money":20000,
                "title":"외식비",
                "memo":"외식을 왔다"
            }
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/accountbook', json.dumps(data),content_type='application/json', **headers)
        # self.assertEqual(response.json(), {"transfer_identifier": 3})
        self.assertEqual(response.status_code, 201)

    def test_Fail_create_account_Serializer_post(self):
        """
        가계부 Create API
        실패 요청 파라미터의 serialize 에러
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                # "day":"2022-11-01",
                "money":20000,
                "title":"외식비",
                "memo":"외식을 왔다"
            }
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/accountbook', json.dumps(data),content_type='application/json', **headers)
        self.assertEqual(response.json(), {'msg': {'day': ['This field is required.']}})
        self.assertEqual(response.status_code, 400)
    
    def test_Fail_create_account_Negative_Integer_post(self):
        """
        가계부 Create API
        실패 요청 파라미터 중 memoy가 음수인 에러
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "day":"2022-11-01",
                "money":-20000,
                "title":"외식비",
                "memo":"외식을 왔다"
            }
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/accountbook', json.dumps(data),content_type='application/json', **headers)
        self.assertEqual(response.json(), {'msg': 'Money Can not be Negative Integer'})
        self.assertEqual(response.status_code, 400)
    

    def test_Success_Get_account_list_get(self):
        """
        가계부 Get API
        성공 
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.get('/accountbook', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
    
    def test_Success_Get_with_offset_account_list_get(self):
        """
        가계부 Get API
        성공 with offset 
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.get('/accountbook?/offset=2', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
    
    def test_Success_Delete_account_delete(self):
        """
        가계부 Delete API
        성공
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.delete('/accountbook?/delete_list=100&delete_list=200', content_type='application/json', **headers)
        self.assertEqual(response.json(), True)
        self.assertEqual(response.status_code, 200)

    def test_Fail_Delete_account_Not_found_delete_list_delete(self):
        """
        가계부 Delete API
        실패
        delete_list=77&delete_list=88 잘못된 accountbook ID
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.delete('/accountbook?/delete_list=77&delete_list=88', content_type='application/json', **headers)
        self.assertEqual(response.json(), {'msg': 'Not Found check delete_list params'})
        self.assertEqual(response.status_code, 400)



class DeleteAPITest(TestCase):
    def setUp(self) -> None:
        User.objects.create(
            id=1,
            name="kim",
            plan_money=10000,
            email="kim@gamil.com",
            password=bcrypt.hashpw("kim12345!".encode("utf8"),bcrypt.gensalt()).decode("utf8")
            )
        
        AccountBook.objects.bulk_create([
            AccountBook(id=300,user=User.objects.get(id=1),day="2022-11-03",day_total=0,delete_status=True),
            AccountBook(id=400,user=User.objects.get(id=1),day="2022-11-04",day_total=0,delete_status=True),
        ])
        
        Pay.objects.bulk_create([
            Pay(id=5,accountbook=AccountBook.objects.get(id=300),money=20000,title="외식비",memo="외식을했다.",delete_status=True),
            Pay(id=6,accountbook=AccountBook.objects.get(id=300),money=20000,title="활동비",memo="활동을했다.",delete_status=True),
            Pay(id=7,accountbook=AccountBook.objects.get(id=400),money=20000,title="출장비",memo="출장을갔다.",delete_status=True),
            Pay(id=8,accountbook=AccountBook.objects.get(id=400),money=20000,title="호텔비",memo="호텔에갔다.",delete_status=True),
        ])
        
    def tearDown(self) -> None:
        User.objects.all().delete()
        AccountBook.objects.all().delete()
        Pay.objects.all().delete()
    
    def test_Success_Get_Deleted_account_list_get(self):
        """
        삭제된 Get 가계부 API
        성공
        리스트로 가지고 오기 
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.get('/deleted', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)

    def test_Success_Patch_Deleted_account_recovery_patch(self):
        """
        삭제된 patch 가계부 API
        성공
        파라미터를 받아서 True->False로 바꾸기 
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.patch('/deleted?recovery_list=400', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)

    def test_fail_Patch_Dleted_recovery_not_found_recovery_number_patch(self):
        """
        삭제된 patch 가계부 API
        실패
        파라미터로 잘못된 값이 들어옴 
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.patch('/deleted?recovery_list=1000', content_type='application/json', **headers)
        self.assertEqual(response.json(), {'msg': 'Not Found check recovery_list params'})
        self.assertEqual(response.status_code, 400)



class PayObjectAPITest(TestCase):
    def setUp(self) -> None:
        User.objects.create(
            id=1,
            name="kim",
            plan_money=10000,
            email="kim@gamil.com",
            password=bcrypt.hashpw("kim12345!".encode("utf8"),bcrypt.gensalt()).decode("utf8")
            )
        
        AccountBook.objects.bulk_create([
            AccountBook(id=100,user=User.objects.get(id=1),day="2022-11-01",day_total=0,delete_status=False),
            AccountBook(id=200,user=User.objects.get(id=1),day="2022-11-02",day_total=0,delete_status=False),
            AccountBook(id=300,user=User.objects.get(id=1),day="2022-11-03",day_total=0,delete_status=True),
            AccountBook(id=400,user=User.objects.get(id=1),day="2022-11-04",day_total=0,delete_status=True),
        ])
        
        Pay.objects.bulk_create([
            Pay(id=1,accountbook=AccountBook.objects.get(id=100),money=20000,title="외식비",memo="외식을했다.",delete_status=False),
            Pay(id=2,accountbook=AccountBook.objects.get(id=100),money=20000,title="활동비",memo="활동을했다.",delete_status=False),
            Pay(id=3,accountbook=AccountBook.objects.get(id=200),money=20000,title="출장비",memo="출장을갔다.",delete_status=False),
            Pay(id=4,accountbook=AccountBook.objects.get(id=200),money=20000,title="호텔비",memo="호텔에갔다.",delete_status=False),
            Pay(id=5,accountbook=AccountBook.objects.get(id=300),money=20000,title="외식비",memo="외식을했다.",delete_status=True),
            Pay(id=6,accountbook=AccountBook.objects.get(id=300),money=20000,title="활동비",memo="활동을했다.",delete_status=True),
            Pay(id=7,accountbook=AccountBook.objects.get(id=400),money=20000,title="출장비",memo="출장을갔다.",delete_status=True),
            Pay(id=8,accountbook=AccountBook.objects.get(id=400),money=20000,title="호텔비",memo="호텔에갔다.",delete_status=True),
        ])

    def tearDown(self) -> None:
        User.objects.all().delete()
        AccountBook.objects.all().delete()
        Pay.objects.all().delete()
    
    def test_Success_Get_special_date_pay_obj_list_get(self):
        """
        Get 특정 날짜의 Pay객체 가지고 오기
        성공
        예를 들어 11/1일 사용한 
        pay객체1, pay객체2 가지고 오기
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.get('/accountbook/2022-11-01', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
    
    def test_Success_Delete_special_date_pay_obj_delete(self):
        """
        Delete 특정 날짜의 Pay객체 
        성공
        예를 들어 11/1일 사용한 pay객체1, pay객체2 중
        pay객체 삭제하기
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.delete('/accountbook/2022-11-01?delete_list=1&delete_list=2', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
    
    def test_Fail_Delete_Not_found_date_pay_obj_delete(self):
        """
        Delete 특정 날짜의 Pay객체 
        실패
        예를 들어 11/1일 사용한 pay객체1, pay객체2 중
        pay객체3 삭제 시도
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.delete('/accountbook/2022-11-01?delete_list=3', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
    
    def test_Success_Patch_recovery_special_date_pay_obj_patch(self):
        """
        Delete 특정 날짜의 Pay객체 
        성공
        예를 들어 11/1일 사용한 pay객체1, pay객체2가 delete_status=True인 상태
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.patch('/accountbook/2022-11-03?recovery_list=5', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
    
    def test_Fail_Patch_Not_found_recovery_date_pay_obj_patch(self):
        """
        Delete 특정 날짜의 Pay객체 
        실패
        예를 들어 11/1일 사용한 pay객체1, pay객체2 중
        pay객체3 수정 시도
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.delete('/accountbook/2022-11-03?recovery_list=100', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)



class PayPartialUpdateViewTest(TestCase):
    def setUp(self) -> None:
        User.objects.create(
            id=1,
            name="kim",
            plan_money=10000,
            email="kim@gamil.com",
            password=bcrypt.hashpw("kim12345!".encode("utf8"),bcrypt.gensalt()).decode("utf8")
            )
        
        AccountBook.objects.bulk_create([
            AccountBook(id=100,user=User.objects.get(id=1),day="2022-11-01",day_total=0,delete_status=False),
            AccountBook(id=200,user=User.objects.get(id=1),day="2022-11-02",day_total=0,delete_status=False),
            AccountBook(id=300,user=User.objects.get(id=1),day="2022-11-03",day_total=0,delete_status=True),
            AccountBook(id=400,user=User.objects.get(id=1),day="2022-11-04",day_total=0,delete_status=True),
        ])
        
        Pay.objects.bulk_create([
            Pay(id=1,accountbook=AccountBook.objects.get(id=100),money=20000,title="외식비",memo="외식을했다.",delete_status=False),
            Pay(id=2,accountbook=AccountBook.objects.get(id=100),money=20000,title="활동비",memo="활동을했다.",delete_status=False),
            Pay(id=3,accountbook=AccountBook.objects.get(id=200),money=20000,title="출장비",memo="출장을갔다.",delete_status=False),
            Pay(id=4,accountbook=AccountBook.objects.get(id=200),money=20000,title="호텔비",memo="호텔에갔다.",delete_status=False),
            Pay(id=5,accountbook=AccountBook.objects.get(id=300),money=20000,title="외식비",memo="외식을했다.",delete_status=True),
            Pay(id=6,accountbook=AccountBook.objects.get(id=300),money=20000,title="활동비",memo="활동을했다.",delete_status=True),
            Pay(id=7,accountbook=AccountBook.objects.get(id=400),money=20000,title="출장비",memo="출장을갔다.",delete_status=True),
            Pay(id=8,accountbook=AccountBook.objects.get(id=400),money=20000,title="호텔비",memo="호텔에갔다.",delete_status=True),
        ])

    def tearDown(self) -> None:
        User.objects.all().delete()
        AccountBook.objects.all().delete()
        Pay.objects.all().delete()
    
    def test_Success_Pay_obj_partial_update(self):
        """
        가계부 put 메서드
        성공
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data        = {"title":"생활비"}
        
        headers     = {'HTTP_AUTHORIZATION' : token}        
        response    = client.put('/accountbook/2022-11-01/1', data=json.dumps(data),content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
    
    def test_Fail_Not_Found_Pay_obj_partial_update(self):
        """
        가계부 put 메서드
        실패 
        Pay객체를 찾지 못함
        ex)2022-01-01/10000
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data        = {"title":"생활비"}
        
        headers     = {'HTTP_AUTHORIZATION' : token}        
        response    = client.put('/accountbook/2022-01-01/10000', data=json.dumps(data),content_type='application/json', **headers)
        self.assertEqual(response.json(), {'msg': 'Not Found check Date or Payobject_id'})
        self.assertEqual(response.status_code, 400)