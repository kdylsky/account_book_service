## ✅ 가계부API

요구사항
- 유저의 회원가입, 로그인
- 유저는 가계부에 사용한 금액과 메모를 추가할수 있다.
- 유저는 작성한 가계부의 내용을 볼 수 있다.
- 유저는 추가된 내용을 삭제할 수 있다.
- 유저는 삭제된 내용을 다시 복구 할 수 있다.

<br>
<br>
<br>

## ✅ 개발 인원
- Back-end  : 김도연

<br>
<br>
<br>

## ✅ 개발 기간
- 2022.11.03 ~ 2022.11.05 (3일)

<br>
<br>
<br>

## ✅ DB 모델링
- 모델링
<img width="1000" src="image/modeling_accountbook.png">

<br>

### 주요 관계

프로젝트에서 중요한 관계 
- 유저(User)와 가계부(AccountBook)
- 가계부(AccountBook)와 지출(Pay)의 관계이다.
<br>

<u>유저는 가계부(날짜별)를 생성할 수 있다.
가계부에는 특정 날짜에 해당하는 여러 지출이 있다.</u><br>

<br>

유저와 가계부사이에는 1:M의 관계가 성립힌다.<br>
한 명의 유저는 날짜별로 가계부를 가질 수 있기 때문에 여러개의 가계부 객체를 가지게 된다.

<br>
가계부와 지출사이에는 1:M의 관계가 성립한다.<br>
11월1일 가계부에는 여러 지출 항목이 있을 수 있다. 11월 1일 지출 객체로는 생활비, 교통비 등 다양한 객체가 존재할 수 있다.<br>


<br>
<br>
<br>

## ✅ Directory 구조
```
.
├── __pycache__
├── accountbook
├── accountbook_service
├── configs
├── decorators
├── provider
├── user
├── exceptions.py
├── manage.py
└── requiremenets.py
 
```
<br>
<br>
<br>

## ✅ 백엔드 역할

```
  - (POST)    회원가입API 
  - (POST)    로그인API
  - (POST)    가계부 생성API
  - (GET)     가계부 전체리스트API
  - (DELETE)  가계부 삭제API
  - (GET)     삭제된 가계부 리스트API
  - (PATCH)   삭제된 가계부 복구API
  - (GET)     특정날짜 기준 지출리스트 API
  - (DELETE)  특정날짜 기준 지출 삭제API
  - (PATCH)   특정날짜 기준 지출 삭제 복구 API
  - (PUT)     특정날짜 기준 지출 수정 API
```

<br>

### 회원가입 API

- HTTP의 POST메서드에 해당하며, body를 통해서 회원가입에 필요한 데이터를 받음
- 유저의 경우 email을 유니크한 속성으로 만들어서 중복확인
- password는 bcrypt 모듈을 이용, 전달받은 데이터를 gensalt(), hashpw()를 이용해서 Rainbow table Attack을 방지 
- hashpw에 해당하는 패스워드를 DB에 저장
- DB 저장시 decode()를 해서 저장, 그렇지 않을 경우 로그인시 invalid salt 오류 발생
<br>
<br>

### 로그인 API

- bcrypt의 checkpw()를 이용 전달받은 패스워드와 DB의 패스워드가 같은지 확인
- 로그인 성공 시 jwt를 이용, 토큰을 발급
- jwt로 각각, 유저id를 payload에 담아 알고리즘과 시크릿키를 이용 encode 후 전달

<br>

### 로그인 데코레이터

- 로그인시 발급된 jwt토큰을 jwt모듈을 이용해서 payload에 담기 정보를 추출
- 데코레이터를 이용해 로그인이 필요한 서비스에 대해 인가

<br>

### 가계부 생성API

- 가계부 생성은 두단계로 이루어진다.
- 먼저 날짜를 만드는 Accoutbook객체를 생성, get_or_create()를 이용해서,<br> 
이미 존재하는 객체가 존재한다면 객체를 가지고오고, 아니면 새로운 객체를 생성
- Accountbook객체가 생성된 후 Pay객체를 생성하고 Accountbook객체의 하루 총 금액을 증가시킨다.

<br>

### 가계부 전체리스트API

- 유저가 가지고 있는 가계부 객체를 가지고 온다. 단, 모든 객체를 가지고 오지 않고 현재 날짜를 기준으로 디폴트로는 최대 30일까지 가지고 온다. <br>
대량의 데이터를 한 번에 가지고 오는 것은 데이터베이스와 서비스에 부담이 될 수 있기 때문에 다음과 같이 구현했다.

- offset으로 값을 제공시 해당 하는 개월 수 전까지 가지고 온다.<br>
ex)offset=2 -> 60 일 전까지


<br>

### 가계부 삭제API

- 쿼리파라미터(delete_list) 원하는 Accountbook객체를 선택, 해당 객체의 삭제상태(delete_state)가 False인 경우만 삭제 처리
- Accountbook객체가 삭제되면 객체 안에 존재하는 Pay객체 역시 삭제상태(delete_state)를 True로 변경해주어야 한다.


<br>

### 삭제된 가계부 리스트API

- 삭제상태가 True인 Accountbook객체만을 출력

<br>

### 삭제된 가계부 복구API

- 쿼리파라미터(recovery_list)로 Accountbook객체 선택, 해당 객체의 삭제상태(delete_state)를 False로 변경해서 복수
- Accountbook객체의 Pay객체도 삭제 상태를 True로 변경

<br>

### 특정날짜 기준 지출리스트 API

- path파라미터를 이용 특정 날짜를 지정해서 날짜에 해당하는 지출 객체 모두 출력



<br>

### 특정날짜 기준 지출 삭제API

- 날짜에 해당하는 Pay객체 삭제
- 삭제시 Accountbook객체의 하루 총 사용 금액에서 Pay객체의 money만큼 빼준다.

<br>

### 특정날짜 기준 지출 삭제 복구 API

- 삭제된 Pay객체를 복구
- 복구시 Accountbook객체의 하루 총 사용 금액에 다시 Pay객체의 money만큼 더해준다.

<br>

### 특정날짜 기준 지출 수정 API

- 지출 관련 내용 수정 가능하다.
- restframework에 이미 정의된 클래스를 재 정의해서 구현
- partical=True에 해당하기 때문에 모든 내용에 대한 수정이 아닌 특정 내용에 대한 수정
<br>
<br>
<br>

## ✅ 백엔드 기술 스택
  - Back-end : Python, Django, JWT, Miniconda, DRF 
  - Database : erdcloud, MySQL
  - HTTP     : Postman
  - Common   : Git & Github
    
<br>
<br>
<br>

## ✅ API 

<br>

## User
### 1. signup

- url: /signup
- method: POST
- request
  
  ```json
  {
    "name":"test",
    "email":"test@gamil.com",
    "password":"test12345!",
    "plan_money":100000
  }
  ```
- response
    ```json
    {
    "id": 7,
    "created_at": "2022-11-05T14:40:09.727682Z",
    "updated_at": "2022-11-05T14:40:09.727728Z",
    "name": "test",
    "email": "test@gamil.com",
    "password": "$2b$12$tNdv/0Z1DFGWUCwdwpiAX.P7vG2RggtSmQEBrI6NrCa4xcn5VW5La",
    "plan_money": 100000
    }
    ```
<br>
<br>


### 2. login

- url: /login
- method: POST    
- request
  ```json
  {
    "email":"test@gamil.com",
    "password":"test12345!"
  }
  ```
- response
    
    ```json
    {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NywiZXhwIjoxNjY3NjYyODgxLjY0MzEzNX0.EBDRHS3rUSOG7yeOTffnJEr9962WXCFMVsvxr0xU4Ig"
    }
    ```
<br>
<br>


## AccountBook(가계부)
### 가계부 생성

- url: /accountbook
- method: POST
- request
    
    ```json
    {
      "day":"2022-11-01",
      "money":777,
      "title":"외식비",
      "memo":"외식을 왔다"
    }
    ```
    
- response
    
    ```json
    {
    "id": 22,
    "created_at": "2022-11-05T14:45:38.771179Z",
    "updated_at": "2022-11-05T14:45:38.771215Z",
    "money": 777,
    "title": "외식비",
    "memo": "외식을 왔다",
    "delete_status": false,
    "accountbook": 10
    }
    ```
<br>
<br>
    
### 가계부 리스트
- url: /accountbook
- method: GET
- request
  ```json
  [
    {
        "id": 11,
        "created_at": "2022-11-05T14:53:57.472761Z",
        "updated_at": "2022-11-05T14:53:57.478093Z",
        "day": "2022-11-02",
        "day_total": 888,
        "delete_status": false,
        "user": 7
    },
    {
        "id": 10,
        "created_at": "2022-11-05T14:45:38.765076Z",
        "updated_at": "2022-11-05T14:52:28.389425Z",
        "day": "2022-11-01",
        "day_total": 1554,
        "delete_status": false,
        "user": 7
    }
  ]
  ```
<br>
<br>


### 가계부 삭제
- url: /accountbook?delete_list=10
- method: DELETE
- response
    
    ```json
    {
        true
    }
    ```
<br>
<br>
    
    
### 가계부 삭제 리스트
- url: /deleted
- method: GET
- response
    
    ```json
    [
      {
        "id": 10,
        "created_at": "2022-11-05T14:45:38.765076Z",
        "updated_at": "2022-11-05T14:45:38.772383Z",
        "day": "2022-11-01",
        "day_total": 777,
        "delete_status": true,
        "user": 7
      },
    ]
    ```
<br>
<br>


### 날짜기준으로 Pay객체 가지고 오기
- url: /accountbook/2022-11-05
- method: PATCH
- response
  
  ```json
  [
    {
        "user": 7,
        "accountbook": "2022-11-01",
        "title": "외식비",
        "money": 777,
        "delete_status": false
    },
    {
        "user": 7,
        "accountbook": "2022-11-01",
        "title": "외식비",
        "money": 777,
        "delete_status": false
    }
  ]
  ```

<br>
<br>

### 날짜기준으로 Pay객체 삭제하기
- url: /accountbook/2022-11-01?delete_list=22
- method: DELETE
- response
  ```json
  {
      true
  }
    ```
<br>
<br>



### 날짜기준으로 Pay객체 복구하기

- url: /accountbook/2022-11-01?recovery_list=22
- method: PATCH 
- response
    
    ```json
    {
      true
    }
    ```

<br>
<br>


### 날짜기준으로 Pay객체 내용 수정하기

- url: /accountbook/2022-11-01/22
- method: PUT
- request
    ```json
    {
    "money":999999,
    "title":"활동비",
    "memo" : "여행을 왔다."
    }
    
    ```
- response
    
    ```json
    {
    "id": 22,
    "created_at": "2022-11-05T14:45:38.771179Z",
    "updated_at": "2022-11-05T15:04:51.103210Z",
    "money": 999999,
    "title": "활동비",
    "memo": "여행을 왔다.",
    "delete_status": true,
    "accountbook": 10
    }
    ```

<br>
<br>
<br>

## ✅ Postman
- 주소 : https://documenter.getpostman.com/view/22269789/2s8YYFr4Cg#33c2e714-5ac7-4486-be73-3d30df6f86d2

<br>
<br>
<br>

## ✅ UnitTest

<img width="1000" src="image/test_accountbook.png">
