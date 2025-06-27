import streamlit as st
import pandas as pd
import random

# CSV 불러오기
df = pd.read_csv("vocab_output_sample5_final.csv")
df = df.dropna(subset=["Word"])

# 페이지 선택
st.title("📚 GMAT & IELTS 단어 암기 앱")
section = st.sidebar.radio("📂 모드 선택", ["1. 단어장", "2. 복습 모드", "3. 테스트 모드"])

# -------------------------
# 1. 단어장 (뜻 가리기)
# -------------------------
if section == "1. 단어장":
    st.header("📘 단어장 (뜻 가리기 모드)")
    query = st.text_input("🔍 단어 검색", "")
    if query:
        filtered_df = df[
            df["Word"].str.contains(query, case=False, na=False) |
            df["korean_definition"].str.contains(query, case=False, na=False)
        ]
    else:
        filtered_df = df
    
    # 단어 카드 반복
    for idx, row in filtered_df.iterrows():
        with st.expander(f"🔤 {row['Word']}"):
            # 뜻 보기 토글
            with st.container():
                st.markdown(f"### 🔤 단어: **{row['Word']}**")

                if st.toggle("🇰🇷 뜻 보기", key=f"korean_{idx}"):
                    st.markdown(f"**🇰🇷 뜻:** {row['korean_definition']}")

                if st.toggle("🇺🇸 영어 정의 보기", key=f"english_{idx}"):
                    st.markdown(f"**🇺🇸 영어 정의:** {row['english_definition']}")

                if st.toggle("📘 해석 보기", key=f"translation_{idx}"):
                    st.markdown(f"**📘 해석:** {row['korean_translation']}")

                if st.toggle("🟢 유의어 보기", key=f"synonyms_{idx}"):
                    st.markdown(f"**🟢 유의어:** {row['synonyms'] or '없음'}")

                if st.toggle("🔴 반의어 보기", key=f"antonyms_{idx}"):
                    st.markdown(f"**🔴 반의어:** {row['antonyms'] or '없음'}")

                if st.toggle("🎯 IELTS 점수 보기", key=f"ielts_{idx}"):
                    st.markdown(f"**🎯 IELTS 점수:** {row['IELTS_score']} / 5")

                if st.toggle("🧠 GMAT 점수 보기", key=f"gmat_{idx}"):
                    st.markdown(f"**🧠 GMAT 점수:** {row['GMAT_score']} / 5")

                st.markdown("---")

            # 기타 정보
            
            st.markdown(f"**📝 예문:** *{row['example_sentence']}*")

# -------------------------
# 2. 복습 모드
# -------------------------
elif section == "2. 복습 모드":
    st.header("🧠 복습 모드 (유의어 / 반의어 중심)")
    for idx, row in df.sample(frac=1).head(10).iterrows():
        st.markdown(f"### 🔤 {row['Word']}")
        st.markdown(f"**🟢 유의어:** {row['synonyms'] or '없음'}")
        st.markdown(f"**🔴 반의어:** {row['antonyms'] or '없음'}")
        st.markdown("---")

# -------------------------
# 3. 테스트 모드
# -------------------------
elif section == "3. 테스트 모드":
    st.header("📝 테스트 모드 (단어 맞히기 퀴즈)")
    num_questions = st.slider("출제 개수", 1, 10, 5)
    quiz_words = df.sample(num_questions).reset_index(drop=True)

    correct = 0
    for i, row in quiz_words.iterrows():
        st.subheader(f"Q{i+1}. 다음 뜻에 맞는 영어 단어는?")
        st.markdown(f"> 🇰🇷 {row['korean_definition']}")
        
        # 보기 만들기
        options = [row["Word"]]
        while len(options) < 4:
            opt = random.choice(df["Word"].tolist())
            if opt not in options:
                options.append(opt)
        random.shuffle(options)

        answer = st.radio("보기 선택", options, key=f"quiz_{i}")
        if st.button(f"정답 확인 (Q{i+1})", key=f"check_{i}"):
            if answer == row["Word"]:
                st.success("✅ 정답입니다!")
                correct += 1
            else:
                st.error(f"❌ 오답입니다. 정답은 **{row['Word']}** 입니다.")

    # 총점
    if st.button("📊 총점 확인"):
        st.info(f"총 {num_questions}문제 중 {correct}개 정답 (정답률 {round((correct/num_questions)*100)}%)")
