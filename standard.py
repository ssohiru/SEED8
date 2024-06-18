import streamlit as st
import pandas as pd

def standard_function():
    
    # Load the provided Excel file
    file_path = '2022_특수교육교육과정(기본+공통)_성취기준_목록.xlsx'

    # Streamlit app setup
    st.title('2022 개정교육과정 성취기준')

    try:
        # Load the Excel file from the specified path
        excel_data = pd.ExcelFile(file_path)

        # Get sheet names excluding '안내'
        sheet_names = [name for name in excel_data.sheet_names if name != '안내']

        # Extract unique subjects from sheet names
        subjects = sorted(set(name[:-1] for name in sheet_names))

        # Sidebar for subject selection
        st.sidebar.title("검색 선택")
        subject_selection = st.sidebar.selectbox('과목을 선택하세요:', subjects)

        if subject_selection:
            st.write(f'## {subject_selection}')        

            # Load and display the "과목이름2" (성취기준)
            sheet_name2 = f'{subject_selection}2'
            if sheet_name2 in sheet_names:
                sheet_data2 = pd.read_excel(file_path, sheet_name=sheet_name2).dropna(how='all').fillna('')
                
                # Extract unique values for '구분' and '학년군'
                if '구분' in sheet_data2.columns and '학년군' in sheet_data2.columns:
                    category_selection = st.sidebar.selectbox('교육과정을 선택하세요:', sheet_data2['구분'].unique())
                    grade_selection = st.sidebar.selectbox('학년군을 선택하세요:', sheet_data2['학년군'].unique())

                    # Filter data based on selections
                    filtered_data = sheet_data2[(sheet_data2['구분'] == category_selection) & (sheet_data2['학년군'] == grade_selection)]
                    st.dataframe(filtered_data)
                else:
                    st.dataframe(sheet_data2)

    except FileNotFoundError:
        st.error(f"파일을 찾을 수 없습니다: {file_path}")


