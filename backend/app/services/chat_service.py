"""
채팅 서비스 레이어
에이전트 호출 및 응답 처리 로직
"""
from langchain_core.messages import HumanMessage
from app.core.agents.chat_agent import get_chat_agent
from app.models.chat import ChatRequest, ChatResponse, AgentStep
from typing import List, Optional


async def process_chat(request: ChatRequest) -> ChatResponse:
    """
    사용자 메시지를 처리하고 에이전트 응답 반환

    Args:
        request: 채팅 요청 (session_id, message)

    Returns:
        ChatResponse: 에이전트 응답 (session_id, response, agent_steps)
    """
    # 에이전트 인스턴스 가져오기
    agent = get_chat_agent()

    # 세션 설정 (thread_id = session_id)
    config = {
        "configurable": {
            "thread_id": request.session_id
        }
    }

    # 사용자 메시지를 LangChain 메시지 형식으로 변환
    user_message = HumanMessage(content=request.message)

    try:
        # 에이전트 호출 (동기 방식)
        # LangGraph는 기본적으로 동기 실행
        result = agent.invoke(
            {"messages": [user_message]},
            config=config
        )

        # 응답 메시지 추출
        # result["messages"]는 대화 전체 히스토리를 포함
        # 마지막 메시지가 에이전트의 최신 응답
        ai_response = result["messages"][-1].content

        # 에이전트 실행 단계 추출 (디버깅용)
        agent_steps = _extract_agent_steps(result)

        return ChatResponse(
            session_id=request.session_id,
            response=ai_response,
            agent_steps=agent_steps
        )

    except Exception as e:
        # 에러 발생시 사용자에게 안내 메시지 반환
        return ChatResponse(
            session_id=request.session_id,
            response=f"죄송합니다. 오류가 발생했습니다: {str(e)}",
            agent_steps=None
        )


def _extract_agent_steps(result: dict) -> Optional[List[AgentStep]]:
    """
    에이전트 실행 결과에서 Tool 사용 단계 추출 (디버깅용)

    Args:
        result: 에이전트 실행 결과

    Returns:
        List[AgentStep] 또는 None
    """
    steps = []

    # result["messages"]를 순회하며 Tool 호출 정보 추출
    for message in result.get("messages", []):
        # AIMessage에 tool_calls가 있는 경우
        if hasattr(message, "tool_calls") and message.tool_calls:
            for tool_call in message.tool_calls:
                steps.append(AgentStep(
                    tool_name=tool_call.get("name"),
                    tool_input=tool_call.get("args"),
                    tool_output=None  # Tool 출력은 다음 메시지에서 확인 가능
                ))

    return steps if steps else None
