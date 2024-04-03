import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
from datetime import timedelta

#====================================================================================================================================

# 현재 날짜 가져오기 + 현재 날짜 +14일 되는 날 -> 변수화
today = datetime.now().date()
to_day = str(today)
two_week = str(today + timedelta(days=13))
one_month = str(today + timedelta(days=30))

#====================================================================================================================================
#한달 데이터 불러와서 가공
startdate = to_day[0:4]+to_day[5:7]+to_day[8:10]
enddate = one_month[0:4]+one_month[5:7]+one_month[8:10]

b = []
for i in range(1,5):
  one_month_url = f"https://www.hrd.go.kr/jsp/HRDP/HRDPO00/HRDPOA60/HRDPOA60_1.jsp?returnType=JSON&authKey=f3pGpa4GLQ2t18ffb7i4sa5RILrJFzmN&pageNum={i}&pageSize=100&srchTraStDt={startdate}&srchTraEndDt={enddate}&outType=1&sort=ASC&sortCol=TRNG_BGDE&crseTracseSe=C0104&srchTraArea1=00"
  one_month_response = requests.get(one_month_url)
  one_month_contents = one_month_response.text
  one_month_json_ob = json.loads(one_month_contents)

  # json에서 데이터프레임으로 변환
  one_month_body = one_month_json_ob["returnJSON"]
  one_month_json_data = json.loads(one_month_body)
  one_month_a = one_month_json_data['srchList']
  one_month_i = pd.DataFrame(one_month_a)
  b.append(one_month_i)

concat_df = pd.concat(b)

# 데이터 전처리
one_month_data = concat_df[["subTitle","title","traStartDate","traEndDate","yardMan","regCourseMan","address","titleLink"]]
one_month_data.columns = ["주관 기관","교육 명","교육 시작일","교육 종료일","교육 정원","신청 인원","지역","Hrd넷 링크"]

# 신청_인원, 교육_정원 데이터 타입 변경
one_month_data['신청 인원'] = one_month_data['신청 인원'].astype(int)
one_month_data['교육 정원'] = one_month_data['교육 정원'].astype(int)

# 경기 이름 세팅
one_month_data['지역'] = one_month_data['지역'].apply(lambda x: x[:6] if x.startswith('경기') else x)

#중복 합치기
one_month_data = one_month_data.groupby('교육 명').agg({
    '주관 기관' : 'first',
    '교육 시작일': 'first',
    '교육 종료일': 'first',
    '교육 정원': 'sum',
    '신청 인원': 'sum',
    '지역': 'first',
    'Hrd넷 링크': 'first'
}).reset_index()


#=================================================================================================================================

#kdt 2주 데이터 호출
two_week_data = one_month_data.set_index(keys='지역').sort_values(by='교육 시작일' ,ascending=True)
two_week_data['교육 시작일'] = pd.to_datetime(two_week_data['교육 시작일'])
two_week_data = two_week_data[(two_week_data['교육 시작일'] >= to_day) & (two_week_data['교육 시작일'] <= two_week)]
df = two_week_data

#====================================================================================================================================

#KDT 우수기업 데이터 호출

# 원하는 주관기관만 뽑기
one_month_data = one_month_data[one_month_data['주관 기관'].str.contains('스파르타|그렙|패스트|엘리스|멋쟁이|코드잇|모두의연구소|플레이데이터|멀티캠퍼스|구름|이스트소프트')]
# 주관 기관을 인덱스로 설정 / 교육 시작일로 정렬
one_month_data = one_month_data.set_index(keys='주관 기관').sort_values(by='교육 시작일' ,ascending=True)
kdt_ace_df = one_month_data

#====================================================================================================================================

st.set_page_config(
    page_title="🗓️실시간 부트캠프 대시보드🗓️",
    page_icon="⭐",
    layout="wide")

st.sidebar.header("3️⃣실시간 부트 캠프 데이터")

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

#====================================================================================================================================

# 타이틀
st.title("💜국비 부트 캠프💜")

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

#====================================================================================================================================

# 타이틀
st.title("🤎인기 국비 부트 캠프🤎")

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
