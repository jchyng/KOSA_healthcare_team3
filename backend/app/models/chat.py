"""
채팅 관련 Pydantic 모델 정의
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ChatRequest(BaseModel):
    """채팅 요청 스키마"""
    session_id: str = Field(..., description="클라이언트가 관리하는 세션 ID (UUID)")
    message: str = Field(..., description="사용자 메시지")

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "message": "안녕하세요, 근처 병원을 찾고 있어요"
            }
        }


class AgentStep(BaseModel):
    """에이전트 실행 단계 정보"""
    tool_name: Optional[str] = Field(None, description="사용된 도구 이름")
    tool_input: Optional[Dict[str, Any]] = Field(None, description="도구 입력")
    tool_output: Optional[str] = Field(None, description="도구 출력")


class ChatResponse(BaseModel):
    """채팅 응답 스키마"""
    session_id: str = Field(..., description="세션 ID")
    response: str = Field(..., description="에이전트 응답 메시지")
    agent_steps: Optional[List[AgentStep]] = Field(
        default=None,
        description="에이전트가 수행한 단계들 (디버깅용)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "response": "근처 병원을 찾아드리겠습니다. 어떤 진료과를 원하시나요?",
                "agent_steps": [
                    {
                        "tool_name": "get_hospital_info",
                        "tool_input": {"query": "근처 병원"},
                        "tool_output": "서울대학교병원, 아주대학교병원"
                    }
                ]
            }
        }
