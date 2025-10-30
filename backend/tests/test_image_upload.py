"""
이미지 업로드 API 테스트
"""
import os
import sys
from pathlib import Path
from io import BytesIO
from PIL import Image
import requests

# UTF-8 출력 설정
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# 테스트 설정
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1/images"


def create_test_image(filename: str = "test_image.png", size: tuple = (100, 100)) -> BytesIO:
    """테스트용 이미지 생성"""
    image = Image.new("RGB", size, color="red")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    buffer.name = filename
    return buffer


def test_upload_image():
    """이미지 업로드 테스트"""
    print("=" * 50)
    print("1. 이미지 업로드 테스트")
    print("=" * 50)

    # 테스트 이미지 생성
    test_image = create_test_image("test_upload.png")

    # 이미지 업로드
    files = {"file": ("test_upload.png", test_image, "image/png")}
    response = requests.post(API_URL, files=files)

    print(f"\n상태 코드: {response.status_code}")
    print(f"응답 본문: {response.json()}\n")

    if response.status_code == 200:
        data = response.json()
        print("✅ 이미지 업로드 성공!")
        print(f"  - 이미지 ID: {data['id']}")
        print(f"  - 조회 URL: {BASE_URL}{data['url']}")
        print(f"  - 원본 파일명: {data['original_filename']}")
        return data["id"]
    else:
        print("❌ 이미지 업로드 실패")
        return None


def test_list_images():
    """이미지 목록 조회 테스트"""
    print("=" * 50)
    print("2. 이미지 목록 조회 테스트")
    print("=" * 50)

    response = requests.get(API_URL)

    print(f"\n상태 코드: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print("✅ 이미지 목록 조회 성공!")
        print(f"  - 전체 개수: {data['total']}")
        print(f"  - Limit: {data['limit']}")
        print(f"  - Offset: {data['offset']}")

        if data['images']:
            print("\n  📋 이미지 목록:")
            for img in data['images'][:5]:  # 최대 5개만 표시
                print(f"    - {img['id']}: {img['original_filename']} ({img['file_size']} bytes)")
    else:
        print("❌ 이미지 목록 조회 실패")


def test_get_image(image_id: str):
    """이미지 조회 테스트"""
    print("=" * 50)
    print("3. 이미지 조회 테스트")
    print("=" * 50)

    url = f"{API_URL}/{image_id}"
    response = requests.get(url)

    print(f"\n상태 코드: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type')}")

    if response.status_code == 200:
        print("✅ 이미지 조회 성공!")
        print(f"  - 이미지 크기: {len(response.content)} bytes")
        print(f"  - Content-Type: {response.headers.get('content-type')}")
    else:
        print("❌ 이미지 조회 실패")


def test_delete_image(image_id: str):
    """이미지 삭제 테스트"""
    print("=" * 50)
    print("4. 이미지 삭제 테스트")
    print("=" * 50)

    url = f"{API_URL}/{image_id}"
    response = requests.delete(url)

    print(f"\n상태 코드: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print("✅ 이미지 삭제 성공!")
        print(f"  - 메시지: {data['message']}")

        # 삭제 확인
        get_response = requests.get(url)
        if get_response.status_code == 404:
            print("  - ✅ 삭제 확인: 이미지가 존재하지 않음")
        else:
            print("  - ❌ 삭제 확인 실패: 이미지가 여전히 존재함")
    else:
        print("❌ 이미지 삭제 실패")


def main():
    """전체 테스트 실행"""
    print("\n" + "=" * 50)
    print("이미지 API 통합 테스트 시작")
    print("=" * 50 + "\n")

    try:
        # 1. 이미지 업로드
        image_id = test_upload_image()

        if image_id:
            # 2. 이미지 목록 조회
            test_list_images()

            # 3. 이미지 조회
            test_get_image(image_id)

            # 4. 이미지 삭제
            test_delete_image(image_id)

        print("\n" + "=" * 50)
        print("모든 테스트 완료!")
        print("=" * 50 + "\n")

    except requests.exceptions.ConnectionError:
        print("\n❌ 서버 연결 실패!")
        print("백엔드 서버가 http://localhost:8000 에서 실행 중인지 확인하세요.\n")
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}\n")


if __name__ == "__main__":
    main()
