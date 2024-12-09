# 📖 자기소개서 자동 완성 웹 README

![readme_mockup2](https://github.com/7-wonders/PerfectFit/blob/develop/banner.png)

<br>

## 프로젝트 소개

- 사용자의 프로젝트 경험, 일 경험, 직업, 프롬프트 등을 기반하여 자기소개서 및 모의 면접을 생성하는 웹 사이트입니다.
- 문장에 대한 띄어쓰기, 맞춤법 등을 검사 해주는 기능을 제공합니다.
- 각 회사 별 인재상을 추출하고, 회사에 대표적인 직업 5가지를 뽑아 모의 면접 내용을 제공합니다.
- 사용자들은 자신의 자기소개서와 모의 면접을 다른 사람들에게 공개할 수 있습니다.

<br>

## 팀원 구성

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
    - 페이지 : 자기소개서 선택, 자기소개서 필수 정보 입력, 자기소개서 로딩, 자기소개서 작성, 자기소개서 목록, 마이페이지, 필수 정보 입력, 선택 정보 입력
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
- UI 구현 : 2022-12-09 ~ 2022-12-01
- 기능 구현 : 2022-12-09 ~ 2022-12-09

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

### [초기화면]
- 서비스 접속 초기화면으로 splash 화면이 잠시 나온 뒤 다음 페이지가 나타납니다.
    - 로그인이 되어 있지 않은 경우 : SNS 로그인 페이지
    - 로그인이 되어 있는 경우 : README 홈 화면
- SNS(카카오톡, 구글, 페이스북) 로그인 기능은 구현되어 있지 않습니다.

| 초기화면 |
|----------|
|![splash](https://user-images.githubusercontent.com/112460466/210172920-aef402ed-5aef-4d4a-94b9-2b7147fd8389.gif)|

<br>

### [회원가입]
- 이메일 주소와 비밀번호를 입력하면 입력창에서 바로 유효성 검사가 진행되고 통과하지 못한 경우 각 경고 문구가 입력창 하단에 표시됩니다.
- 이메일 주소의 형식이 유효하지 않거나 이미 가입된 이메일일 경우 또는 비밀번호가 6자 미만일 경우에는 각 입력창 하단에 경구 문구가 나타납니다.
- 작성이 완료된 후, 유효성 검사가 통과된 경우 다음 버튼이 활성화되며, 버튼을 클릭하면 프로필 설정 화면이 나타납니다.

| 회원가입 |
|----------|
|![join](https://user-images.githubusercontent.com/112460466/210173571-490f5beb-5791-4a4a-8c5e-510cdcb5f1fe.gif)|

<br>

### [프로필 설정]
- 회원가입 페이지의 유효성 검사를 통과해야 진입할 수 있습니다.
- 프로필 설정에 필요한 프로필 사진, 사용자 이름, 계정 ID, 소개를 입력받습니다.
- 사용자 이름과 계정 ID는 필수 입력사항입니다.
- 계정 ID에는 형식 및 중복 검사가 진행됩니다.
- 프로필 사진은 등록하지 않을 경우 기본 이미지가 등록됩니다.

| 프로필 설정 |
|----------|
|![setProfile](https://user-images.githubusercontent.com/112460466/210173749-2da6c9af-eb93-4eea-9663-1a03e19299ec.gif)|

<br>

### [로그인]
- 이메일 주소와 비밀번호를 입력하면 입력창에서 바로 유효성 검사가 진행되고 통과하지 못한 경우 각 경고 문구가 입력창 하단에 표시됩니다.
- 이메일 주소의 형식이 유효하지 않거나 비밀번호가 6자 미만일 경우에는 각 입력창 하단에 경구 문구가 나타납니다.
- 작성이 완료된 후, 유효성 검사가 통과된 경우 로그인 버튼이 활성화됩니다.
- 로그인 버튼 클릭 시 이메일 주소 또는 비밀번호가 일치하지 않을 경우에는 경고 문구가 나타나며, 로그인에 성공하면 홈 피드 화면으로 이동합니다.

| 로그인 |
|----------|
|![login](https://user-images.githubusercontent.com/112460466/210177956-c716414e-01c2-4c1e-b1f7-6562b9b7a857.gif)|

<br>

### [로그아웃]
- 상단 의 kebab menu를 클릭 후 나타나는 모달창의 로그아웃 버튼을 클릭하면 확인창이 뜹니다.
- 로그아웃시 로컬 저장소의 토큰 값과 사용자 정보를 삭제하고 초기화면으로 이동합니다.

| 로그아웃 |
|----------|
|![logout](https://user-images.githubusercontent.com/112460466/210178009-11225733-7af5-4b8b-aa1c-fe264af01797.gif)|

<br>

### [상하단 배너]
- 상단 배너 : 각 페이지별로 다른 종류의 버튼을 가지고 있습니다.
    - 뒤로가기 : 브라우저 상에 기록된 이전 페이지로 돌아갑니다.
    - 검색 : 사용자 검색 페이지로 이동합니다.
    - 사용자 이름 : 채팅룸 페이지의 경우 상대방의 사용자 이름을 보여줍니다.
    - kebab menu : 각 페이지 또는 컴포넌트에 따른 하단 모달창을 생성합니다.
        - 상품, 댓글, 게시글 컴포넌트 - 삭제, 수정, 신고하기
        - 사용자 프로필 페이지 - 설정 및 사용자 정보, 로그아웃
- 하단 탭 메뉴 : 홈, 채팅, 게시물 작성, 프로필 아이콘을 클릭하면 각각 홈 피드, 채팅 목록, 게시글 작성 페이지, 내 프로필 페이지로 이동합니다.

| 상하단 배너 |
|----------|
|![tab](https://user-images.githubusercontent.com/112460466/210178028-3185f944-6ac1-468a-94ba-b32cdc5e380e.gif)|

<br>

### [홈 피드]
- 자신이 팔로우 한 유저의 게시글이 최신순으로 보여집니다.
- 팔로우 한 유저가 없거나, 팔로워의 게시글이 없을 경우 검색 버튼이 표시됩니다.
- 게시글의 상단 유저 배너 클릭 시 게시글을 작성한 유저의 프로필 페이지로, 본문 클릭 시 게시글 상세 페이지로 이동합니다.

| 팔로우하는 유저가 없을 때 | 팔로우하는 유저가 있을 때 |
|----------|----------|
|![home0](https://user-images.githubusercontent.com/112460466/210379059-48900aac-3735-45c6-a249-bc9c41b49414.gif)|![home1](https://user-images.githubusercontent.com/112460466/210379110-49153d27-0405-48e6-adfb-62c7818d2f43.gif)|

<br>

### [검색]
- 사용자 이름 혹은 계정 ID로 유저를 검색할 수 있습니다.
- 검색어와 일치하는 단어는 파란색 글씨로 표시됩니다.
- 클릭 시 해당 유저의 프로필 페이지로 진입합니다.

| 검색 |
|----------|
|![search](https://user-images.githubusercontent.com/112460466/210379805-6c8a42c0-0de8-48d3-8f75-cdf0ae5f4fb6.gif)|

<br>

### [프로필]

#### 1. 내 프로필
- 상단 프로필란에 프로필 수정과 상품 등록 버튼이 나타납니다.
- 판매중인 상품란에는 사용자가 판매하는 상품이 등록되며, 판매중인 상품이 없을 경우에는 영역 자체가 나타나지 않습니다.
- 게시글란은 상단의 리스트형과 앨범형 두 개의 버튼을 통해서 나누어 볼 수 있습니다.
    - 리스트형의 경우, 사용자가 작성한 글 내용과 이미지, 좋아요와 댓글의 수를 보여줍니다.
    - 앨범형의 경우, 사용자 게시글 중 이미지가 있는 글만 필터링해 바둑판 배열로 보여줍니다.
- 게시글을 클릭하면 각 게시글의 상세페이지로 이동합니다.

| 리스트형 & 앨범형 게시글 | 팔로잉 & 팔로워 리스트 |
|----------|----------|
|![myProfile](https://user-images.githubusercontent.com/112460466/210380492-40560e0b-c306-4e69-8939-cc3e7dc3d8fe.gif)|![followList](https://user-images.githubusercontent.com/112460466/210380539-d09b0bd7-0b61-4b22-85fa-f75e6bcecb68.gif)|

<br>

#### 2. 타 유저의 프로필
- 버튼을 클릭해 해당 사용자를 팔로우 또는 언팔로우할지 결정할 수 있으며 팔로워 수의 변화가 페이지에 즉시 반영됩니다.

| 팔로우 & 언팔로우 |
|----------|
|![yourProfile](https://user-images.githubusercontent.com/112460466/210380853-04f2d2bd-adab-4786-a8e8-c275ce765071.gif)|

<br>

#### 3. 프로필 수정
- 사용자 프로필 이미지, 이름, 아이디, 소개 중 한 가지를 수정하면 저장 버튼이 활성화됩니다.
- 계정 ID의 유효한 형식 및 중복 검사를 통과하지 못하면 하단에 경고 문구가 나타나며 저장 버튼이 비활성화됩니다.
- 사용자 이름과 소개는 공백으로 시작할 수 없습니다.
- 프로필 수정이 완료되면 내 프로필 페이지로 이동합니다.

| 초기화면 |
|----------|
|![editProfile](https://user-images.githubusercontent.com/112460466/210381212-d67fdf87-b90c-4501-a331-f2a384534941.gif)|

<br>

### [게시글]

#### 1. 게시글 작성
- 글이 입력되거나 사진이 첨부되면 업로드 버튼이 활성화됩니다.
- 최대 세 장까지 이미지 첨부가 가능하며 첨부한 파일을 취소할 수 있습니다.
- 게시글 하단에 업로드 날짜가 표시됩니다.

| 게시글 작성 |
|----------|
|![uploadPost](https://user-images.githubusercontent.com/112460466/210381758-1de5a889-f587-41d2-b200-22c20a970519.gif)|

<br>

#### 2. 게시글 수정 및 삭제
- 자신의 게시글일 경우 모달 버튼을 통해 수정, 삭제가 가능합니다.
- 게시글 삭제 버튼 클릭 시, 게시글을 삭제하고 페이지를 리렌더링하여 삭제된 내용을 페이지에 반영합니다.
- 타 유저의 게시글일 경우 모달 버튼을 통해 신고할 수 있습니다.

| 게시글 수정 & 삭제 |
|----------|
|![editDeletePost](https://user-images.githubusercontent.com/112460466/210382021-da057943-dc21-411e-a1f8-552be0e973bf.gif)|

<br>

#### 3. 좋아요와 댓글
- 좋아요와 댓글 수는 실시간으로 상세 페이지에 반영됩니다.
- 댓글이 몇 분 전에 작성되었는지 표시됩니다.
- 자신의 댓글일 경우 모달 버튼을 통해 삭제가 가능합니다.
- 타 유저의 댓글일 경우 모달 버튼을 통해 신고할 수 있습니다.

| 좋아요 & 댓글 |
|----------|
|![likeComment](https://user-images.githubusercontent.com/112460466/210382217-01d70181-91c3-43db-a1b8-409a612afb1c.gif)|

<br>

### [상품]

#### 1. 상품 등록
- 상품 이미지, 상품명, 가격, 판매 링크를 필수로 입력해야 저장 버튼이 활성화됩니다.
- 상품 가격은 숫자만 입력할 수 있으며, 숫자를 입력하면 자동으로 원 단위로 변환됩니다.
- 상품 가격이 0원일 경우 버튼이 비활성화되며 하단에 경고 문구가 나타납니다.
- 상품명과 판매 링크는 공백으로 시작할 수 없습니다.
- 상품 등록이 완료되면 내 프로필 페이지로 이동합니다.

| 상품 등록 |
|----------|
|![addProduct](https://user-images.githubusercontent.com/112460466/210386068-c6ff2e05-eb64-4abc-b6dc-93bf52b88d3f.gif)|

<br>

#### 2. 상품 수정 및 삭제
- 상품 이미지, 상품명, 가격, 판매 링크 중 한 가지를 수정하면 저장 버튼이 활성화됩니다.
- 상품 수정이 완료되면 내 프로필 페이지로 이동합니다.
- 상품 삭제 버튼 클릭 시, 상품을 삭제하고 페이지를 리렌더링하여 삭제된 내용을 페이지에 반영합니다.

| 상품 수정 & 삭제 |
|----------|
|![editDeleteProduct](https://user-images.githubusercontent.com/112460466/210386311-5fae87a7-745f-47c0-b8e3-fc41c65cb3cb.gif)|

<br>

### [채팅]
- 채팅 목록에서 아직 읽지 않은 채팅에는 좌측 상단의 파란색 알림을 띄워줍니다.
- 채팅방에서 메시지를 입력하거나 파일을 업로드하면 전송 버튼이 활성화됩니다.
- 채팅방에서 우측 상단의 채팅방 나가기 모달 버튼을 통해 채팅 목록 페이지로 이동할 수 있습니다.
- 채팅 메시지 전송 및 수신 기능은 개발 예정입니다.

| 채팅 |
|----------|
|![chat](https://user-images.githubusercontent.com/112460466/210386478-ea4877c5-1728-4872-ab50-a8408ddf6dcd.gif)|

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
