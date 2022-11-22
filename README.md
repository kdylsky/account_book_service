# Account book Service

### 유저의 가계부 작성 서비스를 위한 REST API 서비스


<br>

## 목차

  * [개발 기간](#개발-기간)
  * [개발 인원](#개발-인원)
  * [프로젝트 개요](#프로젝트-개요)
      - [프로젝트 설명](#01-프로젝트-설명)
      - [개발 조건](#02-개발-조건)
      - [사용 기술](#03-사용-기술)
      - [모델링](#04-모델링)
      - [디렉토리 구조](#05-디렉토리-구조)
      - [API Test](#06-api-test)
  * [프로젝트 분석](#프로젝트-분석)
  * [API ENDPOINT](#api-endpoint)



<br>

## 개발 기간
**2022.11.03 ~ 2022.11.05** 

<br>
<br>
  
## 개발 인원
**Back-end  : 김도연**

<br>
<br>


## 프로젝트 개요


<br>

#### 01. 프로젝트 설명

<u> `인가`된 회원의 가계부 작성 REST API 개발</u>
 
<br>
<br>

#### 02. 개발 조건

> <br>
>
> * **데이터**
> 	* 서울시 OpenAPI 요청시 응답데이터
> 	* 주어진 데이터셋이 효과적으로 이용될 수 있게 자유롭게 모델링하여 구현 
>
><br>
>
> * **API**
>
>   *   **User API**
>       * 유저의 회원가입, 로그인
>
>   *   **Acoount API**
>       * 유저는 가계부에 사용한 금액과 메모를 추가할수 있다.   
>       * 유저는 작성한 가계부의 내용을 볼 수 있다.
>       * 유저는 추가된 내용을 삭제할 수 있다.
>       * 유저는 삭제된 내용을 다시 복구 할 수 있다.
>
> <br>
<br>
<br>

<br>


#### 03. 사용 기술 

- **Back-End** : Python, Django, Django REST Framework
- **Database** : MySQL, ERDCloud
- **HTTP**     : Postman
- **ETC**      : Git, Github, Miniconda


<br>
<br>

#### 04. 모델링

<br>


<p align="center"><img width="800" src="image/modeling_accountbook.png"></p>

<br>

- 주어진 데이터를 처리하는 과정을 고려하여 `User(유저)`, `AccountBook(가계부)` `Pay(지출)` 3개의 테이블로 설정했습니다. 
	- `User(유저)`는 여러개의 `AccountBook(가계부)`를 가질 수 있다(1:M).
  - `AccountBook(가계부)`는 여러개의 `Pay(지출)`를 가질 수 있다(1:M).

<br>

- `AccountBook(가계부)`는 날짜를 유닉크 한 값으로 가진다.
    - 유저는 날짜 별로 가계부 객체를 가질 수 있다.
    - 가계부는 특정 날짜(ex)11월1일)를 기준으로 여러 `Pay(지출)` 가질 수 있다. 

<br>
<br>

#### 05. 디렉토리 구조
<br>


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

#### 06. API Test
<br>

- DB에 저장된 데이터 조회 성공 & 실패 케이스를 구현

<p align="center"><img width="800" src="image/test_accountbook.png"></p>



<br>
<br>

## 프로젝트 분석

<br>

- 데이터모델링의 구조를 생각하여 `user`와 `accountbook` 2개의 앱으로 분리 

<br>

- User API
    - 회원가입
      - email 유니크한 속성으로 설정 후 중복확인
      - `bcrypt모듈` 이용하여 password를 hash한 값을 DB에 저장
      - DB저장시 decode()한 결과값을 저장, 그렇지 않은 경우 로그인 시도 시 invalid salt 오류 발생
    - 로그인
      - bcrypt checkpw()로 DB와 사용자 입력 password 비교 후 처리
      - 로그인 성공 시 `jwt를 이용`, 토큰을 발급
    - 데코레이터
      - 로그인시 발급된 jwt토큰을 jwt모듈을 이용해서 payload에 담기 정보를 추출
      - 데코레이터를 이용해 로그인이 필요한 서비스에 대해 인가

<br>
<br>
<br>



- Account API
  - 가계부 생성API
    - 가계부 생성은 두단계로 이루어진다.
    - 먼저 날짜를 만드는 Accoutbook객체를 생성, `get_or_create()`를 이용해서, 
      이미 존재하는 객체가 존재한다면 객체를 가지고오고, 아니면 새로운 객체를 생성
    - Accountbook객체가 생성된 후 Pay객체를 생성하고 Accountbook객체의 하루 총 금액을 증가
<br>
<br>

  - 가계부 전체리스트API
    - 대량의 데이터를 한 번에 가지고 오는 것은 데이터베이스와 서비스에 부담이 되기 때문에 유저가 가지고 있는 모든 객체를 가지고 오지 않고 현재 날짜를 기준으로 디폴트로는 30일까지 반환 
     
    - `offset`으로 값을 요청 시 해당 하는 개월 수 전까지 반환
        ex)offset=2 -> 60 일 전까지
<br>
<br>

  - 가계부 삭제API
    - `쿼리파라미터(delete_list)` 원하는 Accountbook객체를 선택, 해당 객체의 삭제상태(delete_state)가 False인 경우만 삭제 처리
    - Accountbook객체가 삭제되면 객체 안에 존재하는 Pay객체 역시 삭제상태(delete_state)를 True로 변경
<br>
<br>
  
  - 삭제된 가계부 리스트API
     - 삭제상태가 True인 Accountbook객체만을 출력
<br>
<br>

  - 삭제된 가계부 복구API
    - 쿼리파라미터(recovery_list)로 Accountbook객체 선택, 해당 객체의 삭제상태(delete_state)를 False로 변경
    - Accountbook객체의 Pay객체도 삭제 상태를 True로 변경
<br>
<br>
  
  - 특정날짜 기준 지출리스트 API
    - path파라미터를 이용 특정 날짜를 지정해서 날짜에 해당하는 지출 객체 모두 출력
<br>
<br>
  
  - 특정날짜 기준 지출 삭제API
    - 날짜에 해당하는 Pay객체 삭제
    - 삭제시 Accountbook객체의 하루 총 사용 금액에서 Pay객체의 money만큼 감산
<br>
<br>
  
  - 특정날짜 기준 지출 삭제 복구 API
    - 삭제된 Pay객체를 복구
    - 복구시 Accountbook객체의 하루 총 사용 금액에 다시 Pay객체의 money만큼 가감
<br>
<br>
  
  - 특정날짜 기준 지출 수정 API
    - 지출 관련 내용 수정 가능
    - `restframework에 이미 정의된 클래스를 재정의`해서 구현
    - partical=True에 해당하기 때문에 모든 내용에 대한 수정이 아닌 특정 내용에 대한 수정

<br>
<br>
<br>


## API ENDPOINT

URL|Method|Description|</br>

<br>

## User
### 1. signup
<br>

URL|Method|Description|
|------|---|---|
|"/signup"|POST|회원가입|

<br>

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
<br>

-URL|Method|Description|
|------|---|---|
|"/login"|POST|로그인|

<br>

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
### 1. 가계부 생성
<br>

URL|Method|Description|
|------|---|---|
|"/accountbook"|POST|가계부 생성|

<br>


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
    
### 2. 가계부 리스트
<br>

URL|Method|Description|
|------|---|---|
|"/accountbook"|GET|가계부 리스트 조회|

<br>


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


### 3. 가계부 삭제
<br>

URL|Method|Description|
|------|---|---|
|"/accountbook?delete_list=10"|DELETE|가계부 삭제|

<br>

- response
    
```json
    {
        true
    }
```
<br>
<br>
    
    
### 4. 가계부 삭제 리스트
<br>

URL|Method|Description|
|------|---|---|
|"/deleted"|GET|삭제된 가계부 조회|

<br>

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


### 5. 날짜기준으로 Pay객체 가지고 오기
<br>

URL|Method|Description|
|------|---|---|
|"/accountbook/2022-11-05"|GET|pay객체 조회|

<br>

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

### 6. 날짜기준으로 Pay객체 삭제하기
<br>

URL|Method|Description|
|------|---|---|
|"/accountbook/2022-11-01?delete_list=22"|DELETE|pay객체 삭제|

<br>

- response
```json
  {
      true
  }
```
<br>
<br>



### 7. 날짜기준으로 Pay객체 복구하기
<br>

URL|Method|Description|
|------|---|---|
|"/accountbook/2022-11-01?recovery_list=22"|PATCH|pay객체 복구|

<br>

- response
    
```json
    {
      true
    }
```

<br>
<br>


### 8. 날짜기준으로 Pay객체 내용 수정하기
<br>

URL|Method|Description|
|------|---|---|
|"/accountbook/2022-11-01/22"|PUT|pay객체 내용 수정|

<br>

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

