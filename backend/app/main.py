from fastapi import FastAPI
from app.api.v1 import api_v1_router

app = FastAPI(
    title="Healthcare AI Agent API",
    description="병원 탐색 AI 에이전트 API",
    version="1.0.0"
)

# API v1 라우터 등록
app.include_router(api_v1_router, prefix="/api")


@app.get("/")
def read_root():
    """루트 엔드포인트"""
    return {
        "message": "Healthcare AI Agent API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}
