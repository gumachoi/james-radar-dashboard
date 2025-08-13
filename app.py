import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="JamesRadarBot", page_icon="🤖", layout="wide")

st.title("🤖 JamesRadarBot")
st.write("James(유영상) 관련 뉴스 분석 대시보드")

# 테스트 데이터
data = pd.DataFrame({
    '시간': ['08:00', '09:00', '10:00', '11:00', '12:00'],
    '뉴스량': [2, 5, 3, 7, 4]
})

fig = px.bar(data, x='시간', y='뉴스량', title='시간대별 뉴스량')
st.plotly_chart(fig, use_container_width=True)

st.success("✅ JamesRadarBot 대시보드 테스트 성공!")
