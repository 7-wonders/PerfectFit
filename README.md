# 📖 맞춤형 자기소개서 웹 README

![readme_mockup2](https://github.com/7-wonders/PerfectFit/blob/develop/banner.png)

<br>

## 프로젝트 소개 🌼

- 사용자의 프로젝트 경험, 일 경험, 직업, 프롬프트 등을 기반하여 자기소개서 및 모의 면접을 생성하는 웹 사이트입니다.
- 문장에 대한 띄어쓰기, 맞춤법 등을 검사 해주는 기능을 제공합니다.
- 각 회사 별 인재상을 추출하고, 회사에 대표적인 직업 5가지를 뽑아 모의 면접 내용을 제공합니다.
- 사용자들은 자신의 자기소개서와 모의 면접을 다른 사람들에게 공개할 수 있습니다.

<br>
## 사용 방법

** 1. Project Root 폴더에 " .env " 파일이 있는지 확인합니다. **
- 만약에 " .env " 파일이 존재하지 않는다면, **dbstjdqls14@naver.com**으로 요청 부탁드립니다.

** 2. Project Root 폴더에 아래의 .pem 확장자의 공개키, 비밀키가 있는지 확인합니다. **
- access_token_private_key.pem
- access_token_public_key.pem
- refrest_token_private_key.pem
- refrest_token_public_key.pem
- 만약에 파일이 존재하지 않는다면, **seungyong20@naver.com**으로 요청 부탁드립니다.

** 3. 필수 라이브러리를 설치합니다. **
- $ pip install -r requirements.txt

** 4. Terminal에서 비동기 작업을 위한 "Celery"를 실행시켜줍니다. **
- $ python -m celery -A tasks worker --loglevel=info -P solo

** 5. Flask 서버를 실행합니다. **
- $ python app.py
- 127.0.0.1:5000/  을 통해 메인페이지로 접속 후, 사용하시면 됩니다.

<br>

## 팀원 구성 👨‍👩‍👦‍👦

<div align="center">

| **윤성빈** | **김승용** | **한정석** | **손민재** | **최영원** | **문건규** | **김민우** |
| :------: |  :------: | :------: | :------: | :------: | :------: | :------: |
| [<img src="https://avatars.githubusercontent.com/u/44765636?v=4" height=150 width=150> <br/> @seungyong](https://github.com/seungyong) | [<img src="https://avatars.githubusercontent.com/u/44765636?v=4" height=150 width=150> <br/> @seungyong](https://github.com/seungyong) | [<img src="https://avatars.githubusercontent.com/u/44765636?v=4" height=150 width=150> <br/> @seungyong](https://github.com/seungyong) | [<img src="https://avatars.githubusercontent.com/u/44765636?v=4" height=150 width=150> <br/> @seungyong](https://github.com/seungyong) | [<img src="https://avatars.githubusercontent.com/u/44765636?v=4" height=150 width=150> <br/> @seungyong](https://github.com/seungyong) | [<img src="https://avatars.githubusercontent.com/u/44765636?v=4" height=150 width=150> <br/> @seungyong](https://github.com/seungyong) | [<img src="https://avatars.githubusercontent.com/u/44765636?v=4" height=150 width=150> <br/> @seungyong](https://github.com/seungyong) |

</div>

<br>

## 1. 개발 환경

- Front-end : <img src="https://img.shields.io/badge/-HTML-E34F26?logo=html5&logoColor=white" alt="HTML" /> <img src="https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black" alt="JavaScript" /> <img src="https://img.shields.io/badge/Material--UI-0081CB?logo=mui&logoColor=white" alt="Material-UI" /> <img src="https://img.shields.io/badge/-Jinja-F1A93E?logo=python&logoColor=white" alt="Jinja" />
- Back-end : <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" alt="Python" /> <img src="https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white" alt="Flask" /> <img src="https://img.shields.io/badge/Celery-37814A?logo=celery&logoColor=white" alt="Celery" /> <img src="https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white" alt="Redis" /> <img src="https://img.shields.io/badge/MariaDB-003545?logo=mariadb&logoColor=white" alt="MariaDB" />
- 버전 및 이슈관리 : <img src="https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white" alt="GitHub" />
- 협업 툴 : <img src="https://img.shields.io/badge/Discord-5865F2?logo=discord&logoColor=white" alt="Discord" /> <img src="https://img.shields.io/badge/Notion-000000?logo=notion&logoColor=white" alt="Notion" />
- 디자인 : <img src="https://img.shields.io/badge/Figma-F24E1E?logo=figma&logoColor=white" alt="Figma" />
<br>

## 2. 개발 참고
### 디자인 (Figma)
[![Figma](https://img.shields.io/badge/Figma-바로가기-F24E1E?style=for-the-badge&logo=figma&logoColor=white)](https://www.figma.com/design/3VTTwIWCoKdmb9rWTyEcVm/PerfectFit?node-id=0-1&t=TImuiEmovI954t5U-1)

### 명세서 및 이슈 관리 (Notion)
[![Notion](https://img.shields.io/badge/Notion-바로가기-000000?style=for-the-badge&logo=notion&logoColor=white)](https://rowan-swift-32e.notion.site/Web-Programming-Project-16711902147648b8a96a3e829acc372b?pvs=4)

### DB ERD
[![ERDCloud](https://img.shields.io/badge/ERDCloud-바로가기-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://www.erdcloud.com/d/ZFToFGg5GvyZwoDJc)
<br>

## 2. 채택한 개발 기술과 브랜치 전략

### Jinja

- HTML + Javascript를 사용하여 웹사이트를 구성합니다.
- Flask와 결합하여 백엔드에서 보낸 데이터를 받아 웹사이트를 동적으로 처리합니다.
    
### Flask

- AI ChatBot의 복잡한 로직을 간편하게 사용하기 위해 사용하였습니다.
- AI 개발에 많이 사용되는 언어로, 추후 LLama3 확장을 고려하여 사용하였습니다.

### Redis
- JWT의 Refresh Token을 관리하기 위해 사용하였습니다.
  - RTR(Refresh Token Rotation) 기법을 사용하기 위해 읽기, 쓰기가 빠른 인메모리 데이터베이스를 채택하였습니다.
- Celery의 작업 정보를 저장 및 결과를 저장하기 위해 사용하였습니다.
  - 작업 정보를 Redis에 저장하여, 비동기로 처리 가능하도록 만들었습니다.
  - 작업 결과물을 Redis에 저장하여, 1일 이내로 정보를 가져올 수 있게 만들었습니다.
 
### Celery
- 자기소개서 단락 생성, 모의 면접 질문 생성 등 오래 걸리는 작업을 백그라운드 단에서 처리하기 위해 사용했습니다.
  - 프론트 단에서는 폴링을 통해 1초마다 주기적으로 AI 작업 완성 여부를 판단합니다.
<br>

### 브랜치 전략
<br>

- 처음에는 Front-end와 Back-end의 브랜치를 격리하는 전략을 사용하였습니다.
  - 각 개인 브랜치는 다음과 같은 명명 규칙을 지정하였습니다.
    - [부모_브랜치명]-[브랜치_생성날짜]-[이름_이니셜]
    - e.g develop-fontend-1209-ksy
- 웹 프로토타입을 만든 후 기능 별로 브랜치 전략을 변경하였습니다.
  - feature : 모든 기능을 총괄하는 브랜치입니다.
  - feature-기능명 : 특정 기능을 총괄하는 브랜치입니다.
  - feature-기능명-[frontend|backend] : 특정 기능에서 특정 파트를 담당하는 브랜치입니다.


초반 브랜치 전략은 다음 링크에서 자세히 확인하실 수 있습니다.
<br /> <br />
[![Notion](https://img.shields.io/badge/Notion-Github_전략-000000?style=for-the-badge&logo=notion&logoColor=white)](https://www.notion.so/Github-5798cdad8ac34b18bd3f0c14e299911d)
<br>

## 3. 프로젝트 구조 (PerfectFit 폴더 기준)

```
├── README.md
├── .env
├── access_token_private_key.pem
├── access_token_public_key.pem
├── refresh_token_private_key.pem
├── refresh_token_public_key.pem
├── requirements.txt
├── app.py
├── tasks.py
├── config
│     ├── config_mysql.py
│     └── config_redis.py
├── constants
│     └── sns_kind.py
├── controllers
│     ├── auth_controller.py
│     ├── resume_controller.py
│     └── interview_controller.py
│                .
│                .
│                .
├── services
│     ├── auth_service.py
│     ├── resume_service.py
│     └── interview_service.py
│                .
│                .
│                .
├── domain
│     └── models
│           ├── __init__.py
│           ├── app_user.py
│           ├── resume.py
│           └── interview.py
│                   .
│                   .
│                   .
├── dto
│     ├── comapny_best
│     │     └── comapny_best.py
│     ├── interview
│     ├── interviews
│     ├── job
│     ├── keyword
│     ├── main
│     ├── occupation
│     ├── project_experience
│     ├── resume
│     ├── resume_draft
│     ├── user
│     ├── work_experience
│     └── validatin_class.py
├── exception
│     ├── custom_exception.py
│     ├── exception_handler.py
│     └── exception_type.py
├── logs
│     ├── output
│     │      ├── auth_controller.log
│     │      └── chat_gpt.log
│     │              .
│     │              .
│     │              .
│     └── log.py
├── middlewares
│     └── auth_middleware.py
├── static
│     ├── css
│     │     ├── error_page.css
│     │     └── resume.css
│     │             .
│     │             .
│     │             .
│     ├── img
│     │     ├── arrow_right.svg
│     │     └── banner.svg
│     │             .
│     │             .
│     │             .
│     ├── js
│     │     ├── footer.js
│     │     └── header.js
│     │             .
│     │             .
│     │             .
│     └── favicon.ico
├── templates
│     ├── components
│     │     ├── header.html
│     │     └── footer.html
│     │             .
│     │             .
│     │             .
│     ├── error_page.html
│     └── index.html
│                .
│                .
│                .
├── utils
│     ├── oauth
│     │     ├── google_oauth_handler.py
│     │     ├── kakao_oauth_handler.py
│     │     ├── naver_oauth_handler.py
│     │     └── oauth_handler.py
│     ├── openai
│     │     └── resume
│     │     │     └── full_resume_strategy.py
│     │     │     └── partial_resume_strategy.py
│     │     │     └── resume_helper.py
│     │     │     └── resume_strategy.py
│     │     └── chatgpt.py
│     ├── age.py
│     ├── model_converter.py
│     └── celery_util.py
│                .
│                .
│                .
```

<br>

## 4. 역할 분담

### 🐷윤성빈
- **팀장**
    - 정기 회의 진행 및 의사 결정을 총괄
    - 팀원 역할 분배
- **Frontend**
    - 페이지 : 필수 정보 입력 (수정), 선택 정보 입력 (수정), 면접 선택, 면접 진행
- **Bakcend**
    - 페이지 : 면접 목록(기업, 직업, 검색), 면접 상세, 면접 진행, 필수 정보 입력, 선택 정보 입력
- **기능**
    - 면접 목록
    - 면접 상세
    - 면접 질문 생성
    - 면접 답변 개선 및 도출
    - 좋아요, 조회수
    - 공개 여부 설정
    - 직군, 직업, 회사 추가
    - 회사 또는 직업에 따른 모의 면접 데이터 생성
    - 사용자 필수 정보 입력 및 선택 정보 입력 수정

<br>
    
### 👻김승용
- **Design**
    - 면접 선택, 작성, 로딩, 공개 모달창, 진행
- **Frontend**
    - 페이지 : 면접 목록 (기업, 직업, 검색), 면접 상세, 필수 정보 입력 (수정), 선택 정보 입력 (수정)
    - 공통 컴포넌트 : 전체적인 CSS 수정
- **Bakcend**
    - 페이지 : 자기소개서 선택, 자기소개서 필수 정보 입력, 자기소개서 로딩, 자기소개서 작성, 자기소개서 목록, 마이페이지, 필수 정보 입력, 선택 정보 입력
    - 공통 컴포넌트 : 로그인
- **기능**
    - 자기소개서 목록
    - 자기소개서 상세
    - 자기소개서 단락 생성
    - 자기소개서 단락에 대한 답변 생성
    - 좋아요, 조회수
    - 공개 여부 설정
    - 자신의 자기소개서, 모의 면접, 내 정보 가져오기
    - 필수 정보 입력
    - 선택 정보 입력
    - 로그인 및 회원가입

<br>

### 😋김민우
- **Bakcend**
    - 페이지 : 마이페이지
- **기능**
    - 사용자 프로필 사진 가져오기
    - 자신의 자기소개서, 모의 면접, 내 정보 가져오기

<br>

### 😎한정석
- **Design**
    - 헤더, 푸터, 메인, 마이페이지, 정보 입력창, 자기소개서
- **Frontend**
    - 페이지 : 자기소개서 선택, 자기소개서 필수 정보 입력, 자기소개서 로딩, 자기소개서 작성, 자기소개서 목록, 마이페이지, 필수 정보 입력, 선택 정보 입력, 로그인
    - 공통 컴포넌트 : 헤더, 푸터
- **기능**
    - 자기소개서 목록
    - 자기소개서 상세
    - 자기소개서 단락 생성
    - 좋아요, 조회수
    - 공개 여부 설정
    - 필수 정보 입력
    - 선택 정보 입력
    - 로그인 및 회원가입

<br>

### 😎최영원
- **Design**
    - 면접 목록, 면접 진행, 면접 상세, 면접 공개창
- **Frontend**
    - 페이지 : 면접 목록(기업, 직업, 검색), 면접 상세, 면접 진행, 면접 로딩
- **기능**
    - 면접 목록
    - 면접 상세
    - 면접 진행
    - 면접 공개 수정
    - 면접 로딩

<br>

### 😎문건규
- **Frontend**
    - 페이지 : 선택 정보, 필수 정보, 맞춤법 검사기
    - 공통 컴포넌트 : 푸터
- **기능**
    - 맞춤법 검사기
    - 필수 정보 입력
    - 선택 정보 입력

<br>

### 🐬손민재

- **데이터 분석**
    - 회사 별 인재상 데이터 전처리 및 저장
    - 직업, 직군 데이터 전처리 및 저장
- **일정관리**
    - 팀원의 전체적인 일정을 조율
- **시각화**
    - 회사 별 인재상 데이터 시각화
    - 직업, 직군 분류 코드 추출 및 시각화
    
<br>

## 5. 개발 기간 및 작업 관리

### 개발 기간

- 전체 개발 기간 : 2024-09-09 ~ 2024-12-09
- UI 구현 : 2024-12-09 ~ 2024-12-01
- 기능 구현 : 2024-12-09 ~ 2024-12-09

<br>

### 작업 관리

- Notion을 통해 API 명세서, 페이지 명세서 등 공통 작업을 작성하였습니다.
- 주간회의를 진행하며 작업 순서와 방향성에 대한 고민을 나누고 회의록을 작성하였습니다.
- 개인별 또는 팀별 일정을 작성하여 마감일을 지켰습니다.
- 오류 보고 및 수정은 Notion의 언급 기능을 사용하여 소통하였습니다.

<br>

## 6. 신경 쓴 부분

- [RTR 기법](https://seungyong20.tistory.com/entry/JWT-Access-Token%EA%B3%BC-Refresh-Token-%EA%B7%B8%EB%A6%AC%EA%B3%A0-RTR-%EA%B8%B0%EB%B2%95%EC%97%90-%EB%8C%80%ED%95%B4%EC%84%9C-%EC%95%8C%EC%95%84%EB%B3%B4%EC%9E%90)

- [PyHanSpell Customizing](https://udangtang-dev.tistory.com/9)

<br>

## 7. 페이지별 기능

### [헤더 포함 메인 페이지 조회]
- 자기소개서 위에 마우스를 올리면 자기소개서 목록과 자기소개서 작성 옵션이 나타납니다.
- AI 모의면접 위에 마우스를 올리면 면접 목록과 모의면접 진행 옵션이 나타납니다
- 메인 페이지에서 자기소개서 목록, 자기소개서 작성, 면접 목록, 모의면접 진행, 맞춤법 검사기 서비스를 선택하여 각 서비스 페이지로 이동할 수 있습니다.
- 자기소개서와 모의면접 목록에서는 저장된 데이터와  해당 데이터의 조회 수와 좋아요 수를 확인할 수 있습니다

| 헤더 포함 메인 페이지 조회 |
|----------|
| ![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%ED%97%A4%EB%8D%94%ED%8F%AC%ED%95%A8%EB%A9%94%EC%9D%B8%ED%8E%98%EC%9D%B4%EC%A7%80%EC%A1%B0%ED%9A%8C.gif) |

<br>

### [로그인]
- 우측 상단에 아이콘을 눌러 로그인을 진행합니다
    - SNS(네이버,구글,카카오) 로그인 기능 구현

- 로그인이 되어 있지 않는 경우: 우측 상단의 아이콘이 비어 있는 상태로 표시됩니다.
- 로그인이 되어 있는 경우 : 우측 상단의 아이콘이 사용자 프로필 이미지로 변경되어 표시됩니다.

| 로그인 |
|----------|
| ![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EB%A1%9C%EA%B7%B8%EC%9D%B81.gif) |

<br>

### [마이페이지-리스트 조회]
- 마이페이지에 들어가면 자신이 작성한 자기소개서 및 모의면접을 확인할 수 있으며, 최초 로그인 시 기입한 필수 정보 및 선택 정보를 조회할 수 있습니다.

| 마이페이지-리스트조회 |
|----------|
|![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EB%A7%88%EC%9D%B4%ED%8E%98%EC%9D%B4%EC%A7%80_%EB%A6%AC%EC%8A%A4%ED%8A%B8%EC%A1%B0%ED%9A%8C.gif)|

<br>

### [마이페이지-정보 수정]
- 마이페이지의 "내 정보" 탭에 들어가면 최초 로그인 시 기입한 필수 정보 및 선택 정보를 조회할 수 있으며, 해당 내용을 "내용 수정하기>" 버튼을 클릭하여 수정할 수 있습니다.

| 마이페이지-정보 수정 |
|----------|
|![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EB%A7%88%EC%9D%B4%ED%8E%98%EC%9D%B4%EC%A7%80_%EC%A0%95%EB%B3%B4%EC%88%98%EC%A0%95.gif)|

<br>

### [핫 자기소개서,모의면접 확인]
- 메인 페이지에서 조회 수가 높은 자기소개서와 모의면접을 확인할 수 있으며 동일한 조회수일 경우, 좋아요가 높으면 메인 페이지에 게시됩니다.
- 더 보기 버튼을 클릭하면 자기소개서와 모의면접 리스트를 확인할 수 있습니다.
- 자기소개서를 선택하면 해당 자기소개서를 자세히 확인할 수 있으며, 모의면접을 선택하면 모의면접 내용과 이에 대한 개선사항을 확인할 수 있습니다.
- (이 서비스는 로그인한 회원만 이용할 수 있습니다.)

| 핫 자기소개서,모의면접 확인 |
|----------|
|![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EB%A9%94%EC%9D%B8%ED%8E%98%EC%9D%B4%EC%A7%80_%ED%95%AB.gif)|

### [메인페이지 자기소개서 이동]
- "자기소개서 작성"을 선택하면, 자기소개서 작성 유형 선택 페이지로 이동합니다.
    - 전체 작성 유형을 선택한 경우에는 정보 입력 페이지로 넘어갑니다.
    - 부분 작성 유형을 선택한 경우에는 자기소개서 입력 페이지로 넘어갑니다.
- (이 서비스는 로그인한 회원만 이용할 수 있습니다.)

| 메인페이지 자기소개서 전체 작성 이동 |
|----------|
| ![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EB%A9%94%EC%9D%B8%ED%8E%98%EC%9D%B4%EC%A7%80_%EC%9E%90%EC%86%8C%EC%84%9C_%EC%A0%84%EC%B2%B4%EC%9D%B4%EB%8F%99.gif) |

| 메인페이지 자기소개서 부분 작성 이동 |
|----------|
| ![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EB%A9%94%EC%9D%B8%ED%8E%98%EC%9D%B4%EC%A7%80_%EC%9E%90%EC%86%8C%EC%84%9C_%EB%B6%80%EB%B6%84%EC%9D%B4%EB%8F%99.gif) |

<br>

### [자기소개서 전체 작성]
- 모든 필드를 입력한 후 다음 버튼을 클릭하면 AI가 자기소개서를 작성하여 전체 작성 페이지에 표시합니다.
    - 이후 사용자는 제목을 수정하고 공개 또는 비공개를 선택한 뒤 저장 버튼을 누르면 작성된 자기소개서를 마이페이지에서 확인할 수 있습니다.
- (이 서비스는 로그인한 회원만 이용할 수 있습니다.)

| 자기소개서 전체 작성 |
|----------|
|![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EC%9E%90%EA%B8%B0%EC%86%8C%EA%B0%9C%EC%84%9C_%EC%A0%84%EC%B2%B4%EC%9E%91%EC%84%B1.gif)|

<br>

### [자기소개서 부분 작성]
- 선택 사항 및 항목에 대한 내용을 제외한 모든 필드를 입력한 후, AI 자기소개서 작성 아이콘을 클릭하면 입력된 내용을 바탕으로 AI가 자기소개서를 작성합니다.
- 휴지통 아이콘을 클릭하면 해당 내용이 삭제되며, 섹션 추가하기 버튼을 누르면 새로운 섹션이 추가됩니다.
- 작성을 완료한 후 공개 또는 비공개를 선택하고 저장 버튼을 누르면 작성된 자기소개서를 마이페이지에서 확인할 수 있습니다.
(이 서비스는 로그인한 회원만 이용할 수 있습니다.)

| 자기소개서 부분 작성 |
|----------|
|![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EC%9E%90%EA%B8%B0%EC%86%8C%EA%B0%9C%EC%84%9C_%EB%B6%80%EB%B6%84%EC%9E%91%EC%84%B1.gif)|

<br>

### [자기소개서 임시 저장]
- 자기소개서를 작성한 뒤 임시 저장 버튼을 클릭하면 작성된 내용이 임시 저장되며, 임시 저장 목록에서 확인할 수 있습니다.
- 임시 저장 목록에 있는 항목의 제목을 클릭하면 임시 저장된 내용을 불러올 수 있습니다.
- 임시 저장된 항목을 불러온 후 수정한 다음, 다시 임시저장을 누르면 임시저장 내용이 수정됩니다.
- (이 서비스는 로그인한 회원만 이용할 수 있습니다.)

| 자기소개서 임시 저장 |
|----------|
|![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EC%9E%90%EA%B8%B0%EC%86%8C%EA%B0%9C%EC%84%9C_%EC%9E%84%EC%8B%9C%EC%A0%80%EC%9E%A5.gif)|

<br>

### [맞춤법 검사기]
- 원문에 300자 이내로 글을 입력한 후 "검사하기"를 누르면 교정된 문구가 표시됩니다.
- 복사 아이콘을 클릭하면 교정된 문구를 클립보드에 복사할 수 있습니다
- (이 서비스는 로그인한 회원만 이용할 수 있습니다.)

| 맞춤법 검사기 |
|----------|
|![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EB%A7%9E%EC%B6%A4%EB%B2%95%EA%B2%80%EC%82%AC%EA%B8%B0.gif)|

<br>

### [메인페이지 모의면접 이동]
- "AI 모의면접"을 선택하면, 자기소개서 기반으로 진행할지, 직무 기반으로 진행할지 선택하는 모의면접 진행 유형 선택 페이지로 이동합니다.
- (이 서비스는 로그인한 회원만 이용할 수 있습니다.)

| 메인페이지 모의면접 자기소개서 기반 이동 |
|----------|
| ![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EB%A9%94%EC%9D%B8%ED%8E%98%EC%9D%B4%EC%A7%80_%EB%A9%B4%EC%A0%91_%EC%9E%90%EA%B8%B0%EC%86%8C%EA%B0%9C%EC%84%9C%EA%B8%B0%EB%B0%98.gif) |

| 메인페이지 모의면접 직무 기반 이동 |
|----------|
| ![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EB%A9%94%EC%9D%B8%ED%8E%98%EC%9D%B4%EC%A7%80_%EB%A9%B4%EC%A0%91_%EC%A7%81%EB%AC%B4%20%EA%B8%B0%EB%B0%98.gif) |

### [모의면접-자기소개서 기반(#1)]
- AI 모의 면접 유형 선택 화면에서 자기소개서 기반 모의 면접을 클릭하면 해당 페이지로 이동합니다.
- 자기소개서 기반 모의 면접 페이지에서는 사용자가 제목을 직접 입력하여 지정할 수 있으며, 지원 경력을 선택한 뒤 원하는 항목을 선택하여 다음 버튼을 눌러 면접을 진행할 수 있습니다.
- (이 서비스는 로그인한 회원만 이용할 수 있습니다.)

| 모의면접-자기소개서 기반(#1) |
|----------|
|![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EB%AA%A8%EC%9D%98%EB%A9%B4%EC%A0%91_%EC%9E%90%EC%86%8C%EC%84%9C%EA%B8%B0%EB%B0%98_1.gif)|

<br>

### [모의면접-자기소개서 기반(#2)]
- 10개의 면접 질문 개수가 표기되며, 각 질문에 대해 답변을 작성할 수 있는 시간이 1분 주어집니다.
- 1분이 지나면 경고 메시지가 표시되고 자동으로 다음 질문으로 넘어가며, 사용자는 다음 버튼을 눌러 질문을 직접 넘길 수도 있습니다.
- (이 서비스는 로그인한 회원만 이용할 수 있습니다.)

| 모의면접-자기소개서 기반(#2) |
|----------|
|![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EB%AA%A8%EC%9D%98%EB%A9%B4%EC%A0%91_%EC%9E%90%EC%86%8C%EC%84%9C%EA%B8%B0%EB%B0%98_2.gif)|

<br>

### [모의면접-자기소개서 기반(#3)]

- 모든 질문에 대한 답변을 완료하면 공개 여부를 설정하는 모달 화면이 나타납니다.
- 모달 화면에는 공개 여부를 선택할 수 있는 체크란이 표시되며, 체크란을 선택한 후 "공개 안 함", "선택된 항목 공개" 중 하나를 선택할 수 있습니다.
- 선택을 완료하면 개선사항 확인 페이지로 이동하며, 이 페이지에서 "개선사항 확인" 버튼을 누르면 각 질문에 대한 답변의 개선사항을 확인할 수 있습니다.
- (이 서비스는 로그인한 회원만 이용할 수 있습니다.)

| 모의면접-자기소개서 기반(#3) |
|----------|
|![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EB%AA%A8%EC%9D%98%EB%A9%B4%EC%A0%91_%EC%9E%90%EC%86%8C%EC%84%9C%EA%B8%B0%EB%B0%98_3.gif)|

<br>

### [모의면접-직무 기반(#1)]

- AI 모의 면접 유형 선택 화면에서 직무 기반 모의 면접을 클릭하면 해당 페이지로 이동합니다.
- 직무 기반 모의 면접 페이지에서는 사용자가 제목을 직접 입력하여 지정할 수 있으며, 지원 경력을 선택한 뒤 원하는 직군과 직무를 선택한 뒤 다음 버튼을 눌러 면접을 진행할 수 있습니다.
- (이 서비스는 로그인한 회원만 이용할 수 있습니다.)

| 모의면접-직무 기반(#1) |
|----------|
|![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EB%AA%A8%EC%9D%98%EB%A9%B4%EC%A0%91_%EC%A7%81%EB%AC%B4%EA%B8%B0%EB%B0%98_1.gif)|

<br>

### [모의면접-직무 기반(#2)]

- 10개의 면접 질문 개수가 표기되며, 각 질문에 대해 답변을 작성할 수 있는 시간이 3분 주어집니다.
- 1분이 지나면 경고 메시지가 표시되고 자동으로 다음 질문으로 넘어가며, 사용자는 다음 버튼을 눌러 질문을 직접 넘길 수도 있습니다.
- (이 서비스는 로그인한 회원만 이용할 수 있습니다.)

| 모의면접-직무 기반(#2) |
|----------|
|![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EB%AA%A8%EC%9D%98%EB%A9%B4%EC%A0%91_%EC%A7%81%EB%AC%B4%EA%B8%B0%EB%B0%98_2_%EC%88%98%ED%96%89.gif)|

<br>

### [모의면접-직무 기반(#3)]

- 모든 질문에 대한 답변을 완료하면 공개 여부를 설정하는 모달 화면이 나타납니다.
- 모달 화면에는 공개 여부를 선택할 수 있는 체크란이 표시되며, 체크란을 선택한 후 "공개 안 함", "선택된 항목 공개" 중 하나를 선택할 수 있습니다.
- 선택을 완료하면 개선사항 확인 페이지로 이동하며, 이 페이지에서 "개선사항 확인" 버튼을 누르면 각 질문에 대한 답변의 개선사항을 확인할 수 있습니다.
- (이 서비스는 로그인한 회원만 이용할 수 있습니다.)

| 모의면접-직무 기반(#3) |
|----------|
|![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EB%AA%A8%EC%9D%98%EB%A9%B4%EC%A0%91_%EC%A7%81%EB%AC%B4%EA%B8%B0%EB%B0%98_3.gif)|

<br>

### [모의면접 목록]

- 모의면접 목록 페이지에 들어가면 기업별, 지원분야별로 모의면접을 검색할 수 있으며, 내용 검색을 통해 사용자가 원하는 모의면접을 검색할 수 있습니다.
- 모의면접을 클릭하면 해당 모의면접 상세 페이지로 들어가며, 모의면접 내용과 이에 대한 개선사항을 확인할 수 있습니다.

| 모의면접 목록 |
|----------|
|![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EB%AA%A8%EC%9D%98%EB%A9%B4%EC%A0%91_%EB%AA%A9%EB%A1%9D.gif)|

<br>

### [자기소개서, 모의면접 -조회수 및 좋아요]
- 자기소개서와 모의면접 상세 페이지에 들어가면 좋아요를 누를 수 있으며, 기존 좋아요 상태와 조회수를 확인할 수도 있습니다.

| 자기소개서, 모의면접 -조회수 및 좋아요 |
|----------|
|![splash](https://github.com/7-wonders/PerfectFit/blob/develop/video/%EB%A7%88%EC%9D%B4%ED%8E%98%EC%9D%B4%EC%A7%80_%EC%A1%B0%ED%9A%8C%EC%88%98%EB%B0%8F%EC%A2%8B%EC%95%84%EC%9A%94.gif)|

<br>

## 8. 개선 목표

- Chat GPT 프롬프트를 조정하여 답변의 질을 올리고, LAG를 통해 자기소개서에 특화된 모델을 구축해야 합니다.
- Chat GPT만 사용하는 것이 아닌 Llama 3를 적용하여 모델을 선택할 수 있게 변경하는 것이 목표입니다.
- SQLAlchemy를 통해 쿼리 최적화를 하는 것이 목표입니다.
    - 현재, for 문 안에 CRUD를 무분별하게 돌리는 문제가 있어 성능 저하를 초래하고 있습니다.
    - join, query delete를 통해 성능 최적화에 초점을 두어야 합니다.
- CSS 통합, Scss를 이용한 클래스 간의 간섭을 최소화해야 합니다.
- 각 UI 별 Component를 선별하여, 재사용이 가능한 UI로 변경해야 합니다.
- flash를 통한 오류 메시지를 보여줘야 하며, 페이지를 그리는 함수에서는 오류 발생 보단 flash를 적극 사용해야 합니다.
