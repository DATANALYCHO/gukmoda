import streamlit as st
import pandas as pd
import requests
import json

st.write("Hello World")

url = "https://www.hrd.go.kr/jsp/HRDP/HRDPO00/HRDPOA60/HRDPOA60_1.jsp?returnType=JSON&authKey=f3pGpa4GLQ2t18ffb7i4sa5RILrJFzmN&pageNum=1&pageSize=100&srchTraStDt=20240325&srchTraEndDt=20240531&outType=1&sort=ASC&sortCol=TRNG_BGDE&crseTracseSe=C0104&srchTraArea1=00"

response = requests.get(url)
contents = response.text
json_ob = json.loads(contents)

body = json_ob["returnJSON"]
json_data = json.loads(body)
a = json_data['srchList']
a = pd.DataFrame(a)
data = a[["subTitle","title","traStartDate","traEndDate","yardMan","regCourseMan","address","titleLink"]]
data.columns = ["주관 기관","교육 명","교육 시작일","교육 종료일","교육 정원","신청 인원","지역","Hrd넷 링크"]
data