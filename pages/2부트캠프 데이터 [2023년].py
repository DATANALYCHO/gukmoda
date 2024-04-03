import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
from datetime import timedelta

# 현재 날짜 가져오기 + 현재 날짜 +14일 되는 날 -> 변수화
today = datetime.now().date()
to_day = str(today)
two_week = str(today + timedelta(days=13))
one_month = str(today + timedelta(days=30))

#2023 교육 운영 데이터 호출

b = []
for i in range(1,16):
  last_year_url = f"https://www.hrd.go.kr/jsp/HRDP/HRDPO00/HRDPOA60/HRDPOA60_1.jsp?returnType=JSON&authKey=f3pGpa4GLQ2t18ffb7i4sa5RILrJFzmN&pageNum={i}&pageSize=100&srchTraStDt=20230101&srchTraEndDt=20231231&outType=1&sort=ASC&sortCol=TRNG_BGDE&crseTracseSe=C0104&srchTraArea1=00"
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


#=================================================================================================================================================================================
#2023 과정별 데이터 호출

#중복 합치기
last_year_data = last_year_data.groupby('교육 명').agg({
    '주관 기관' : 'first',
    '2023년 총 신청 인원': 'sum',
    'Hrd넷 링크' : 'first'
}).reset_index()

# 원하는 주관기관만 뽑기
last_year_data = last_year_data[last_year_data['주관 기관'].str.contains('스파르타|그렙|패스트|엘리스|멋쟁이|코드잇|모두의연구소|플레이데이터|멀티캠퍼스|구름|이스트소프트')]

last_year_data = last_year_data.set_index(keys='주관 기관').sort_values(by='2023년 총 신청 인원' ,ascending=False)
last_year_data_df = last_year_data

#====================================================================================================================================

#2023 교육 운영 데이터 호출[그래프]

#중복 합치기
last_year_graph_data = last_year_data.groupby('주관 기관').agg({
    '2023년 총 신청 인원': 'sum'
}).reset_index()

# 원하는 주관기관만 뽑기
last_year_graph_data = last_year_graph_data[last_year_graph_data['주관 기관'].str.contains('스파르타|그렙|패스트|엘리스|멋쟁이|코드잇|모두의연구소|플레이데이터|멀티캠퍼스|구름|이스트소프트')]
last_year_graph_data = last_year_graph_data.set_index(keys='주관 기관').sort_values(by='2023년 총 신청 인원' ,ascending=False)
last_year_graph_data_df = last_year_graph_data

#==================================================================================================================================

#중복 합치기
last_year_sheet_data = last_year_data.groupby('주관 기관').agg({
    '2023년 총 신청 인원': 'sum',
    'Hrd넷 링크' : 'first'
}).reset_index()

# 원하는 주관기관만 뽑기
last_year_sheet_data = last_year_sheet_data[last_year_sheet_data['주관 기관'].str.contains('스파르타|그렙|패스트|엘리스|멋쟁이|코드잇|모두의연구소|플레이데이터|멀티캠퍼스|구름|이스트소프트')]
last_year_sheet_data = last_year_sheet_data.set_index(keys='주관 기관').sort_values(by='2023년 총 신청 인원' ,ascending=False)
last_year_sheet_data_df = last_year_sheet_data

#====================================================================================================================================

st.set_page_config(
    page_title="🗓️2023년 부트캠프 대시보드🗓️",
    page_icon="⭐",
    layout="wide")

st.sidebar.header("2️⃣2023년 부트 캠프 데이터")

a1, a2, a3, a4 = st.columns(4)   

with a1:
    #버튼
    st.link_button("❤️국모다 홈페이지 접속❤️", "https://slashpage.com/%EA%B5%AD%EB%AA%A8%EB%8B%A4")

with a2:
    #버튼
    st.link_button("💛부트캠프 상담 신청💛", "https://forms.gle/ytur6ENewhtsNXRo8")

with a3:
    #버튼
    st.link_button("💚부트캠프 테스트 체험💚", "https://smore.im/quiz/OeXhUTZjG4")
    
with a4:
    #버튼
    st.link_button("💙국모다 오픈채팅방 참여💙", "https://open.kakao.com/o/g9nk698f")

# 타이틀
st.title("💜2023년 인기 부트 캠프💜")

# 필터 및 데이터 프레임 출력
last_year_countries = st.multiselect(
"원하는 기관을 고르세요.", sorted(set(last_year_data_df.index)))

if not last_year_countries:
    last_year_data_filter = last_year_data_df
else:
    last_year_data_filter = last_year_data_df.loc[last_year_countries]
    
st.header("🥇 과정 별 수강 인원 1~3위 🥇", anchor=None, help=None)
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
st.header("✏️과정 별 수강 인원✏️", anchor=None, help=None)

# 데이터 프레임 출력
if not last_year_countries:
    st.dataframe(last_year_data_df, column_config={"Hrd넷 링크":st.column_config.LinkColumn()})
else:
    st.dataframe(last_year_data_df.loc[last_year_countries], column_config={"Hrd넷 링크":st.column_config.LinkColumn()})
    last_year_data_df.sort_index()
st.divider()
st.header("✏️기관 별 수강 인원✏️", anchor=None, help=None)

last_year_graph_data1, last_year_graph_data2 = st.columns(2)
with last_year_graph_data1:
    st.dataframe(data=last_year_sheet_data_df, column_config={"Hrd넷 링크":st.column_config.LinkColumn()})
    
with last_year_graph_data2:   
    st.bar_chart(data=last_year_graph_data_df)

st.divider()