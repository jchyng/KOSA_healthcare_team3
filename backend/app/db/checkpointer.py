"""
PostgreSQL Checkpointer 관리 (LangGraph 전용)

이 모듈은 LangGraph 에이전트의 대화 히스토리 저장을 위한 PostgresSaver를 관리합니다.
일반적인 데이터베이스 쿼리는 session.py의 get_db()를 사용하세요.
"""
import os
from typing import Optional
from dotenv import load_dotenv
from langgraph.checkpoint.postgres import PostgresSaver
import psycopg
from psycopg_pool import ConnectionPool

# 환경변수 로드
load_dotenv()


def get_checkpointer_database_url() -> str:
    """
    PostgreSQL 연결 문자열 반환 (psycopg 드라이버 사용)

    환경변수에서 DATABASE_URL을 우선 사용하고,
    없으면 개별 필드(DB_HOST, DB_PORT 등)로 구성

    Returns:
        str: PostgreSQL 연결 문자열

    Raises:
        ValueError: 필수 환경변수가 없을 경우
    """
    # 방법 1: DATABASE_URL 직접 사용
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    # 방법 2: 개별 필드로 구성
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    if not all([db_name, db_user, db_password]):
        raise ValueError(
            "데이터베이스 연결 정보가 부족합니다. "
            "DATABASE_URL 또는 DB_NAME, DB_USER, DB_PASSWORD 환경변수를 설정해주세요."
        )

    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


# PostgresSaver 싱글톤 인스턴스
_checkpointer: Optional[PostgresSaver] = None


def get_postgres_checkpointer() -> PostgresSaver:
    """
    PostgresSaver 인스턴스 반환 (싱글톤)

    LangGraph 에이전트의 대화 히스토리를 PostgreSQL에 영구 저장

    Returns:
        PostgresSaver: PostgreSQL 기반 checkpointer

    Raises:
        Exception: DB 연결 실패 시
    """
    global _checkpointer

    if _checkpointer is None:
        try:
            database_url = get_checkpointer_database_url()

            # 연결 풀 생성
            connection_pool = ConnectionPool(
                conninfo=database_url,
                min_size=1,
                max_size=10
            )

            # PostgresSaver 초기화
            _checkpointer = PostgresSaver(connection_pool)

            # 테이블 생성 (이미 존재하면 무시됨)
            _checkpointer.setup()

            print("✅ PostgreSQL checkpointer 초기화 완료")

        except Exception as e:
            print(f"❌ PostgreSQL 연결 실패: {e}")
            raise Exception(
                f"데이터베이스 연결에 실패했습니다: {e}\n"
                "PostgreSQL 서버가 실행 중인지, .env 파일의 연결 정보가 올바른지 확인해주세요."
            )

    return _checkpointer


def close_checkpointer():
    """
    PostgresSaver 연결 종료 (애플리케이션 종료 시 호출)
    """
    global _checkpointer
    if _checkpointer:
        _checkpointer = None
        print("✅ PostgreSQL checkpointer 종료")
