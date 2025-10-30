"""
API v1 라우터 통합
"""
from fastapi import APIRouter
from app.api.v1.endpoints import chat, image

# API v1 메인 라우터
api_v1_router = APIRouter(prefix="/v1")

# 개별 엔드포인트 라우터 등록
api_v1_router.include_router(chat.router)
api_v1_router.include_router(image.router)
