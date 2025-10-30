"""
이미지 관련 Pydantic 모델 정의
"""
from pydantic import BaseModel, Field
from datetime import datetime


class ImageMetadata(BaseModel):
    """이미지 메타데이터 스키마"""
    id: str = Field(..., description="이미지 UUID")
    filename: str = Field(..., description="파일명 (확장자 제외)")
    extension: str = Field(..., description="파일 확장자")
    file_size: int = Field(..., description="파일 크기 (bytes)")
    created_at: datetime = Field(..., description="업로드 시간")


class ImageUploadResponse(BaseModel):
    """이미지 업로드 응답 스키마"""
    id: str = Field(..., description="이미지 UUID")
    url: str = Field(..., description="이미지 조회 URL")
    filename: str = Field(..., description="파일명 (확장자 제외)")
    extension: str = Field(..., description="파일 확장자")
