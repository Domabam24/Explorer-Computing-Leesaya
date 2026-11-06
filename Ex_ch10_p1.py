import streamlit as st

st.title("나의 소개 페이지")

st.header("자기소개")
st.text("안녕하세요, 제 이름은 이사야입니다.")
st.markdown("저는 **게임 개발**과 *AI 사용*에 관심이 있습니다.")

st.subheader("좋아하는 것")
st.write("저는 재밌는 게임과 맛있는 음식을 좋아합니다.")
st.markdown("가장 자주 방문하는 사이트는 claude.ai (클로드ai 사이트)입니다.")

st.subheader("앞으로의 목표")
st.write("앞으로 다양한 프로젝트를 진행하면서 게임 개발에 대한 지식과 실력을 키우고 싶습니다.")

st.caption("제가 좋아하는 파이썬 코드 예시")
st.code("""import random

dice = random.randint(1, 6)
print(f"🎲 주사위 결과: {dice}")""", language="python")

st.caption("피타고라스 정리")
st.latex(r"a^2 + b^2 = c^2")
