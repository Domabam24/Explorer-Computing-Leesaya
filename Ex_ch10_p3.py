import pandas as pd
import pydeck as pdk
import streamlit as st

st.title("✈️ 내가 가보고 싶은 장소")

# 가보고 싶은 장소 데이터 (위도, 경도)
places = pd.DataFrame({
    "장소": ["모스콘 센터 (GDC 개최지)", "아키하바라", "닌텐도 본사", "에펠탑", "한라산"],
    "도시": ["미국 샌프란시스코", "일본 도쿄", "일본 교토", "프랑스 파리", "대한민국 제주"],
    "이유": ["세계 최대 게임 개발자 행사 GDC에 가보고 싶어서",
            "게임과 애니메이션 문화를 직접 느껴보고 싶어서",
            "좋아하는 게임을 만든 회사를 보고 싶어서",
            "파리의 야경을 직접 보고 싶어서",
            "정상에 올라 백록담을 보고 싶어서"],
    "lat": [37.7842, 35.6984, 34.9697, 48.8584, 33.3617],
    "lon": [-122.4016, 139.7731, 135.7563, 2.2945, 126.5292],
})

st.subheader("📋 장소 목록")
st.dataframe(places[["장소", "도시", "이유"]], hide_index=True)

# 1. 기본 지도 (st.map)
st.subheader("📍 기본 지도 (st.map)")
st.map(places, latitude="lat", longitude="lon", size=100000, color="#FF4B4B")

# 2. PyDeck 지도 (마우스를 올리면 장소 정보 표시)
st.subheader("🗺️ PyDeck 지도 (st.pydeck_chart)")
layer = pdk.Layer(
    "ScatterplotLayer",
    data=places,
    get_position="[lon, lat]",
    get_radius=150000,       # 반지름 150km (세계 지도라서 크게)
    radius_min_pixels=6,     # 지도를 축소해도 점이 너무 작아지지 않게
    get_fill_color=[255, 75, 75],
    pickable=True,
)
tooltip = {"text": "{장소}\n{도시}\n{이유}", "style": {"color": "white"}}
view_state = pdk.ViewState(latitude=35, longitude=40, zoom=0.8, pitch=0)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip))