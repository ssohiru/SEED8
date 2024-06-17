import streamlit as st
import openai
import os
from googletrans import Translator

# OpenAI API 키 설정
openai.api_key = st.secrets["openai"]["api_key"]

# 경로 설정
base_path = r'C:/Users/sohi9/OneDrive - 서울공항초등학교/8. SEED'

# 토큰 사용량 추적 변수
if 'token_usage' not in st.session_state:
    st.session_state.token_usage = 0

# 단계별 진행 상태 변수
if 'step' not in st.session_state:
    st.session_state.step = 0

# 선택된 핵심 개념 키워드 변수
if 'selected_keyword' not in st.session_state:
    st.session_state.selected_keyword = None

# 번역기 객체 생성
translator = Translator()

# 페이지 구성 설정
st.set_page_config(
    page_title="2022 교사교육과정 및 학급교육과정 개발 도우미(by. SEED)",
    layout="wide",
)

# 사이드바 설정
st.sidebar.title("2022 교사교육과정 및 학급교육과정 개발 도우미")
st.sidebar.markdown("by. SEED")

# 남은 토큰 수 표시
st.sidebar.markdown(f"남은 GPT-4 토큰 수: {max(0, 4000 - st.session_state.token_usage)}")

# 메인 페이지 제목
st.title("2022 교사교육과정 및 학급교육과정 개발 도우미")
st.markdown("이 어플리케이션은 2022 교사교육과정 및 학급교육과정 개발을 돕기 위해 설계되었습니다.")

# 기본 정보 설정
default_values = {
    "disability_type": ['지적 장애', '자폐성 장애'],
    "school_level": '초등학교',
    "grade": '4학년',
    "subject": '사회',
    "subject_level": '수업 주제와 관련된 간단한 배경지식을 1,2개의 단어로 대답함',
    "student_response": '교사의 질문에 1,2개의 단어로 답하며, 추상적인 사고와 구체적 내용의 답변이 어려움.',
    "core_concept": '사람들은 다양한 사회적 관계를 형성하고 사회적 맥락과 역할에 알맞게 행동한다.',
    "achievement_standard": '[4사회02-03] 학교에서 친구를 아끼고 사이좋게 생활한다.',
    "content_category": '지식&이해: 친구와 사이좋은 학교생활. 과정&기능: 친구 간 사이좋게 지내는 모습 살펴보기. 가치&태도: 친구를 소중히 여기는 마음'
}

# 기본 정보 입력 섹션
if st.session_state.step == 0:
    st.subheader("1. 시작 (Start)")
    st.write('수업에 참여하는 학생들의 기본 정보를 입력하세요.')

    # 장애 유형 목록
    disability_options = [
        '지적 장애', '지체 장애', '시각 장애', '청각 장애', '정서 및 행동 장애', 
        '자폐성 장애', '의사소통 장애', '학습 장애', '건강 장애', 
        '발달 지체', '뇌병변 장애', '간질 장애', '기타 장애'
    ]

    # 학교급 및 학년 선택 옵션
    school_levels = ['초등학교', '중학교', '고등학교']
    elementary_grades = [str(i) + '학년' for i in range(1, 7)]
    middle_high_grades = [str(i) + '학년' for i in range(1, 4)]

    # 교과 선택 옵션
    subjects = [
        '국어', '수학', '영어', '과학', '사회', '음악', 
        '미술', '체육', '도덕', '기술', '가정', '정보'
    ]

    # 사용자 입력 폼
    with st.form(key='start_form'):
        disability_type = st.multiselect('수업에 참여하는 학생들의 장애 유형 (최대 3가지)', disability_options, max_selections=3)
        school_level = st.selectbox('학교급', school_levels)

        if school_level == '초등학교':
            grade = st.selectbox('학년', elementary_grades)
        else:
            grade = st.selectbox('학년', middle_high_grades)

        subject = st.selectbox('수업할 교과', subjects)
        subject_level = st.text_input('교과와 관련한 현재 학습 수행 수준')
        student_response = st.text_input('학생들의 반응 양식 및 표현 양식, 언어 유창성')
        core_concept = st.text_input('교사가 선정한 수업할 핵심개념 또는 핵심개념을 추출할 교육과정 핵심아이디어의 문장')
        achievement_standard = st.text_input('수업할 부분의 관련한 성취기준(코드까지)')
        content_category = st.text_input('수업할 부분의 교육과정 내용체계의 범주(ex: 지식&이해, 과정&기능, 가치&태도)')
        submit_button = st.form_submit_button(label='Submit')

    # 제출 후 처리
    if submit_button:
        st.session_state.step = 1
        st.session_state.disability_type = disability_type
        st.session_state.school_level = school_level
        st.session_state.grade = grade
        st.session_state.subject = subject
        st.session_state.subject_level = subject_level
        st.session_state.student_response = student_response
        st.session_state.core_concept = core_concept
        st.session_state.achievement_standard = achievement_standard
        st.session_state.content_category = content_category

        # GPT-3.5로 핵심 개념을 추출하는 작업 수행
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that assists in designing concept-based curriculum lesson plans tailored for educational settings in Korea."},
                {"role": "user", "content": f"Based on the following information, generate 5 core concepts for the lesson plan:\nDisability Type: {', '.join(disability_type)}\nSchool Level: {school_level}\nGrade: {grade}\nSubject: {subject}\nSubject Level: {subject_level}\nStudent Response and Expression: {student_response}\nCore Concept: {core_concept}\nAchievement Standard: {achievement_standard}\nContent Category: {content_category}"}
            ],
            max_tokens=500
        )
        core_concepts = response['choices'][0]['message']['content']

        # 번역 기능 추가
        translator = Translator()
        translated_core_concepts = translator.translate(core_concepts, src='en', dest='ko').text
        st.session_state.core_concepts = translated_core_concepts.split('\n')
        st.experimental_rerun()

# Step 1: Choose a Core Concept
if st.session_state.step == 1:
    st.subheader("Step 1: 핵심 개념 선택")

    st.write("GPT가 생성한 핵심 개념입니다. 여기서 핵심 개념을 선택하세요:")
    st.write(st.session_state.core_concepts)

    selected_keyword = st.radio('어떤 핵심개념을 선택하시겠습니까?', st.session_state.core_concepts)

    if st.button('Select'):
        st.session_state.selected_keyword = selected_keyword
        st.session_state.step = 2

        # GPT-3.5로 개념적 렌즈를 생성하는 작업 수행
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that assists in designing concept-based curriculum lesson plans tailored for educational settings in Korea."},
                {"role": "user", "content": f"Based on the selected core concept '{selected_keyword}', generate 3 conceptual lenses for the lesson plan."}
            ],
            max_tokens=200
        )
        conceptual_lenses = response['choices'][0]['message']['content']

        # 번역 기능 추가
        translated_conceptual_lenses = translator.translate(conceptual_lenses, src='en', dest='ko').text
        st.session_state.conceptual_lenses = translated_conceptual_lenses.split('\n')
        st.experimental_rerun()

# Step 2: Research Related Keywords and Present Conceptual Lenses
if st.session_state.step == 2:
    st.subheader("Step 2: 개념적 렌즈 선택")

    st.write("GPT가 생성한 개념적 렌즈입니다. 여기서 선택하세요:")
    st.write(st.session_state.conceptual_lenses)

    selected_lens = st.radio('어떤 개념적 렌즈를 선택하시겠습니까?', st.session_state.conceptual_lenses)

    if st.button('Select Lens'):
        st.session_state.selected_lens = selected_lens
        st.session_state.step = 3

        # GPT-3.5로 스트렌드를 생성하는 작업 수행
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that assists in designing concept-based curriculum lesson plans tailored for educational settings in Korea."},
                {"role": "user", "content": f"Based on the conceptual lens '{selected_lens}', create strands for the main theme. Generate:\n1. Three sub-contents related to the achievement standards.\n2. Two generalization methods.\n3. Two guiding questions.\n4. Two critical content knowledge points.\n5. Two core skills.\n6. Evaluation rubrics for levels 3, 2, and 1."}
            ],
            max_tokens=500
        )
        strands = response['choices'][0]['message']['content']

        # 번역 기능 추가
        translated_strands = translator.translate(strands, src='en', dest='ko').text
        st.session_state.strands = translated_strands
        st.experimental_rerun()

# Step 3: Develop Strands
if st.session_state.step == 3:
    st.subheader("Step 3: 스트렌드 개발")
    st.write(st.session_state.strands)

    if st.button('Proceed to Step 4'):
        st.session_state.step = 4
        st.experimental_rerun()

# Step 4: 프로젝트 학습 설계
if st.session_state.step == 4:
    st.subheader("Step 4: 프로젝트 학습 설계")

    # GPT-3.5로 프로젝트 학습 활동과 수업 차시 계획 생성
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that assists in designing concept-based curriculum lesson plans tailored for educational settings in Korea."},
            {"role": "user", "content": f"Based on the strands provided, create a project learning activity and a lesson plan with 4 sessions. Each session should include activities, objectives, achievement standards (provided by the user), and related skills."}
        ],
        max_tokens=500
    )
    project_plan = response['choices'][0]['message']['content']

    # 번역 기능 추가
    translated_project_plan = translator.translate(project_plan, src='en', dest='ko').text
    st.session_state.project_plan = translated_project_plan
    st.write(translated_project_plan)

    selected_session = st.radio('어떤 차시를 선택하시겠습니까?', options=['차시 1', '차시 2', '차시 3', '차시 4'])

    if st.button('Proceed to Step 5'):
        st.session_state.selected_session = selected_session
        st.session_state.step = 5
        st.experimental_rerun()

# Step 5: 상세 수업 계획 설계
if st.session_state.step == 5:
    st.subheader("Step 5: 상세 수업 계획 설계")
    
    # GPT-3.5로 상세 수업 계획 생성
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that assists in designing concept-based curriculum lesson plans tailored for educational settings in Korea."},
            {"role": "user", "content": f"Based on the selected session '{st.session_state.selected_session}', create a detailed lesson plan including:\n1. Lesson objectives.\n2. Lesson activities (Introduction - Development - Conclusion).\n3. EdTech tools to be used.\n4. Evaluation methods.\n5. Recommended teaching materials."}
        ],
        max_tokens=500
    )
    detailed_lesson_plan = response['choices'][0]['message']['content']

    # 번역 기능 추가
    translated_detailed_lesson_plan = translator.translate(detailed_lesson_plan, src='en', dest='ko').text
    st.session_state.detailed_lesson_plan = translated_detailed_lesson_plan
    st.write(translated_detailed_lesson_plan)

# 파일 읽기 예제
st.subheader("파일 읽기 예제")
file_path = os.path.join(base_path, 'example.txt')

if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
        st.text_area("파일 내용:", file_content)
else:
    st.write("example.txt 파일이 지정된 경로에 존재하지 않습니다.")

