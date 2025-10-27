"""
OpenAI GPT LLM 초기화
"""
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()


def get_openai_llm() -> ChatOpenAI:
    """
    OpenAI GPT-4o mini 모델을 초기화하여 반환

    Returns:
        ChatOpenAI 인스턴스

    Raises:
        ValueError: OPENAI_API_KEY가 설정되지 않은 경우
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key == "your-openai-api-key-here":
        raise ValueError(
            "OPENAI_API_KEY가 설정되지 않았습니다. "
            "backend/.env 파일에 올바른 API 키를 설정해주세요."
        )

    # OpenAI GPT-4o mini 모델 초기화
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,  # 응답 창의성 조절 (0.0 ~ 1.0)
        api_key=api_key
    )

    return llm
