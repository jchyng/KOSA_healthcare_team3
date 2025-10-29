import streamlit as st
from components.chat_display import display_chat_history
from components.file_download import download_multiple_formats

# 페이지 설정
st.set_page_config(page_title="HealthCare Agent", layout="wide")

# 메인 타이틀
st.title("HealthCare Agent")

# 세션 상태 초기화 (채팅 히스토리 저장)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 히스토리 표시
display_chat_history(st.session_state.messages)

# 사용자 입력
if prompt := st.chat_input("증상을 입력하세요"):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI 응답 (임시)
    ai_response = "백엔드 연동 후 AI 분석 결과가 여기에 표시됩니다."
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    # 페이지 새로고침으로 메시지 표시
    st.rerun()

# 사이드바: 파일 다운로드 기능
with st.sidebar:
    st.header("데이터 다운로드")

    # 더미 데이터 생성
    dummy_data = [
        {"증상": "두통", "날짜": "2025-01-15", "강도": "중간"},
        {"증상": "발열", "날짜": "2025-01-16", "강도": "높음"},
        {"증상": "기침", "날짜": "2025-01-17", "강도": "낮음"}
    ]

    # 다운로드 버튼 표시
    download_multiple_formats(dummy_data, prefix="health_data")
