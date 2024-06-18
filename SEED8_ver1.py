import streamlit as st
import openai

def seed_function():
    # OpenAI API 키 설정
    openai.api_key = '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'

    # 세션 상태 초기화
    if 'token_usage' not in st.session_state:
        st.session_state.token_usage = 0

    if 'step' not in st.session_state:
        st.session_state.step = 0

    if 'core_concepts' not in st.session_state:
        st.session_state.core_concepts = []

    if 'selected_core_concept' not in st.session_state:
        st.session_state.selected_core_concept = ""

    if 'conceptual_lenses' not in st.session_state:
        st.session_state.conceptual_lenses = []

    if 'strands' not in st.session_state:
        st.session_state.strands = ""

    if 'project_plan' not in st.session_state:
        st.session_state.project_plan = ""

    if 'selected_session' not in st.session_state:
        st.session_state.selected_session = ""

    if 'detailed_lesson_plan' not in st.session_state:
        st.session_state.detailed_lesson_plan = ""

    # 사이드바 설정
    st.sidebar.title("2022 교사교육과정 및 학급교육과정 개발 도우미")
    st.sidebar.markdown("by. SEED")

    # 남은 토큰 수 표시
    st.sidebar.markdown(f"남은 GPT-3.5 토큰 수: {max(0, 4000 - st.session_state.token_usage)}")

    # 메인 페이지 제목
    st.title("2022 교사교육과정 및 학급교육과정 개발 도우미")

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
                    {"role": "system", "content": "당신은 한국의 교육 환경에 맞춘 개념 기반 교육과정 수업 계획을 설계하는 데 도움을 주는 유용한 조수입니다."},
                    {"role": "user", "content": f"다음 정보를 바탕으로 수업 계획을 위한 5개의 핵심 개념을 간단하게 설명 없이 생성해 주세요:\n장애 유형: {', '.join(disability_type)}\n학교 급: {school_level}\n학년: {grade}\n교과: {subject}\n현재 학습 수행 수준: {subject_level}\n학생들의 반응 양식 및 표현 양식, 언어 유창성: {student_response}\n교사가 선정한 핵심개념: {core_concept}\n성취기준: {achievement_standard}\n교육과정 내용체계의 범주: {content_category}"}
                ],
                max_tokens=500
            )
            core_concepts = response['choices'][0]['message']['content']
            st.session_state.core_concepts = [concept.strip() for concept in core_concepts.split('\n') if concept.strip()]
            st.experimental_rerun()

    # Step 1: Display Core Concepts and Select One
    if st.session_state.step == 1:
        st.subheader("Step 1:핵심 개념 선택")

        st.write("GPT가 생성한 핵심 개념입니다. 여기서 핵심 개념을 선택하세요:")
        st.markdown("<답변>", unsafe_allow_html=True)
        st.markdown(f"<div style='border:1px solid black; padding: 10px;'>{'<br>'.join(st.session_state.core_concepts)}</div>", unsafe_allow_html=True)

        selected_core_concept = st.radio('어떤 핵심개념을 선택하시겠습니까?', st.session_state.core_concepts)

        if st.button('선택'):
            st.session_state.selected_core_concept = selected_core_concept
            st.session_state.step = 2

    # Step 2: Research Related Keywords and Present Conceptual Lenses
    if st.session_state.step == 2:
        st.subheader("Step 2: 개념적 렌즈 선택")

        # GPT-3.5로 개념적 렌즈를 생성하는 작업 수행
        if not st.session_state.conceptual_lenses:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 한국의 교육 환경에 맞춘 개념 기반 교육과정 수업 계획을 설계하는 데 도움을 주는 유용한 조수입니다."},
                    {"role": "user", "content": f"선택한 핵심 개념 '{st.session_state.selected_core_concept}'를 바탕으로 수업 계획을 위한 3개의 개념적 렌즈를 생성해 주세요."}
                ],
                max_tokens=500
            )
            conceptual_lenses = response['choices'][0]['message']['content']
            st.session_state.conceptual_lenses = [lens.strip() for lens in conceptual_lenses.split('\n') if lens.strip()]

        st.write("GPT가 생성한 개념적 렌즈입니다. 여기서 선택하세요:")
        st.markdown("<답변>", unsafe_allow_html=True)
        st.markdown(f"<div style='border:1px solid black; padding: 10px;'>{'<br>'.join(st.session_state.conceptual_lenses)}</div>", unsafe_allow_html=True)
        
        selected_lens = st.radio('어떤 개념적 렌즈를 선택하시겠습니까?', st.session_state.conceptual_lenses)

        if st.button('개념적 렌즈 선택'):
            st.session_state.selected_lens = selected_lens
            st.session_state.step = 3

    # Step 3: Develop Strands and Create Project Learning Plan
    if st.session_state.step == 3:
        st.subheader("Step 3: 스트렌드 개발 및 프로젝트 학습 설계")

        # GPT-3.5로 스트렌드를 생성하는 작업 수행
        if not st.session_state.strands:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 한국의 교육 환경에 맞춘 개념 기반 교육과정 수업 계획을 설계하는 데 도움을 주는 유용한 조수입니다."},
                    {"role": "user", "content": f"선택한 개념적 렌즈 '{st.session_state.selected_lens}'를 바탕으로 다음의 내용을 생성해 주세요:\n1. 성취기준과 관련된 3개의 하위 내용.\n2. 두 가지 일반화 방법.\n3. 두 개의 안내 질문.\n4. 두 가지 핵심 내용 지식 포인트.\n5. 두 가지 핵심 기술.\n6. 3, 2, 1 수준의 평가 루브릭."}
                ],
                max_tokens=2000
            )
            strands = response['choices'][0]['message']['content']
            st.session_state.strands = strands

        st.write("GPT가 생성한 스트렌드입니다:")
        st.markdown(f"<div style='border:1px solid black; padding: 10px;'>{st.session_state.strands}</div>", unsafe_allow_html=True)

        if st.button('다음 단계로 이동'):
            # GPT-3.5로 프로젝트 학습 활동과 수업 차시 계획 생성
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 한국의 교육 환경에 맞춘 개념 기반 교육과정 수업 계획을 설계하는 데 도움을 주는 유용한 조수입니다."},
                    {"role": "user", "content": f"'{st.session_state.strands}'를 바탕으로 프로젝트 학습 활동과 4차시 수업 계획을 생성해 주세요. 각 차시에는 활동, 목표, 성취기준(사용자가 제공한), 관련 기술을 포함해야 합니다."}
                ],
                max_tokens=2000
            )
            project_plan = response['choices'][0]['message']['content']
            st.session_state.project_plan = project_plan
            st.session_state.step = 4
            st.experimental_rerun()

    # Step 4: Display Project Learning Plan
    if st.session_state.step == 4:
        st.subheader("Step 4: 프로젝트 학습 계획")

        st.write("GPT가 생성한 프로젝트 학습 계획입니다. 여기서 각 차시를 선택하세요:")
        st.markdown(f"<div style='border:1px solid black; padding: 10px;'>{st.session_state.project_plan}</div>", unsafe_allow_html=True)

        # 각 차시의 내용을 담은 라디오 옵션 설정
        sessions = st.session_state.project_plan.split("\n\n")  # 각 차시를 구분하는 기준에 따라 수정 필요
        session_options = [f"차시 {i+1}: {session[:100]}..." for i, session in enumerate(sessions)]  # 처음 100자를 미리보기로 표시

        selected_session = st.radio('어떤 차시를 선택하시겠습니까?', session_options)

        if st.button('상세 수업 설계'):
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
                {"role": "system", "content": "당신은 한국의 교육 환경에 맞춘 개념 기반 교육과정 수업 계획을 설계하는 데 도움을 주는 유용한 조수입니다."},
                {"role": "user", "content": f"'{st.session_state.selected_session}'를 바탕으로 상세 수업 계획을 생성해 주세요. 포함할 내용:\n1. 수업 목표\n2. 수업 활동 (도입 - 전개 - 마무리)\n3. 사용할 에듀테크 도구\n4. 평가 방법\n5. 추천 교재"}
            ],
            max_tokens=2000
        )
        detailed_lesson_plan = response['choices'][0]['message']['content']
        st.session_state.detailed_lesson_plan = detailed_lesson_plan
        st.write(detailed_lesson_plan)

if __name__ == '__main__':
    seed_function()
