import streamlit as st
import pandas as pd
import requests
import json
import numpy as np
from datetime import datetime
from datetime import timedelta


# 현재 날짜 가져오기 + 현재 날짜 +14일 되는 날 -> 변수화
today = datetime.now().date()
to_day = str(today)
one_week = str(today + timedelta(days=7))
two_week = str(today + timedelta(days=14))

#2주 데이터 호출
startdate = to_day[0:4]+to_day[5:7]+to_day[8:10]
enddate = two_week[0:4]+two_week[5:7]+two_week[8:10]
two_week_url = f"https://www.hrd.go.kr/jsp/HRDP/HRDPO00/HRDPOA60/HRDPOA60_1.jsp?returnType=JSON&authKey=f3pGpa4GLQ2t18ffb7i4sa5RILrJFzmN&pageNum=1&pageSize=100&srchTraStDt={startdate}&srchTraEndDt={enddate}&outType=1&sort=ASC&sortCol=TRNG_BGDE&crseTracseSe=C0104&srchTraArea1=00"

two_week_response = requests.get(two_week_url)
two_week_contents = two_week_response.text
two_week_json_ob = json.loads(two_week_contents)

# json에서 데이터프레임으로 변환
two_week_body = two_week_json_ob["returnJSON"]
two_week_json_data = json.loads(two_week_body)
two_week_a = two_week_json_data['srchList']
two_week_a = pd.DataFrame(two_week_a)

# 데이터 전처리
two_week_data = two_week_a[["subTitle","title","traStartDate","traEndDate","yardMan","regCourseMan","address","titleLink"]]
two_week_data.columns = ["주관 기관","교육 명","교육 시작일","교육 종료일","교육 정원","신청 인원","지역","Hrd넷 링크"]

# 신청 인원, 교육_정원 데이터 타입 변경
two_week_data['신청 인원'] = two_week_data['신청 인원'].astype(int)
two_week_data['교육 정원'] = two_week_data['교육 정원'].astype(int)

# 경기 수원시 ~~구 -> 경기 수원시
two_week_data['지역'] = two_week_data['지역'].apply(lambda x: x[:6] if x.startswith('경기') else x)

# 지역을 인덱스로 변경
two_week_data = two_week_data.set_index(keys='지역')

df = two_week_data

# kdc 데이터 호출
startdate = to_day[0:4]+to_day[5:7]+to_day[8:10]
enddate = two_week[0:4]+two_week[5:7]+two_week[8:10]
kdc_url = f"https://www.hrd.go.kr/jsp/HRDP/HRDPO00/HRDPOA60/HRDPOA60_1.jsp?returnType=JSON&authKey=f3pGpa4GLQ2t18ffb7i4sa5RILrJFzmN&pageNum=1&pageSize=100&srchTraStDt={startdate}&srchTraEndDt={enddate}&outType=1&sort=ASC&sortCol=TRNG_BGDE&crseTracseSe=C0105&srchTraArea1=00"

kdc_response = requests.get(kdc_url)
kdc_contents = kdc_response.text
kdc_json_ob = json.loads(kdc_contents)

# json에서 데이터프레임으로 변환
kdc_body = kdc_json_ob["returnJSON"]
kdc_json_data = json.loads(kdc_body)
kdc_a = kdc_json_data['srchList']
kdc_a = pd.DataFrame(kdc_a)

# 데이터 전처리
kdc_data = kdc_a[["subTitle","title","traStartDate","traEndDate","yardMan","regCourseMan","address","titleLink"]]
kdc_data.columns = ["주관 기관","교육 명","교육 시작일","교육 종료일","교육 정원","신청 인원","지역","Hrd넷 링크"]

# 신청_인원, 교육_정원 데이터 타입 변경
kdc_data['신청 인원'] = kdc_data['신청 인원'].astype(int)
kdc_data['교육 정원'] = kdc_data['교육 정원'].astype(int)

# kdc_data['지역'] = kdc_data['지역'].apply(lambda x: '경기 수원시' if x.startswith('경기 수원시') else x)
kdc_data['지역'] = kdc_data['지역'].apply(lambda x: x[:6] if x.startswith('경기') else x)

# filtered_df = df[df['지역'].str.startswith('경기')]['지역'].apply(lambda x: x[:6])

kdc_data = kdc_data.set_index(keys='지역')
kdc_df = kdc_data



st.set_page_config(
    page_title="🗓️국모다 국비 교육 개강 일정 대시보드🗓️",
    page_icon="⭐",
    layout="wide")

#버튼
st.link_button("국모다 홈페이지", "https://slashpage.com/%EA%B5%AD%EB%AA%A8%EB%8B%A4")

#메인 이미지
st.image('main.png')

# 타이틀
st.title("❤️국비 부트 캠프❤️")

# 필터 및 데이터 프레임 출력
countries = st.multiselect(
"원하는 지역을 고르세요.", sorted(set(df.index)))

if not countries:
    df_filter = df
else:
    df_filter = df.loc[countries]

st.header("🥇 실시간 인기 국비 부트 캠프 1~3위 🥇", anchor=None, help=None)
col_metric1, col_metric2, col_metric3 = st.columns(3)

with col_metric1:
    st.subheader(df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=1).iloc[-1]]['주관 기관'].values[0])
    index_string = str(df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=1).iloc[-1]].index)
    result = index_string.split("[")[1].split("]")[0]
    st.text(result[1:3])
    st.metric(df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=1).iloc[-1]]['교육 명'].values[0], value = str(df_filter['신청 인원'].nlargest(n=1).iloc[-1]) + "명")
    a = df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=1).iloc[-1]]['Hrd넷 링크'].values[0]
    st.link_button("교육 확인하기", f"{a}")

with col_metric2:
    st.subheader(df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=2).iloc[-1]]['주관 기관'].values[0])
    index_string = str(df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=2).iloc[-1]].index)
    result = index_string.split("[")[1].split("]")[0]
    st.text(result[1:3])
    st.metric(df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=2).iloc[-1]]['교육 명'].values[0], value = str(df_filter['신청 인원'].nlargest(n=2).iloc[-1]) + "명")
    a = df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=2).iloc[-1]]['Hrd넷 링크'].values[0]
    st.link_button("교육 확인하기", f"{a}")

with col_metric3:
    st.subheader(df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=3).iloc[-1]]['주관 기관'].values[0])
    index_string = str(df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=3).iloc[-1]].index)
    result = index_string.split("[")[1].split("]")[0]
    st.text(result[1:3])
    st.metric(df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=3).iloc[-1]]['교육 명'].values[0] , value = str(df_filter['신청 인원'].nlargest(n=3).iloc[-1]) + "명")
    a = df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=3).iloc[-1]]['Hrd넷 링크'].values[0]
    st.link_button("교육 확인하기", f"{a}")

st.divider()
st.header("✏️2주 내 개강 과정✏️", anchor=None, help=None)
st.caption('아래 내용은 실시간으로 업데이트 됩니다!')

# 데이터 프레임 출력
if not countries:
    st.dataframe(df)
else:
    st.dataframe(df.loc[countries])
    df.sort_index()
    
st.divider()
st.divider()

st.title("❤️국비 기초 교육❤️")
st.header("🥇 실시간 인기 국비 기초 교육 1~3위 🥇", anchor=None, help=None)
col_kdc1, col_kdc2, col_kdc3 = st.columns(3)

with col_kdc1:
    st.subheader(kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=1).iloc[-1]]['주관 기관'].values[0])
    index_string = str(kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=1).iloc[-1]].index)
    result = index_string.split("[")[1].split("]")[0]
    st.text(result[1:3])
    st.metric(kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=1).iloc[-1]]['교육 명'].values[0], value = str(kdc_df['신청 인원'].nlargest(n=1).iloc[-1]) + "명")
    a = kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=1).iloc[-1]]['Hrd넷 링크'].values[0]
    st.link_button("교육 확인하기", f"{a}")

with col_kdc2:
    st.subheader(kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=2).iloc[-1]]['주관 기관'].values[0])
    index_string = str(kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=2).iloc[-1]].index)
    result = index_string.split("[")[1].split("]")[0]
    st.text(result[1:3])
    st.metric(kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=2).iloc[-1]]['교육 명'].values[0], value = str(kdc_df['신청 인원'].nlargest(n=2).iloc[-1]) + "명")
    a = kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=2).iloc[-1]]['Hrd넷 링크'].values[0]
    st.link_button("교육 확인하기", f"{a}")

with col_kdc3:
    st.subheader(kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=3).iloc[-1]]['주관 기관'].values[0])
    index_string = str(kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=3).iloc[-1]].index)
    result = index_string.split("[")[1].split("]")[0]
    st.text(result[1:3])
    st.metric(kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=3).iloc[-1]]['교육 명'].values[0] , value = str(kdc_df['신청 인원'].nlargest(n=3).iloc[-1]) + "명")
    a = kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=3).iloc[-1]]['Hrd넷 링크'].values[0]
    st.link_button("교육 확인하기", f"{a}")

st.divider()
st.header("✏️1주 내 개강 과정✏️", anchor=None, help=None)
st.caption('아래 내용은 실시간으로 업데이트 됩니다!')
st.dataframe(kdc_df)
st.divider()