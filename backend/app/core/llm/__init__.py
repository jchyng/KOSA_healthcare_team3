"""
LLM 모듈
Gemini와 OpenAI 중 선택하여 사용
"""
from app.core.llm.gemini import get_gemini_llm
from app.core.llm.gpt import get_openai_llm


def get_llm():
    """
    현재 사용할 LLM 모델 반환
    주석 처리로 Gemini <-> OpenAI 전환 가능
    """
    # === 사용할 LLM 선택 ===

    # OpenAI 사용 (테스트용 - 기본값)
    return get_openai_llm()

    # Gemini 사용 (실제 배포용)
    # return get_gemini_llm()


# 외부에서 사용할 함수들 노출
__all__ = [
    "get_llm",
    "get_gemini_llm",
    "get_openai_llm"
]
