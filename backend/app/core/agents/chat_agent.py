"""
채팅 에이전트 구성
LangGraph + MemorySaver를 활용한 멀티턴 대화 에이전트
"""
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from app.core.llm import get_llm
from app.core.tools.hospital_tools import get_hospital_info, search_nearby_hospitals


# MemorySaver 인스턴스 (인메모리 저장)
memory = MemorySaver()


def create_chat_agent():
    """
    LangGraph 기반 채팅 에이전트 생성

    Returns:
        LangGraph 에이전트 (create_react_agent)
    """
    # LLM 초기화 (gemini.py의 get_llm()에서 모델 선택)
    llm = get_llm()

    # 사용할 도구 목록
    tools = [
        get_hospital_info,
        search_nearby_hospitals
    ]

    # LangGraph ReAct 에이전트 생성
    # - MemorySaver를 checkpointer로 사용하여 대화 히스토리 저장
    # - thread_id (session_id)를 기준으로 대화 컨텍스트 관리
    # - 기본 ReAct 프롬프트 사용 (커스텀 프롬프트는 LLM 초기화 시 설정)
    agent = create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=memory
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
