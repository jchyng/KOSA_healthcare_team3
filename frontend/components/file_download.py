import streamlit as st
from utils.file_utils import (
    create_text_content,
    create_json_content,
    create_csv_content,
    get_filename
)

"""텍스트 다운로드 버튼"""
def download_text_file(data, prefix="data"):
    content = create_text_content(data)
    filename = get_filename(prefix, "txt")

    st.download_button(
        label="TXT 다운로드",
        data=content,
        file_name=filename,
        mime="text/plain"
    )

"""JSON 다운로드 버튼"""
def download_json_file(data, prefix="data"):
    content = create_json_content(data)
    filename = get_filename(prefix, "json")

    st.download_button(
        label="JSON 다운로드",
        data=content,
        file_name=filename,
        mime="application/json"
    )

"""CSV 다운로드 버튼"""
def download_csv_file(data, prefix="data"):
    content = create_csv_content(data)
    filename = get_filename(prefix, "csv")

    st.download_button(
        label="CSV 다운로드",
        data=content.encode('utf-8'),
        file_name=filename,
        mime="text/csv"
    )

"""다중 파일 형식 다운로드 버튼"""
def download_multiple_formats(data, prefix="data"):
    col1, col2, col3 = st.columns(3)

    with col1:
        download_text_file(data, prefix)

    with col2:
        download_json_file(data, prefix)

    with col3:
        download_csv_file(data, prefix)
