import streamlit as st
import SEED8_ver1
import standard
import edutech

st.set_page_config(page_title="2022 교사교육과정 및 학급교육과정 개발 도우미", layout="wide")

def main():
    st.sidebar.title("SEED가 준비한 도움들😄")
    menu = ["도움 설명서", "수업설계 도우미", "성취기준 검색기", "에듀테크 사례 검색기"]
    choice = st.sidebar.selectbox("세가지 선물🎁", menu)

    if choice == "도움 설명서":
        st.subheader("도움 설명서")
        st.write("""
        이 웹 애플리케이션은 2022 교사교육과정 및 학급교육과정 개발 도우미와 성취기준 검색기를 제공합니다.
        
        사이드바에서 원하는 기능을 선택하세요:
        - **수업설계 도우미**: 교사 교육과정 및 학급 교육과정 개발 도우미 기능을 제공합니다.
        - **성취기준 검색기**: 2022 개정 교육과정 성취기준을 검색할 수 있는 기능을 제공합니다.
        - **에듀테크 사례 검색기**: 연구대회 보고서 속 에듀테크 사례를 검색할 수 있는 기능을 제공합니다.
        """)

    elif choice == "수업설계 도우미":
        SEED8_ver1.seed_function()

    elif choice == "성취기준 검색기":
        standard.standard_function()
    
    elif choice == "에듀테크 사례 검색기":
        edutech.search_function()

if __name__ == '__main__':
    main()



