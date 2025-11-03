"""
이미지 API 엔드포인트
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from app.models.image import ImageUploadResponse
from app.services.image_service import (
    save_image,
    get_image_path,
    get_all_images,
    delete_image,
    get_image_metadata
)
from app.db.session import get_db
from psycopg import AsyncConnection

router = APIRouter(
    prefix="/images",
    tags=["images"]
)


@router.post(
    "",
    response_model=ImageUploadResponse,
    summary="이미지 업로드",
    description="이미지 파일을 업로드하고 webp 형식으로 저장합니다."
)
async def upload_image(
    file: UploadFile = File(...),
    db: AsyncConnection = Depends(get_db)
) -> ImageUploadResponse:
    """이미지 업로드 엔드포인트"""
    try:
        # 이미지 저장 (DB 포함)
        metadata = await save_image(file, db)

        # 응답 생성
        return ImageUploadResponse(
            id=metadata.id,
            url=f"/api/v1/images/{metadata.id}",
            filename=metadata.filename,
            extension=metadata.extension
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"이미지 업로드 중 오류가 발생했습니다: {str(e)}"
        )


@router.get(
    "",
    summary="이미지 목록 조회",
    description="업로드된 이미지 목록을 조회합니다."
)
async def list_images(
    limit: int = Query(default=100, ge=1, le=1000, description="조회할 이미지 개수"),
    offset: int = Query(default=0, ge=0, description="건너뛸 이미지 개수"),
    db: AsyncConnection = Depends(get_db)
):
    """이미지 목록 조회 엔드포인트"""
    try:
        images = await get_all_images(db, limit=limit, offset=offset)
        return {
            "total": len(images),
            "limit": limit,
            "offset": offset,
            "images": images
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"이미지 목록 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get(
    "/{image_id}",
    summary="이미지 조회",
    description="UUID로 이미지를 조회합니다."
)
async def get_image(image_id: str):
    """이미지 조회 엔드포인트"""
    try:
        # 이미지 경로 가져오기
        image_path = get_image_path(image_id)

        # 파일 응답 반환 (브라우저에서 바로 표시)
        return FileResponse(
            path=image_path,
            media_type="image/webp"
        )

    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"이미지를 찾을 수 없습니다: {str(e)}"
        )


@router.delete(
    "/{image_id}",
    summary="이미지 삭제",
    description="UUID로 이미지를 삭제합니다."
)
async def delete_image_endpoint(
    image_id: str,
    db: AsyncConnection = Depends(get_db)
):
    """이미지 삭제 엔드포인트"""
    try:
        await delete_image(image_id, db)
        return {"message": f"이미지가 성공적으로 삭제되었습니다: {image_id}"}

    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"이미지 삭제 중 오류가 발생했습니다: {str(e)}"
        )
