import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score


@st.cache_data
def load_data():
    df = pd.read_csv("./data/cars.csv")
    # continent 값의 앞 공백과 끝의 마침표 제거 (" US." -> "US")
    df["continent"] = df["continent"].str.strip().str.rstrip(".")
    return df


def cars_home():
    # 자동차 연비 대시보드의 주요 목적과 활용 포인트를 소개한다.
    st.title("🚗 자동차 연비 분석 대시보드")

    st.write("""
    이 대시보드는 자동차 성능 데이터를 기반으로
    **대륙별 평균 연비, 마력(hp)과 연비(mpg) 관계, 차량 무게와 연비 관계, 연도별 평균 연비 변화**등을 시각화합니다.
    """)

    st.markdown("---")

    st.subheader("📊 주요 기능")
    st.markdown("""
    1. **탐색적 자료분석 (EDA)**
       - 제조 대륙별 평균 연비 비교, 마력과 차량 무게 대비 연비 분포, 연도별 연비 변화 등을 시각화합니다.
       - 그래프를 통해 데이터를 직관적으로 확인할 수 있습니다.

    2. **연비 예측**
       - 차량의 제원(`hp`, `weightlbs`, `cubicinches`, `cylinders`)을 입력하면
         머신러닝 모델이 예상 연비를 예측합니다.

    3. **실시간 인터랙티브 시각화**
       - 슬라이더, 드롭다운 등 Streamlit 위젯을 활용하여
         조건을 바꾸면 그래프가 **즉시 업데이트**됩니다.
    """)

    st.markdown("---")

    st.subheader("💡 활용 포인트")
    st.info("""
    - 데이터를 시각화하며 **연비에 영향을 주는 변수**를 탐색할 수 있습니다.
    - 사용자가 직접 조건을 조정하면서 **예상 연비 모델의 반응**을 실시간으로 확인할 수 있습니다.
    - Streamlit을 활용해 **웹 기반 데이터 분석 대시보드** 제작을 체험할 수 있습니다.
    """)

    st.markdown("---")

    st.caption("📁 데이터 출처: Kaggle - Auto MPG Dataset")


def cars_EDA(df):
    # 연비(mpg)와 주요 변수 간의 관계, 대륙별 특성, 연도별 변화 등을 시각적으로 분석한다.
    st.title("🔍 자동차 연비 분석 (EDA)")

    st.write("""
    이 탭에서는 자동차 성능 데이터를 활용하여
    **연비(mpg)와 주요 변수들 간의 관계, 대륙별 특성, 연도별 변화** 등을 탐색합니다.
    """)

    # ------------------------------------------------------------
    # [추가 기능 1] 사이드바 필터: 대륙과 연도 범위를 골라서 분석
    # ------------------------------------------------------------
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔎 데이터 필터")
    continents = sorted(df["continent"].unique())
    selected_continents = st.sidebar.multiselect("제조 대륙", continents, default=continents)
    year_min, year_max = int(df["year"].min()), int(df["year"].max())
    year_range = st.sidebar.slider("연도 범위", year_min, year_max, (year_min, year_max))

    df = df[
        df["continent"].isin(selected_continents)
        & df["year"].between(year_range[0], year_range[1])
    ]

    if df.empty:
        st.warning("선택한 조건에 맞는 데이터가 없습니다. 필터를 다시 선택해 주세요.")
        return

    # ------------------------------------------------------------
    # [추가 기능 2] 핵심 지표 요약 카드
    # ------------------------------------------------------------
    st.subheader("📌 핵심 지표 요약")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("차량 수", f"{len(df)}대")
    col2.metric("평균 연비", f"{df['mpg'].mean():.1f} mpg")
    col3.metric("평균 마력", f"{df['hp'].mean():.0f} hp")
    col4.metric("평균 무게", f"{df['weightlbs'].mean():,.0f} lbs")

    st.markdown("---")

    # 데이터 미리보기
    st.subheader("📄 데이터 미리보기")
    st.dataframe(df.head())

    st.markdown("---")

    # 🚀 해보기 1: 대륙별 평균 연비
    st.subheader("🌏 대륙별 평균 연비")
    continent_mpg = df.groupby("continent")["mpg"].mean().reset_index()
    fig1 = px.bar(
        continent_mpg,
        x="continent",
        y="mpg",
        color="mpg",
        title="대륙별 평균 연비",
        color_continuous_scale="Greens"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.info("""
    💡 **분석 포인트**
    - 대륙별로 차량 특성이 다르며, 미국 차량은 비교적 연비가 낮고 일본 차량은 연비가 높은 편입니다.
    """)

    st.markdown("---")

    # 🚀 해보기 2: 마력(hp)과 연비(mpg) 관계
    st.subheader("⚡ 마력(hp)과 연비(mpg) 관계")
    fig2 = px.scatter(
        df,
        x="hp",
        y="mpg",
        color="continent",
        size="weightlbs",
        hover_name="continent",
        title="마력 대비 연비 산점도"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.info("""
    💡 **분석 포인트**
    - 마력이 높을수록 연비가 낮아지는 경향이 있습니다.""")

    st.markdown("---")

    # 🚀 해보기 2: 차량 무게와 연비 관계
    st.subheader("⚖️ 차량 무게(weightlbs)와 연비 관계")
    fig3 = px.scatter(
        df,
        x="weightlbs",
        y="mpg",
        color="continent",
        size="hp",
        hover_name="continent",
        title="차량 무게 대비 연비 산점도"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.info("""
    💡 **분석 포인트**
    - 차량 무게가 무거울수록 연비가 낮아지는 경향이 있습니다.""")

    st.markdown("---")

    # 🚀 해보기 2: 연도별 평균 연비 변화
    st.subheader("📆 연도별 평균 연비 변화")
    year_mpg = df.groupby("year")["mpg"].mean().reset_index()
    fig4 = px.line(
        year_mpg,
        x="year",
        y="mpg",
        title="연도별 평균 연비 추이",
        markers=True
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.info("""
    💡 **분석 포인트**
    - 연도별 평균 연비가 점차 개선되는 추세를 확인할 수 있습니다.""")

    st.markdown("---")

    # ------------------------------------------------------------
    # [추가 기능 3] 변수 간 상관관계 히트맵
    # ------------------------------------------------------------
    st.subheader("🧩 변수 간 상관관계 히트맵")
    num_cols = ["mpg", "cylinders", "cubicinches", "hp", "weightlbs", "time-to-60", "year"]
    corr = df[num_cols].corr().round(2)
    fig5 = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="변수 간 상관계수"
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.info("""
    💡 **분석 포인트**
    - 1에 가까우면 함께 커지고, -1에 가까우면 하나가 커질 때 다른 하나는 작아집니다.
    - 연비(mpg)는 무게·배기량·실린더 수·마력과 강한 음의 상관관계를 보입니다.""")


def cars_predict(df):
    # 머신러닝 모델을 활용하여 자동차의 연비를 예측하는 기능을 구현한다.
    st.header("🤖 자동차 연비 예측")
    st.write("선형회귀(Linear Regression) 모델을 활용하여 자동차의 연비(mpg)를 예측합니다.")

    # 입력 변수(X)와 목표 변수(y) 설정
    X = df[["cylinders", "cubicinches", "hp", "weightlbs", "time-to-60"]]
    y = df["mpg"]

    # 학습 데이터와 테스트 데이터 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 모델 학습
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 예측 성능 표시
    y_pred = model.predict(X_test)
    score = r2_score(y_test, y_pred)
    st.write(f"📊 모델 성능 (R²): **{score:.3f}**")

    # 사용자 입력
    st.subheader("🚗 자동차 정보 입력")
    cylinders = st.slider("실린더 수 (cylinders)", 3, 12, 6)
    cubicinches = st.slider("배기량 (cubicinches)", 60, 500, 200)
    hp = st.slider("마력 (horsepower)", 50, 400, 150)
    weightlbs = st.slider("무게 (weightlbs)", 1500, 6000, 3000)
    time_to_60 = st.slider("시속 60마일 도달 시간 (초)", 4.0, 20.0, 10.0)

    # 입력값으로 예측 수행
    input_data = pd.DataFrame({
        "cylinders": [cylinders],
        "cubicinches": [cubicinches],
        "hp": [hp],
        "weightlbs": [weightlbs],
        "time-to-60": [time_to_60]
    })

    mpg_pred = model.predict(input_data)[0]
    st.success(f"예상 연비: **{mpg_pred:.2f} mpg** 🚘")


def main():
    st.set_page_config(page_title="자동차 연비 대시보드", layout="wide")

    df = load_data()

    # --- 사이드바 메뉴 ---
    menu = st.sidebar.radio(
        "대시보드 메뉴",
        ["홈", "탐색적 자료분석(EDA)", "연비 예측"]
    )

    # --- 홈 화면 ---
    if menu == "홈":
        cars_home()

    # --- 탐색적 자료분석 화면 ---
    elif menu == "탐색적 자료분석(EDA)":
        cars_EDA(df)

    # --- 연비 예측 화면 ---
    elif menu == "연비 예측":
        cars_predict(df)


if __name__ == "__main__":
    main()
