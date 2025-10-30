"""
이미지 업로드 및 조회 서비스
"""

import os
import uuid
from pathlib import Path
from io import BytesIO
from PIL import Image
from fastapi import UploadFile, HTTPException
from app.models.image import ImageMetadata
from datetime import datetime
from psycopg import AsyncConnection


def get_upload_dir() -> Path:
    """
    이미지 저장 디렉토리 경로 반환
    시스템 홈 디렉토리의 myhealthmap_uploads/images를 사용
    """
    home_dir = Path.home()
    upload_dir = home_dir / "myhealthmap_uploads" / "images"

    # 디렉토리 생성
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


# 이미지 저장 디렉토리
UPLOAD_DIR = get_upload_dir()


async def save_image(file: UploadFile, db: AsyncConnection) -> ImageMetadata:
    """이미지를 webp 형식으로 변환하여 저장하고 DB에 메타데이터 저장"""
    # 파일 확장자 확인
    allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
    file_ext = Path(file.filename).suffix.lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"지원하지 않는 파일 형식입니다. 허용된 형식: {allowed_extensions}",
        )

    try:
        # UUID 생성 (확장자 없음)
        image_id = str(uuid.uuid4())

        # 파일명과 확장자 분리
        original_path = Path(file.filename)
        filename = original_path.stem  # 확장자 제외한 파일명
        extension = original_path.suffix.lstrip(".")  # 확장자 (점 제거)

        # 파일 읽기
        contents = await file.read()
        file_size = len(contents)

        # PIL로 이미지 열기 (BytesIO 사용)
        image = Image.open(BytesIO(contents))

        # webp 형식으로 저장 (확장자 없이 UUID만 사용)
        output_path = UPLOAD_DIR / image_id
        file_path = image_id  # UUID만 저장 (시스템 독립적)
        image.save(output_path, format="WEBP", quality=85)

        # DB에 메타데이터 저장
        async with db.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO images (id, filename, extension, file_size, file_path, mime_type, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    image_id,
                    filename,
                    extension,
                    file_size,
                    file_path,
                    "image/webp",
                    datetime.now(),
                ),
            )

        # 메타데이터 생성
        metadata = ImageMetadata(
            id=image_id,
            filename=filename,
            extension=extension,
            file_size=file_size,
            created_at=datetime.now(),
        )

        return metadata

    except Exception as e:
        # 에러 발생 시 파일 삭제
        if "output_path" in locals() and output_path.exists():
            output_path.unlink()
        raise HTTPException(
            status_code=500, detail=f"이미지 저장 중 오류가 발생했습니다: {str(e)}"
        )


async def get_image_metadata(image_id: str, db: AsyncConnection) -> dict:
    """DB에서 이미지 메타데이터 조회"""
    async with db.cursor() as cur:
        await cur.execute(
            "SELECT id, filename, extension, file_size, file_path, mime_type, created_at FROM images WHERE id = %s",
            (image_id,),
        )
        row = await cur.fetchone()

        if not row:
            raise HTTPException(
                status_code=404, detail=f"이미지를 찾을 수 없습니다: {image_id}"
            )

        return {
            "id": row[0],
            "filename": row[1],
            "extension": row[2],
            "file_size": row[3],
            "file_path": row[4],
            "mime_type": row[5],
            "created_at": row[6],
        }


async def get_all_images(
    db: AsyncConnection, limit: int = 100, offset: int = 0
) -> list:
    """DB에서 이미지 목록 조회"""
    async with db.cursor() as cur:
        await cur.execute(
            """
            SELECT id, filename, extension, file_size, file_path, mime_type, created_at
            FROM images
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset),
        )
        rows = await cur.fetchall()

        return [
            {
                "id": row[0],
                "filename": row[1],
                "extension": row[2],
                "file_size": row[3],
                "file_path": row[4],
                "mime_type": row[5],
                "created_at": row[6],
            }
            for row in rows
        ]


async def delete_image(image_id: str, db: AsyncConnection) -> None:
    """이미지 파일 및 DB 레코드 삭제"""
    # DB에서 파일 경로 조회
    metadata = await get_image_metadata(image_id, db)

    # 파일 삭제 (UPLOAD_DIR과 UUID 결합)
    file_path = UPLOAD_DIR / metadata["file_path"]
    if file_path.exists():
        file_path.unlink()

    # DB에서 삭제
    async with db.cursor() as cur:
        await cur.execute("DELETE FROM images WHERE id = %s", (image_id,))


def get_image_path(image_id: str) -> Path:
    """이미지 파일 경로 반환 (파일 시스템 기반)"""
    image_path = UPLOAD_DIR / image_id

    if not image_path.exists():
        raise HTTPException(
            status_code=404, detail=f"이미지를 찾을 수 없습니다: {image_id}"
        )

    return image_path
