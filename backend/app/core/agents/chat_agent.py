"""
채팅 에이전트 구성
LangGraph + PostgresSaver를 활용한 멀티턴 대화 에이전트
"""
from langgraph.prebuilt import create_react_agent
from app.core.llm import get_llm
from app.db import get_postgres_checkpointer
from app.core.tools.hospital_tools import get_hospital_info, search_nearby_hospitals


def create_chat_agent():
    """
    LangGraph 기반 채팅 에이전트 생성

    Returns:
        LangGraph 에이전트 (create_react_agent)
    """
    # LLM 초기화
    llm = get_llm()

    # 사용할 도구 목록
    tools = [
        get_hospital_info,
        search_nearby_hospitals
    ]

    # PostgreSQL 기반 checkpointer 가져오기
    checkpointer = get_postgres_checkpointer()

    # LangGraph ReAct 에이전트 생성 (PostgresSaver로 대화 히스토리 영구 저장)
    agent = create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=checkpointer
    )

    return agent


# 싱글톤 패턴으로 에이전트 인스턴스 관리
_agent_instance = None


def get_chat_agent():
    """
    채팅 에이전트 인스턴스를 반환 (싱글톤)

    Returns:
        LangGraph 에이전트
    """
    global _agent_instance

    if _agent_instance is None:
        _agent_instance = create_chat_agent()

    return _agent_instance
