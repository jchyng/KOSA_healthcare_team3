"""
채팅 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import process_chat

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post(
    "",
    response_model=ChatResponse,
    summary="채팅 메시지 전송",
    description="사용자 메시지를 AI 에이전트에게 전송하고 응답을 받습니다. 멀티턴 대화를 위해 session_id를 사용합니다."
)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    채팅 메시지 처리 엔드포인트

    Args:
        request: ChatRequest (session_id, message)

    Returns:
        ChatResponse: 에이전트 응답

    Raises:
        HTTPException: 처리 중 오류 발생시
    """
    try:
        response = await process_chat(request)
        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"채팅 처리 중 오류가 발생했습니다: {str(e)}"
        )
