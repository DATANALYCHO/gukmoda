import streamlit as st
import pandas as pd
import requests
import json
import numpy as np
from datetime import datetime
from datetime import timedelta

#====================================================================================================================================


# 현재 날짜 가져오기 + 현재 날짜 +14일 되는 날 -> 변수화
today = datetime.now().date()
to_day = str(today)
one_week = str(today + timedelta(days=7))
two_week = str(today + timedelta(days=14))
two_month = str(today + timedelta(days=30))

#====================================================================================================================================

#kdt 2주 데이터 호출
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

#중복 합치기
two_week_data = two_week_data.groupby('교육 명').agg({
    '주관 기관' : 'first',
    '교육 시작일': 'first',
    '교육 종료일': 'first',
    '교육 정원': 'sum',
    '신청 인원': 'sum',
    '지역': 'first',
    'Hrd넷 링크': 'first'
}).reset_index()

# 지역을 인덱스로 변경
two_week_data = two_week_data.set_index(keys='지역').sort_values(by='교육 시작일' ,ascending=True)

df = two_week_data

#====================================================================================================================================

# # kdc 데이터 호출
# startdate = to_day[0:4]+to_day[5:7]+to_day[8:10]
# enddate = two_week[0:4]+two_week[5:7]+two_week[8:10]
# kdc_url = f"https://www.hrd.go.kr/jsp/HRDP/HRDPO00/HRDPOA60/HRDPOA60_1.jsp?returnType=JSON&authKey=f3pGpa4GLQ2t18ffb7i4sa5RILrJFzmN&pageNum=1&pageSize=100&srchTraStDt={startdate}&srchTraEndDt={enddate}&outType=1&sort=ASC&sortCol=TRNG_BGDE&crseTracseSe=C0105&srchTraArea1=00"

# kdc_response = requests.get(kdc_url)
# kdc_contents = kdc_response.text
# kdc_json_ob = json.loads(kdc_contents)

# # json에서 데이터프레임으로 변환
# kdc_body = kdc_json_ob["returnJSON"]
# kdc_json_data = json.loads(kdc_body)
# kdc_a = kdc_json_data['srchList']
# kdc_a = pd.DataFrame(kdc_a)

# # 데이터 전처리
# kdc_data = kdc_a[["subTitle","title","traStartDate","traEndDate","yardMan","regCourseMan","address","titleLink"]]
# kdc_data.columns = ["주관 기관","교육 명","교육 시작일","교육 종료일","교육 정원","신청 인원","지역","Hrd넷 링크"]

# # 신청_인원, 교육_정원 데이터 타입 변경
# kdc_data['신청 인원'] = kdc_data['신청 인원'].astype(int)
# kdc_data['교육 정원'] = kdc_data['교육 정원'].astype(int)

# # kdc_data['지역'] = kdc_data['지역'].apply(lambda x: '경기 수원시' if x.startswith('경기 수원시') else x)
# kdc_data['지역'] = kdc_data['지역'].apply(lambda x: x[:6] if x.startswith('경기') else x)

# # filtered_df = df[df['지역'].str.startswith('경기')]['지역'].apply(lambda x: x[:6])

# kdc_data = kdc_data.set_index(keys='지역')
# kdc_df = kdc_data

#====================================================================================================================================

#KDT 우수기업 데이터 호출
startdate = to_day[0:4]+to_day[5:7]+to_day[8:10]
enddate = two_month[0:4]+two_month[5:7]+two_month[8:10]

b = []
for i in range(1,5):
  two_month_url = f"https://www.hrd.go.kr/jsp/HRDP/HRDPO00/HRDPOA60/HRDPOA60_1.jsp?returnType=JSON&authKey=f3pGpa4GLQ2t18ffb7i4sa5RILrJFzmN&pageNum={i}&pageSize=100&srchTraStDt={startdate}&srchTraEndDt={enddate}&outType=1&sort=ASC&sortCol=TRNG_BGDE&crseTracseSe=C0104&srchTraArea1=00"
  two_month_response = requests.get(two_month_url)
  two_month_contents = two_month_response.text
  two_month_json_ob = json.loads(two_month_contents)

  # json에서 데이터프레임으로 변환
  two_month_body = two_month_json_ob["returnJSON"]
  two_month_json_data = json.loads(two_month_body)
  two_month_a = two_month_json_data['srchList']
  two_month_i = pd.DataFrame(two_month_a)
  b.append(two_month_i)

concat_df = pd.concat(b)

# 데이터 전처리
two_month_data = concat_df[["subTitle","title","traStartDate","traEndDate","yardMan","regCourseMan","address","titleLink"]]
two_month_data.columns = ["주관 기관","교육 명","교육 시작일","교육 종료일","교육 정원","신청 인원","지역","Hrd넷 링크"]

# 신청_인원, 교육_정원 데이터 타입 변경
two_month_data['신청 인원'] = two_month_data['신청 인원'].astype(int)
two_month_data['교육 정원'] = two_month_data['교육 정원'].astype(int)

# 경기 이름 세팅
two_month_data['지역'] = two_month_data['지역'].apply(lambda x: x[:6] if x.startswith('경기') else x)

#중복 합치기
two_month_data = two_month_data.groupby('교육 명').agg({
    '주관 기관' : 'first',
    '교육 시작일': 'first',
    '교육 종료일': 'first',
    '교육 정원': 'sum',
    '신청 인원': 'sum',
    '지역': 'first',
    'Hrd넷 링크': 'first'
}).reset_index()

two_month_data = two_month_data[two_month_data['주관 기관'].str.contains('스파르타|그렙|패스트|엘리스|멋쟁이|코드잇|모두의연구소|플레이데이터|멀티캠퍼스|구름')]
two_month_data = two_month_data.set_index(keys='주관 기관').sort_values(by='교육 시작일' ,ascending=True)
kdt_ace_df = two_month_data

#====================================================================================================================================

#2023 교육 운영 데이터 호출

startdate = "20230101"
enddate = "20231231"

b = []
for i in range(1,16):
  last_year_url = f"https://www.hrd.go.kr/jsp/HRDP/HRDPO00/HRDPOA60/HRDPOA60_1.jsp?returnType=JSON&authKey=f3pGpa4GLQ2t18ffb7i4sa5RILrJFzmN&pageNum={i}&pageSize=100&srchTraStDt={startdate}&srchTraEndDt={enddate}&outType=1&sort=ASC&sortCol=TRNG_BGDE&crseTracseSe=C0104&srchTraArea1=00"
  last_year_response = requests.get(last_year_url)
  last_year_contents = last_year_response.text
  last_year_json_ob = json.loads(last_year_contents)

  # json에서 데이터프레임으로 변환
  last_year_body = last_year_json_ob["returnJSON"]
  last_year_json_data = json.loads(last_year_body)
  last_year_a = last_year_json_data['srchList']
  last_year_i = pd.DataFrame(last_year_a)
  b.append(last_year_i)

last_year_concat_df = pd.concat(b)

# 데이터 전처리
last_year_data = last_year_concat_df[["subTitle","title","regCourseMan","titleLink"]]
last_year_data.columns = ["주관 기관","교육 명","2023년 총 신청 인원","Hrd넷 링크"]


# 신청_인원, 교육_정원 데이터 타입 변경
last_year_data['2023년 총 신청 인원'] = last_year_data['2023년 총 신청 인원'].astype(int)


#중복 합치기
last_year_data = last_year_data.groupby('교육 명').agg({
    '주관 기관' : 'first',
    '2023년 총 신청 인원': 'sum',
    'Hrd넷 링크' : 'first'
}).reset_index()



# 원하는 주관기관만 뽑기
last_year_data = last_year_data[last_year_data['주관 기관'].str.contains('스파르타|그렙|패스트|엘리스|멋쟁이|코드잇|모두의연구소|플레이데이터|멀티캠퍼스|구름')]

last_year_data = last_year_data.set_index(keys='주관 기관').sort_values(by='2023년 총 신청 인원' ,ascending=False)
last_year_data_df = last_year_data

#====================================================================================================================================
#2023 교육 운영 데이터 호출[그래프]

# 데이터 전처리
last_year_aa_data = last_year_concat_df[["subTitle","title","regCourseMan","subTitleLink"]]
last_year_aa_data.columns = ["주관 기관","교육 명","2023년 총 신청 인원","Hrd넷 링크"]


# 신청_인원, 교육_정원 데이터 타입 변경
last_year_aa_data['2023년 총 신청 인원'] = last_year_aa_data['2023년 총 신청 인원'].astype(int)

#중복 합치기
last_year_graph_data = last_year_aa_data.groupby('주관 기관').agg({
    '2023년 총 신청 인원': 'sum'
}).reset_index()

# 원하는 주관기관만 뽑기
last_year_graph_data = last_year_graph_data[last_year_graph_data['주관 기관'].str.contains('스파르타|그렙|패스트|엘리스|멋쟁이|코드잇|모두의연구소|플레이데이터|멀티캠퍼스|구름')]
last_year_graph_data = last_year_graph_data.set_index(keys='주관 기관').sort_values(by='2023년 총 신청 인원' ,ascending=False)
last_year_graph_data_df = last_year_graph_data



#중복 합치기
last_year_sheet_data = last_year_aa_data.groupby('주관 기관').agg({
    '2023년 총 신청 인원': 'sum',
    'Hrd넷 링크' : 'first'
}).reset_index()

# 원하는 주관기관만 뽑기
last_year_sheet_data = last_year_sheet_data[last_year_sheet_data['주관 기관'].str.contains('스파르타|그렙|패스트|엘리스|멋쟁이|코드잇|모두의연구소|플레이데이터|멀티캠퍼스|구름')]
last_year_sheet_data = last_year_sheet_data.set_index(keys='주관 기관').sort_values(by='2023년 총 신청 인원' ,ascending=False)
last_year_sheet_data_df = last_year_sheet_data

#====================================================================================================================================

#페이지 전체 세팅
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

st.header("🥇 실시간 신청 1~3위 🥇", anchor=None, help=None)
col_metric1, col_metric2, col_metric3 = st.columns(3)

with col_metric1:
    st.write("1위")
    st.subheader(df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=1).iloc[-1]]['주관 기관'].values[0])
    index_string = str(df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=1).iloc[-1]].index)
    result = index_string.split("[")[1].split("]")[0]
    st.text(result[1:3])
    st.metric(df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=1).iloc[-1]]['교육 명'].values[0], value = str(df_filter['신청 인원'].nlargest(n=1).iloc[-1]) + "명")
    a = df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=1).iloc[-1]]['Hrd넷 링크'].values[0]
    st.link_button("교육 확인하기", f"{a}")

with col_metric2:
    st.write("2위")
    st.subheader(df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=2).iloc[-1]]['주관 기관'].values[0])
    index_string = str(df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=2).iloc[-1]].index)
    result = index_string.split("[")[1].split("]")[0]
    st.text(result[1:3])
    st.metric(df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=2).iloc[-1]]['교육 명'].values[0], value = str(df_filter['신청 인원'].nlargest(n=2).iloc[-1]) + "명")
    a = df_filter[df_filter['신청 인원'] == df_filter['신청 인원'].nlargest(n=2).iloc[-1]]['Hrd넷 링크'].values[0]
    st.link_button("교육 확인하기", f"{a}")

with col_metric3:
    st.write("3위")
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
    st.dataframe(df, column_config={"Hrd넷 링크":st.column_config.LinkColumn()})
else:
    st.dataframe(df.loc[countries], column_config={"Hrd넷 링크":st.column_config.LinkColumn()})
    df.sort_index()
    
st.divider()
st.divider()

# 타이틀
st.title("❤️인기 국비 부트 캠프❤️")

# 필터 및 데이터 프레임 출력
ka_countries = st.multiselect(
"원하는 주관 기관을 고르세요.", sorted(set(kdt_ace_df.index)))

if not ka_countries:
    kdt_ace_df_filter = kdt_ace_df
else:
    kdt_ace_df_filter = kdt_ace_df.loc[ka_countries]
    
st.header("🥇 실시간 신청 1~3위 🥇", anchor=None, help=None)
kdt_ace_col_metric1, kdt_ace_col_metric2, kdt_ace_col_metric3 = st.columns(3)   

with kdt_ace_col_metric1:
    st.write("1위")
    st.subheader(kdt_ace_df_filter[kdt_ace_df_filter['신청 인원'] == kdt_ace_df_filter['신청 인원'].nlargest(n=1).iloc[-1]].index.values[0])
    st.metric(kdt_ace_df_filter[kdt_ace_df_filter['신청 인원'] == kdt_ace_df_filter['신청 인원'].nlargest(n=1).iloc[-1]]['교육 명'].values[0], value = str(kdt_ace_df_filter['신청 인원'].nlargest(n=1).iloc[-1]) + "명")
    a = kdt_ace_df_filter[kdt_ace_df_filter['신청 인원'] == kdt_ace_df_filter['신청 인원'].nlargest(n=1).iloc[-1]]['Hrd넷 링크'].values[0]
    st.link_button("교육 확인하기", f"{a}")

with kdt_ace_col_metric2:
    st.write("2위")
    st.subheader(kdt_ace_df_filter[kdt_ace_df_filter['신청 인원'] == kdt_ace_df_filter['신청 인원'].nlargest(n=2).iloc[-1]].index.values[0])
    st.metric(kdt_ace_df_filter[kdt_ace_df_filter['신청 인원'] == kdt_ace_df_filter['신청 인원'].nlargest(n=2).iloc[-1]]['교육 명'].values[0], value = str(kdt_ace_df_filter['신청 인원'].nlargest(n=2).iloc[-1]) + "명")
    a = kdt_ace_df_filter[kdt_ace_df_filter['신청 인원'] == kdt_ace_df_filter['신청 인원'].nlargest(n=2).iloc[-1]]['Hrd넷 링크'].values[0]
    st.link_button("교육 확인하기", f"{a}")

with kdt_ace_col_metric3:
    st.write("3위")
    st.subheader(kdt_ace_df_filter[kdt_ace_df_filter['신청 인원'] == kdt_ace_df_filter['신청 인원'].nlargest(n=3).iloc[-1]].index.values[0])
    st.metric(kdt_ace_df_filter[kdt_ace_df_filter['신청 인원'] == kdt_ace_df_filter['신청 인원'].nlargest(n=3).iloc[-1]]['교육 명'].values[0] , value = str(kdt_ace_df_filter['신청 인원'].nlargest(n=3).iloc[-1]) + "명")
    a = kdt_ace_df_filter[kdt_ace_df_filter['신청 인원'] == kdt_ace_df_filter['신청 인원'].nlargest(n=3).iloc[-1]]['Hrd넷 링크'].values[0]
    st.link_button("교육 확인하기", f"{a}")

st.divider()
st.header("✏️1달 내 개강 과정✏️", anchor=None, help=None)
st.caption('아래 내용은 실시간으로 업데이트 됩니다!')

# 데이터 프레임 출력
if not ka_countries:
    st.dataframe(kdt_ace_df, column_config={"Hrd넷 링크":st.column_config.LinkColumn()})
else:
    st.dataframe(kdt_ace_df.loc[ka_countries], column_config={"Hrd넷 링크":st.column_config.LinkColumn()})
    kdt_ace_df.sort_index()

st.divider()
st.divider()

# st.title("❤️국비 기초 교육❤️")
# st.header("🥇 실시간 신청 1~3위 🥇", anchor=None, help=None)
# col_kdc1, col_kdc2, col_kdc3= st.columns(3)

# with col_kdc1:
#     st.write("1위")
#     st.subheader(kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=1).iloc[-1]]['주관 기관'].values[0])
#     index_string = str(kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=1).iloc[-1]].index)
#     result = index_string.split("[")[1].split("]")[0]
#     st.text(result[1:3])
#     st.metric(kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=1).iloc[-1]]['교육 명'].values[0], value = str(kdc_df['신청 인원'].nlargest(n=1).iloc[-1]) + "명")
#     a = kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=1).iloc[-1]]['Hrd넷 링크'].values[0]
#     st.link_button("교육 확인하기", f"{a}")

# with col_kdc2:
#     st.write("2위")
#     st.subheader(kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=2).iloc[-1]]['주관 기관'].values[0])
#     index_string = str(kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=2).iloc[-1]].index)
#     result = index_string.split("[")[1].split("]")[0]
#     st.text(result[1:3])
#     st.metric(kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=2).iloc[-1]]['교육 명'].values[0], value = str(kdc_df['신청 인원'].nlargest(n=2).iloc[-1]) + "명")
#     a = kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=2).iloc[-1]]['Hrd넷 링크'].values[0]
#     st.link_button("교육 확인하기", f"{a}")

# with col_kdc3:
#     st.write("3위")
#     st.subheader(kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=3).iloc[-1]]['주관 기관'].values[0])
#     index_string = str(kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=3).iloc[-1]].index)
#     result = index_string.split("[")[1].split("]")[0]
#     st.text(result[1:3])
#     st.metric(kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=3).iloc[-1]]['교육 명'].values[0] , value = str(kdc_df['신청 인원'].nlargest(n=3).iloc[-1]) + "명")
#     a = kdc_df[kdc_df['신청 인원'] == kdc_df['신청 인원'].nlargest(n=3).iloc[-1]]['Hrd넷 링크'].values[0]
#     st.link_button("교육 확인하기", f"{a}")
    

# st.divider()
# st.header("✏️1주 내 개강 과정✏️", anchor=None, help=None)
# st.caption('아래 내용은 실시간으로 업데이트 됩니다!')
# st.dataframe(kdc_df)
# st.divider()

# 타이틀
st.title("❤️2023년 인기 부트 캠프 총 수강 인원❤️")

# 필터 및 데이터 프레임 출력
last_year_countries = st.multiselect(
"원하는 기관을 고르세요.", sorted(set(last_year_data_df.index)))

if not last_year_countries:
    last_year_data_filter = last_year_data_df
else:
    last_year_data_filter = last_year_data_df.loc[last_year_countries]
    
st.header("🥇 총 수강 인원 1~3위 🥇", anchor=None, help=None)
last_year_metric1, last_year_metric2, last_year_metric3 = st.columns(3)   

with last_year_metric1:
    st.write("1위")
    st.subheader(last_year_data_filter[last_year_data_filter['2023년 총 신청 인원'] == last_year_data_filter['2023년 총 신청 인원'].nlargest(n=1).iloc[-1]].index.values[0])
    st.metric(last_year_data_filter[last_year_data_filter['2023년 총 신청 인원'] == last_year_data_filter['2023년 총 신청 인원'].nlargest(n=1).iloc[-1]]['교육 명'].values[0], value = str(last_year_data_filter['2023년 총 신청 인원'].nlargest(n=1).iloc[-1]) + "명")
    a = last_year_data_filter[last_year_data_filter['2023년 총 신청 인원'] == last_year_data_filter['2023년 총 신청 인원'].nlargest(n=1).iloc[-1]]['Hrd넷 링크'].values[0]
    st.link_button("교육 확인하기", f"{a}")

with last_year_metric2:
    st.write("2위")
    st.subheader(last_year_data_filter[last_year_data_filter['2023년 총 신청 인원'] == last_year_data_filter['2023년 총 신청 인원'].nlargest(n=2).iloc[-1]].index.values[0])
    st.metric(last_year_data_filter[last_year_data_filter['2023년 총 신청 인원'] == last_year_data_filter['2023년 총 신청 인원'].nlargest(n=2).iloc[-1]]['교육 명'].values[0], value = str(last_year_data_filter['2023년 총 신청 인원'].nlargest(n=2).iloc[-1]) + "명")
    a = last_year_data_filter[last_year_data_filter['2023년 총 신청 인원'] == last_year_data_filter['2023년 총 신청 인원'].nlargest(n=2).iloc[-1]]['Hrd넷 링크'].values[0]
    st.link_button("교육 확인하기", f"{a}")

with last_year_metric3:
    st.write("3위")
    st.subheader(last_year_data_filter[last_year_data_filter['2023년 총 신청 인원'] == last_year_data_filter['2023년 총 신청 인원'].nlargest(n=3).iloc[-1]].index.values[0])
    st.metric(last_year_data_filter[last_year_data_filter['2023년 총 신청 인원'] == last_year_data_filter['2023년 총 신청 인원'].nlargest(n=3).iloc[-1]]['교육 명'].values[0] , value = str(last_year_data_filter['2023년 총 신청 인원'].nlargest(n=3).iloc[-1]) + "명")
    a = last_year_data_filter[last_year_data_filter['2023년 총 신청 인원'] == last_year_data_filter['2023년 총 신청 인원'].nlargest(n=3).iloc[-1]]['Hrd넷 링크'].values[0]
    st.link_button("교육 확인하기", f"{a}")

st.divider()
st.header("✏️2023년 과정 별 총 수강 인원✏️", anchor=None, help=None)

# 데이터 프레임 출력
if not last_year_countries:
    st.dataframe(last_year_data_df, column_config={"Hrd넷 링크":st.column_config.LinkColumn()})
else:
    st.dataframe(last_year_data_df.loc[last_year_countries], column_config={"Hrd넷 링크":st.column_config.LinkColumn()})
    last_year_data_df.sort_index()
st.divider()
st.header("✏️2023년 총 수강 인원✏️", anchor=None, help=None)

last_year_graph_data1, last_year_graph_data2 = st.columns(2)
with last_year_graph_data1:
    st.dataframe(data=last_year_sheet_data_df, column_config={"Hrd넷 링크":st.column_config.LinkColumn()})
    
with last_year_graph_data2:   
    st.bar_chart(data=last_year_graph_data_df)

st.divider()


