import streamlit as st
import pandas as pd

def search_function():
    # 통합된 데이터 불러오기
    file_path = '통합_에듀테크_정리.xlsx
    data = pd.read_excel(file_path)

    # Streamlit 어플리케이션
    st.title("에듀테크 수업 사례 검색기")
    
    # 검색 옵션 선택
    search_option = st.radio("검색 옵션을 선택하세요:", ("과목별 검색", "에듀테크별 검색"))

    if search_option == "과목별 검색":
        subject = st.selectbox("과목을 선택하세요:", data['과목'].unique())
        if st.button("검색"):
            results = data[data['과목'] == subject]
            st.write(f"### '{subject}' 과목의 수업 사례")
            st.dataframe(results)
    
    elif search_option == "에듀테크별 검색":
        edutech = st.selectbox("에듀테크 도구를 선택하세요:", data['에듀테크'].unique())
        if st.button("검색"):
            results = data[data['에듀테크'] == edutech]
            st.write(f"### '{edutech}' 에듀테크 도구의 수업 사례")
            st.dataframe(results)

    # 출처 링크 추가
    st.markdown("### 출처")
    st.markdown("[SEED 2조 한컴 독스](https://www.hancomdocs.com/open?fileId=p6jQp6iFkUCHzRh8bRp2mFEUrNAUyHrQ)")

if __name__ == '__main__':
    search_function()

