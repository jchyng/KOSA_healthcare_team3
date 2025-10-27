# 🌈 Healthcare AI Agent

사용자와 대화를 통해 사용자에게 적합한 병원을 추천해주고, 해당 병원의 정보와 위치, 찾아가는 방법 등에 대한 정보를 제공해주는
병원 탐색 All in One AI Service

<br><br>

## 💻 기술 스택

| 구분         | 기술                                                                                                                         | 설명                            |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| Backend      | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)                              | 비동기 Python 웹 프레임워크     |
| Frontend     | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)                        | 대화형 데이터 대시보드          |
| AI Framework | ![LangChain](https://img.shields.io/badge/LangChain-ffffff?logo=langchain&logoColor=green)                                   | LLM 기반 응용 개발 프레임워크   |
| Database     | ![PostgreSQL](<https://img.shields.io/badge/PostgreSQL%20(pgvector%2017)-336791?style=flat&logo=postgresql&logoColor=white>) | 벡터 임베딩 및 유사도 검색 지원 |

<br><br>

## 🧠 데이터 및 API 활용

| 구분            | 출처 / API                                       | 활용 내용                               |
| --------------- | ------------------------------------------------ | --------------------------------------- |
| 의료 데이터     | **아주대학교병원**                               | 환자 진료 이력 및 임상 데이터 분석      |
| 의료 데이터     | **서울대학교병원**                               | 의료 통계 및 진단 보조 모델 학습        |
| 공공 데이터     | **보건의료빅데이터개방시스템** (기준일: 2025-09) | 전국 병원 정보 및 진료 건수 기반 데이터 |
| 지도 / 위치 API | **KakaoMap API**                                 | 병원 위치 기반 시각화 및 거리 계산      |

<br><br>

## 📁 프로젝트 구조

```
healthcare_ai_agent/
│
├── documents/                        # 프로젝트 문서
├── backend/                          # FastAPI 백엔드 애플리케이션
│   ├── app/
│   │   ├── api/                     # API 레이어 - HTTP 인터페이스
│   │   │   └── v1/                 # API 버전 1
│   │   │       └── endpoints/      # 개별 엔드포인트 모듈
│   │   │
│   │   ├── core/                    # 핵심 비즈니스 로직
│   │   │   ├── agents/             # AI 에이전트 구현 및 오케스트레이션
│   │   │   ├── llm/                # LLM 통합 레이어
│   │   │   └── tools/              # 에이전트 도구 및 유틸리티
│   │   │
│   │   ├── models/                  # Pydantic 모델 (스키마)
│   │   ├── services/                # 비즈니스 로직 서비스
│   │   └── utils/                   # 유틸리티 함수
│   │
│   └── tests/                       # 백엔드 테스트
│
├── frontend/                        # Streamlit 프론트엔드 애플리케이션
│   ├── .streamlit/                 # Streamlit 설정
│   ├── components/                 # 재사용 가능한 UI 컴포넌트
│   ├── pages/                      # 멀티페이지 앱 구조
│   ├── services/                   # 프론트엔드 서비스 레이어
│   └── utils/                      # 프론트엔드 유틸리티
│
├── shared/                          # 백엔드/프론트엔드 공유 코드
└── scripts/                         # 개발 및 유틸리티 스크립트
```

<br><br>

## 🤖 AI 모델 선정

선정 기준: 가장 저렴하면서, 최소한의 성능을 만족시키는 모델

| 역할      | 모델명                 | 입력 토큰 비용 (per 1M) | 출력 토큰 비용 (per 1M) | 비고                                                                                        |
| --------- | ---------------------- | ----------------------- | ----------------------- | ------------------------------------------------------------------------------------------- |
| Agent LLM | Gemini 2.5 Flash-Lite  | **$0.10**               | **$0.40**               | 가장 저렴한 2.5 계열 모델. 고성능 필요 최소화 시 적합 :contentReference[oaicite:5]{index=5} |
| Agent LLM | GPT‑4o mini            | ~$0.15                  | ~$0.60                  | OpenAI 저비용 계열. 텍스트 기반 사용 시 유리 :contentReference[oaicite:7]{index=7}          |
| Agent LLM | Gemini 2.5 Flash       | ~$0.30                  | ~$2.50                  | 성능은 높지만 비용도 증가됨 :contentReference[oaicite:9]{index=9}                           |
| Embedding | text-embedding-3-small | **$0.02**               | ~$0 (사실상 무료)       | 비용 매우 저렴. 대량 임베딩 시 유리 :contentReference[oaicite:10]{index=10}                 |

<br><br>

## 🚀 프로젝트 실행하기

### 1️⃣ 가상환경 생성

```bash
python -m venv .venv
```

### 2️⃣ 가상환경 활성화

```bash
# macOS / Linux
source .venv/bin/activate

# Powershell
.venv\Scripts\Activate.ps1
# CMD
.venv\Scripts\activate.bat
# Gitbash
source .venv/Scripts/activate
```

### 3️⃣ 패키지 설치

```bash
# requirements.txt는 backend, frontend 폴더에 각각 존재함
pip install -r requirements.txt
```

### 4️⃣ 서버 실행

```bash
bash scripts/run_backend.sh
```

<br><br>

## 🧭 개발 규칙

프로젝트의 코드 스타일, 브랜치 전략, 커밋 규칙 등은 아래 문서에서 확인할 수 있습니다.  
➡️ [개발 규칙 바로가기](./docs/DEVELOP_RULES.md)
