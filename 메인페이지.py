import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
from datetime import timedelta
#====================================================================================================================================

st.set_page_config(
    page_title="🗓️국모다 부트 캠프 대시보드🗓️",
    page_icon="⭐",
    layout="wide")

st.sidebar.header("1️⃣국모다 부트 캠프 대시보드")

a1, a2, a3, a4 = st.columns(4)   

with a1:
    #버튼
    st.link_button("❤️국모다 홈페이지로 마실가기❤️", "https://slashpage.com/%EA%B5%AD%EB%AA%A8%EB%8B%A4")

with a2:
    #버튼
    st.link_button("💛부트캠프 상담 신청하기💛", "https://forms.gle/ytur6ENewhtsNXRo8")

with a3:
    #버튼
    st.link_button("💚부트캠프 테스트 하러가기💚", "https://smore.im/quiz/OeXhUTZjG4")
    
with a4:
    #버튼
    st.link_button("💙국모다 오픈채팅방 참여하기💙", "https://open.kakao.com/o/g9nk698f")

#메인 이미지
st.image('main.png')

#====================================================================================================================================

