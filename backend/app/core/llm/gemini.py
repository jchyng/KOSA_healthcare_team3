"""
LLM 초기화 및 설정
Gemini 또는 OpenAI 중 선택 가능
"""
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()


def get_gemini_llm() -> ChatGoogleGenerativeAI:
    """
    Gemini 2.5 Flash 모델을 초기화하여 반환

    Returns:
        ChatGoogleGenerativeAI 인스턴스

    Raises:
        ValueError: GOOGLE_API_KEY가 설정되지 않은 경우
    """
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key or api_key == "your-gemini-api-key-here":
        raise ValueError(
            "GOOGLE_API_KEY가 설정되지 않았습니다. "
            "backend/.env 파일에 올바른 API 키를 설정해주세요."
        )

    # Gemini 2.5 Flash 모델 초기화
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,  # 응답 창의성 조절 (0.0 ~ 1.0)
        google_api_key=api_key
    )

    return llm


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


def get_llm():
    """
    현재 사용할 LLM 모델 반환
    주석 처리로 Gemini <-> OpenAI 전환 가능
    """
    # === 사용할 LLM 선택 ===
    # OpenAI 사용시: 아래 주석 해제
    return get_openai_llm()

    # Gemini 사용시: 아래 주석 해제 (위 return은 주석 처리)
    # return get_gemini_llm()
