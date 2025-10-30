"""
이미지 관련 Pydantic 모델 정의
"""
from pydantic import BaseModel, Field
from datetime import datetime


class ImageMetadata(BaseModel):
    """이미지 메타데이터 스키마"""
    id: str = Field(..., description="이미지 UUID")
    original_filename: str = Field(..., description="원본 파일명")
    file_size: int = Field(..., description="파일 크기 (bytes)")
    created_at: datetime = Field(..., description="업로드 시간")


class ImageUploadResponse(BaseModel):
    """이미지 업로드 응답 스키마"""
    id: str = Field(..., description="이미지 UUID")
    url: str = Field(..., description="이미지 조회 URL")
    original_filename: str = Field(..., description="원본 파일명")
