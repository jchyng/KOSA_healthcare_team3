"""
psycopg3 기반 비동기 세션 관리

LangGraph checkpointer와는 독립적인 연결 풀 관리
향후 일반 데이터베이스 쿼리 실행 시 사용
"""
import os
from typing import AsyncGenerator, Optional
from dotenv import load_dotenv
from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool

# 환경변수 로드
load_dotenv()

# 연결 풀 싱글톤
_connection_pool: Optional[AsyncConnectionPool] = None

async def get_connection_pool() -> AsyncConnectionPool:
    """
    비동기 연결 풀 반환 (싱글톤)

    Returns:
        AsyncConnectionPool: psycopg3 연결 풀

    Raises:
        Exception: DB 연결 실패 시
    """
    global _connection_pool

    if _connection_pool is None:
        try:
            database_url = os.getenv("DATABASE_URL")

            # AsyncConnectionPool 생성
            _connection_pool = AsyncConnectionPool(
                conninfo=database_url,
                min_size=2,
                max_size=10,
                open=False,
            )

            # 연결 풀 열기
            await _connection_pool.open()

            print("✅ psycopg3 연결 풀 초기화 완료")

        except Exception as e:
            print(f"❌ psycopg3 연결 풀 초기화 실패: {e}")
            raise Exception(
                f"데이터베이스 연결에 실패했습니다: {e}\n"
                "PostgreSQL 서버가 실행 중인지, .env 파일의 연결 정보가 올바른지 확인해주세요."
            )

    return _connection_pool


async def get_db() -> AsyncGenerator[AsyncConnection, None]:
    """
    FastAPI 의존성 함수: 비동기 DB 커넥션 제공

    Yields:
        AsyncConnection: 비동기 데이터베이스 커넥션 (자동 커밋/롤백 처리)
    """
    pool = await get_connection_pool()
    async with pool.connection() as conn:
        try:
            yield conn
            await conn.commit()
        except Exception:
            await conn.rollback()
            raise


async def close_db_connections():
    """
    데이터베이스 연결 종료 (애플리케이션 종료 시 호출)
    """
    global _connection_pool

    if _connection_pool:
        await _connection_pool.close()
        _connection_pool = None
        print("✅ psycopg3 연결 풀 종료")
