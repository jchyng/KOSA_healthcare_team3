#!/usr/bin/env python3
"""
PostgreSQL 기반 대화 영구 저장 테스트 스크립트

사용법:
    python scripts/test_persistent_chat.py
"""
import requests
import uuid
import time

BASE_URL = "http://localhost:8000/api/v1/chat"

def send_message(session_id: str, message: str):
    """메시지 전송 및 응답 출력"""
    print(f"\n👤 사용자: {message}")

    try:
        response = requests.post(
            BASE_URL,
            json={"session_id": session_id, "message": message},
            timeout=30
        )
        response.raise_for_status()

        result = response.json()
        print(f"🤖 AI: {result['response']}")

        # 디버깅: 도구 사용 이력 출력
        if result.get('agent_steps'):
            print(f"🔧 사용된 도구: {[step['tool_name'] for step in result['agent_steps']]}")

        return result

    except requests.exceptions.ConnectionError:
        print("❌ 서버 연결 실패. 서버가 실행 중인지 확인해주세요.")
        print("   실행 명령: bash scripts/run_backend.sh")
        exit(1)
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        exit(1)


def test_multiturn_conversation():
    """멀티턴 대화 테스트 (같은 세션)"""
    print("\n" + "="*60)
    print("🧪 테스트 1: 멀티턴 대화 (같은 세션)")
    print("="*60)

    session_id = str(uuid.uuid4())
    print(f"📝 세션 ID: {session_id}")

    # 첫 번째 대화
    send_message(session_id, "안녕하세요")

    # 두 번째 대화 (컨텍스트 기억 확인)
    send_message(session_id, "방금 내가 뭐라고 했지?")

    # 세 번째 대화 (병원 정보 요청)
    send_message(session_id, "서울대병원 정보 알려줘")

    # 네 번째 대화 (이전 병원 정보 기억 확인)
    send_message(session_id, "방금 말한 병원 전화번호가 뭐였지?")

    return session_id


def test_new_session():
    """새로운 세션 테스트 (컨텍스트 없음)"""
    print("\n" + "="*60)
    print("🧪 테스트 2: 새로운 세션 (컨텍스트 없음)")
    print("="*60)

    new_session_id = str(uuid.uuid4())
    print(f"📝 세션 ID: {new_session_id}")

    # 이전 대화 내용을 알 수 없어야 함
    send_message(new_session_id, "방금 내가 뭐라고 했지?")


def test_session_persistence(original_session_id: str):
    """세션 영구 저장 테스트 (서버 재시작 시뮬레이션)"""
    print("\n" + "="*60)
    print("🧪 테스트 3: 세션 영구 저장 확인")
    print("="*60)

    print(f"📝 원래 세션 ID: {original_session_id}")
    print("⏱️  잠시 대기... (DB 저장 확인)")
    time.sleep(2)

    # 같은 세션 ID로 재접속
    print("\n🔄 같은 세션 ID로 재접속...")
    send_message(original_session_id, "우리가 처음에 무슨 이야기를 했지?")
    send_message(original_session_id, "서울대병원 정보를 물어봤었는데 기억해?")


def main():
    """메인 테스트 실행"""
    print("\n" + "🏥 Healthcare AI Agent - PostgreSQL 대화 영구 저장 테스트")
    print("=" * 60)

    # 서버 연결 확인
    try:
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ 서버 연결 성공")
        else:
            print("❌ 서버 응답 오류")
            exit(1)
    except:
        print("❌ 서버에 연결할 수 없습니다.")
        print("   실행 명령: bash scripts/run_backend.sh")
        exit(1)

    # 테스트 실행
    original_session_id = test_multiturn_conversation()
    test_new_session()
    test_session_persistence(original_session_id)

    print("\n" + "="*60)
    print("✅ 모든 테스트 완료!")
    print("="*60)
    print("\n💡 수동 테스트 방법:")
    print("   1. 서버 재시작: Ctrl+C 후 bash scripts/run_backend.sh")
    print(f"   2. 같은 세션 ID로 테스트: session_id={original_session_id}")
    print("   3. 이전 대화 내용을 기억하는지 확인")


if __name__ == "__main__":
    main()
