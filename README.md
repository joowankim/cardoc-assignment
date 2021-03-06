# Cardoc-assignment

## 기업과제
- 기업명: 카닥
- 기업사이트: https://www.cardoc.co.kr/
- 기업채용공고: https://www.wanted.co.kr/wd/57545

## 과제 내용

#### **[필수 포함 사항]**

- READ.ME 작성
    - 프로젝트 빌드, 자세한 실행 방법 명시
    - 구현 방법과 이유에 대한 간략한 설명
    - **서버 구조 및 디자인 패턴에 대한 개략적인 설명**
    - 완료된 시스템이 배포된 서버의 주소
    - 해당 과제를 진행하면서 회고 내용 블로그 포스팅
- Swagger나 Postman을 이용하여 API 테스트 가능하도록 구현

### 1. 배경 및 공통 요구사항

<aside>
😁 카닥에서 실제로 사용하는 프레임워크를 토대로 타이어 API를 설계 및 구현합니다.

</aside>

- 데이터베이스 환경은 별도로 제공하지 않습니다.
 **RDB중 원하는 방식을 선택**하면 되며, sqlite3 같은 별도의 설치없이 이용 가능한 in-memory DB도 좋으며, 가능하다면 Docker로 준비하셔도 됩니다.
- 단, 결과 제출 시 README.md 파일에 실행 방법을 완벽히 서술하여 DB를 포함하여 전체적인 서버를 구동하는데 문제없도록 해야합니다.
- 데이터베이스 관련처리는 raw query가 아닌 **ORM을 이용하여 구현**합니다.
- Response Codes API를 성공적으로 호출할 경우 200번 코드를 반환하고, 그 외의 경우에는 아래의 코드로 반환합니다.

#### Copy of Code

| Response Code | Description |
|:---|:---|
| 200 OK | 성공 |
| 400 Bad Request | Parameter가 잘못된 (범위, 값 등) |
| 401 Unauthorized | 인증을 위한 Header가 잘못됨 |
| 500 Internal Server Error | 기타 서버 에러 |

### 2. 사용자 생성 API

🎁 **요구사항**

- ID/Password로 사용자를 생성하는 API.
- 인증 토큰을 발급하고 이후의 API는 인증된 사용자만 호출할 수 있다.

```jsx
/* Request Body 예제 */

 { "id": "candycandy", "password": "ASdfdsf3232@" }
```

### 3. 사용자가 소유한 타이어 정보를 저장하는 API

🎁 **요구사항**

- 자동차 차종 ID(trimID)를 이용하여 사용자가 소유한 자동차 정보를 저장한다.
- 한 번에 최대 5명까지의 사용자에 대한 요청을 받을 수 있도록 해야한다. 즉 사용자 정보와 trimId 5쌍을 요청데이터로 하여금 API를 호출할 수 있다는 의미이다.

```jsx
/* Request Body 예제 */
[
  {
    "id": "candycandy",
    "trimId": 5000
  },
  {
    "id": "mylovewolkswagen",
    "trimId": 9000
  },
  {
    "id": "bmwwow",
    "trimId": 11000
  },
  {
    "id": "dreamcar",
    "trimId": 15000
  }
]
```

🔍 **상세구현 가이드**

- 자동차 정보 조회 API의 사용은 아래와 같이 5000, 9000부분에 trimId를 넘겨서 조회할 수 있다.
  - **자동차 정보 조회 API 사용 예제**
    - https://dev.mycar.cardoc.co.kr/v1/trim/5000
    - https://dev.mycar.cardoc.co.kr/v1/trim/9000
    - https://dev.mycar.cardoc.co.kr/v1/trim/11000
    - https://dev.mycar.cardoc.co.kr/v1/trim/15000
- 조회된 정보에서 타이어 정보는 spec → driving → frontTire/rearTire 에서 찾을 수 있다.
- 타이어 정보는 205/75R18의 포맷이 정상이다. 205는 타이어 폭을 의미하고 75R은 편평비, 그리고 마지막 18은 휠사이즈로써 {폭}/{편평비}R{18}과 같은 구조이다.
 위와 같은 형식의 데이터일 경우만 DB에 항목별로 나누어 서로다른 Column에 저장하도록 한다.

### 4. 사용자가 소유한 타이어 정보 조회 API

🎁 **요구사항**

- 사용자 ID를 통해서 2번 API에서 저장한 타이어 정보를 조회할 수 있어야 한다.
----

## 구현 내용

카닥 과제를 위해 구현된 내용은 다음과 같습니다.
1. 사용자를 생성하기 위한 회원가입 기능
2. 사용자를 인증하고 토큰을 발급하기 위한 로그인 기능
3. 액세스 토큰 인증 기능
4. 사용자가 소유한 타이어 정보를 저장하는 기능
5. 사용자가 소유한 타이어 정보를 조회하는 기능

### 구현된 엔드포인트

엔드포인트 POSTMAN 문서: https://documenter.getpostman.com/view/12446432/UVJZpypz

- `POST /users`: 회원가입
- `POST /auth`: 로그인(액세스 토큰 발급)
- `POST /tires`: 사용자가 소유한 타이어 정보 저장 
- `GET /tires`: 로그인한 사용자가 소유한 타이어 정보 조회

### 애플리케이션 구조

애플리케이션에는 사용자, 타이어, 인증에 해당하는 영역이 있으며 각 영역은 아래와 같은 디렉토리로 표현됩니다.

- `users`: 사용자 생성과 같은 사용자 객체의 생애주기가 관리되는 영역
- `tires`: 타이어 정보 생성과 조회에 관련된 기능이 관리되는 영역
- `authenticates`: 로그인, 액세스 토큰 인증과 같은 인증 사항들을 담당하는 영역

그리고 각 영역 내부는 다음과 같은 계층으로 구성되며 기술된 책임을 갖습니다.

- presentation layer: 애플리케이션으로 들어온 요청을 application layer로 전달합니다.
  - `routers.py`: 애플리케이션으로 들어온 요청을 적절한 서비스에 전달합니다. 
- application layer: 도메인 모델을 이용해 들어온 요청을 처리합니다.
  - `services.py`: 전달받은 요청을 비즈니스 로직에 맞게 도메인 모델을 이용해 처리합니다.
  - `unit_of_work.py`: 데이터베이스나 외부 데이터 저장소에 접근할 때 트랜잭션을 관리합니다.
- domain layer: 도메인 규칙대로 행동하는 도메인 모델을 정의합니다.
  - `models.py`: 도메인 모델들을 정의합니다.
- infra layer: 데이터베이스와 같은 세부사항에 대한 인터페이스를 제공하며 데이터베이스에 존재해야할 테이블을 정의합니다.
  - `orm.py`: 데이터베이스의 테이블을 정의하는 클래스를 담고있습니다.
  - `repository.py`: 외부 저장소에 대한 접근을 추상화합니다.

#### 작업 단위: `UnitOfWork`

작업 단위 객체는 application layer에서 데이터베이스에 대한 접근을 관리하는 컨텍스트 매니저입니다.
`with` 키워드와 함께 `__enter__` 메소드를 호출하면 데이터베이스와 연결된 세션을 생성하며 이를 접근하려는 레포지토리 객체에 주입시켜 데이터베이스와의 소통을 보조합니다.
컨텍스트 종료시 `__exit__` 메소드를 호출해 커밋되지 않은 사항들은 `rollback` 시키고 세션을 닫아 트랜잭션을 관리합니다.

#### 레포지토리: `Repository`

레포지토리는 외부 데이터 저장소에 대한 접근을 추상화시켜 애플리케이션이 해당 메소드를 이용해 데이터베이스와 같은 외부 데이터 저장소와 소통할 수 있도록 합니다.

#### 데이터 소스: `DataSource`

역할 자체는 레포지토리와 다르지 않습니다.
타이어의 정보를 가져오기 위해 외부 API를 호출합니다. 그리고 이를 추상화시켜 애플리케이션은 타이어의 정보를 가져올 때 해당 인터페이스를 이용합니다.

### 애플리케이션 구현시 추가된 가정 및 규칙

- 소유자와 차종에 대한 정보가 같은게 들어오면 같은 소유주가 2대의 같은 차종을 가지는 것으로 간주합니다. 그렇기 때문에 중복이 가능하게 만들었습니다.
- 차에 대한 정보를 제공하는 외부 API와 관련된 예외나 에러가 발생하면 Internal Server Error로 간주합니다.

### 존재하는 모델

- `User`: 애플리케이션 사용자 (타이어 정보 생성 및 조회 가능)
- `Tire`: 사용자가 소유한 타이어의 정보를 가지는 객첵
- `TireInfo`: 타이어에 자체에 대한 정보만을 가지는 객체

## 실행환경 설절 방법

> `git`과 `docker`, `docker-compose`가 설치되어 있어야 합니다.

1. 레포지토리 git 클론

    ```bash
    $ git clone https://github.com/joowankim/cardoc-assignment.git
    ```
   
2. 다음과 같은 내용의 `.env` 파일 프로젝트 루트 디렉토리에 생성

    ```.dotenv
    JWT_SECRET=[JWT 생성시 필요한 SECRET KEY]
    JWT_ALGORITHM=[JWT 생성시 필요한 알고리즘 이름]
    TOKEN_TYPE=[JWT의 타입(e.g. Bearer)]
    ``` 

4. 애플리케이션 실행하기

    ```bash
    $ docker-compose up

    # 애플리케이션을 백그라운드에서 실행하고 싶다면
    $ docker-compose up -d
    ```

5. 로컬에서 실행된 애플리케이션에 접근하기

    ```
    http://localhost:8000
    ```

## 8️⃣ 과제 결과물 테스트 및 확인 방법

1. POSTMAN 확인: https://documenter.getpostman.com/view/12446432/UVJZpypz

2. 배포된 서버의 주소

    ```commandline
    http://3.37.127.222:8000
    ```

# 8️⃣ Reference

이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 카닥에서 출제한 과제를 기반으로 만들었습니다.
