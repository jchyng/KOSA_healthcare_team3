import streamlit as st

# 페이지 설정
st.set_page_config(page_title="HealthMap", layout="wide")

# 메인 타이틀
st.title("HealthMap")

# 테스트용 입력창
user_input = st.text_input("증상을 입력하세요", placeholder="예: 두통이 심해요")

if user_input:
    st.success(f"입력하신 증상: {user_input}")
    st.info("백엔드 연동 후 AI 분석 결과가 여기에 표시됩니다.")
