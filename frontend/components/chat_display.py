import streamlit as st


def display_chat_message(role: str, content: str):
    """
    채팅 메시지 하나를 표시

    Args:
        role: "user" 또는 "assistant"
        avatar: 아바타 이모지(변경 가능)
        content: 메시지 내용
    """
    if role == "user":
        with st.chat_message("user", avatar="👤"):
            st.write(content)
    else:
        with st.chat_message("assistant", avatar="💆"):
            st.write(content)


def display_chat_history(messages: list):
    """
    채팅 히스토리 전체를 표시

    Args:
        messages: [{"role": "user", "content": "..."}, ...] 형태의 메시지 리스트
    """
    for msg in messages:
        display_chat_message(msg["role"], msg["content"])
