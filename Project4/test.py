import os
import csv
from flask import Flask, render_template, request
import pandas as pd
import numpy as np

# CSV 파일 경로
CSV_FILEPATH = os.path.join(os.getcwd(), '중소기업은행_펀드 정보_20210205.csv') 

def eda(df):
    # 결측치 제거
    df['선취수수료(%)'] = df['선취수수료(%)'].fillna(0)

    # 법인 상품 제거
    _idx = df[df['펀드유형'].str.contains('법인')].index
    df.drop(index=_idx, inplace=True)

    # 'type' 컬럼 생성
    df['type'] = -1
    df = set_type(df, '주식형', 1)
    df = set_type(df, '채권형', 2)
    df = set_type(df, '혼합형', 3)
    df = set_type(df, '파생상품', 4)
    df = set_type(df, '재간접투자', 5)
    df = set_type(df, 'MMF', 6)
    df = set_type(df, '특별자산투자', 7)

    return df


# 펀드유형별 종목 번호 생성
# 1.주식형  2.채권형  3.주식혼합형&채권혼합형 
# 4.파생상품  5.재간접투자  6.MMF 7.특별자산투자
def set_type(df, typename, typenum):
  _idx = df[df['펀드유형'].str.contains(typename)].index
  for idx in _idx:
    df.at[idx, 'type'] = typenum
  return df


# 투자종목 선택
def fund_type(df, typenum):
  return df[df['type'] == typenum]


# 총보수(%) 선택
def total_pay(df, limitnum):
  if limitnum == 1:
    return df[df['총보수(%)'] <= 1.0]
  elif limitnum == 2:
    return df[(df['총보수(%)'] > 1.0) & (df['총보수(%)'] <= 2.0)]
  elif limitnum == 3:
    return df[(df['총보수(%)'] > 2.0) & (df['총보수(%)'] <= 3.0)]
  elif limitnum == 4:
    return df[(df['총보수(%)'] > 3.0) & (df['총보수(%)'] <= 4.0)]


# 고객 투자성향 선택
# 1.공격투자성향  2.중립투자성향  3.안정투자성향
def invest_type(df, style):
  grade = df['펀드등급'].values
  grade = np.unique(grade)
  grade.sort()
  result = list()
  mid = int(len(grade) / 3 * 2)

  if style == 1:
    result = [grade[0]]
  elif style == 2:
    result = grade[1:mid]
  elif style == 3:
    result = grade[mid:]

  return df[df['펀드등급'].isin(result)]


# 장단기 투자별 수익률 top10
# 1.단기  2.장기
def profit10(df, term):
  if term == 1:
    sorted_df = df.sort_values(by='3개월누적수익률(%)' ,ascending=False)
    result_df = sorted_df[sorted_df['3개월누적수익률(%)'] > 0]
  elif term == 2:
    sorted_df = df.sort_values(by='12개월누적수익률(%)', ascending=False)
    result_df = sorted_df[sorted_df['12개월누적수익률(%)'] > 0]
  return result_df


typenum = 1
style = 3
term = 2
paynum = 2

df = pd.read_csv(CSV_FILEPATH, encoding='cp949')
df = eda(df)
df1 = fund_type(df, typenum)  # 주식형 선택
df2 = total_pay(df1, paynum)  # 총보수 2% 이하로 제한
df3 = invest_type(df2, style) # 공격투자성향 선택
df4 = profit10(df3, term)  # 단기투자 선택
result = df4.sample(3)

v1 = result['운용사명'].values
v2 = result['상품명'].values
if term == 1:
    v3 = result['3개월누적수익률(%)'].values
elif term == 2:
    v3 = result['12개월누적수익률(%)'].values
v4 = result['펀드등급'].values
v5 = result['펀드유형'].values
v6 = result['선취수수료(%)'].values
v7 = result['총보수(%)'].values

data = pd.DataFrame({
    '운용사' : v1,
    '상품명' : v2,
    '펀드유형' : v3,
    '펀드위험등급' : v4,
    '누적수익률(%)' : v5,
    '선취수수료(%)' : v6,
    '총보수(%)' : v7
}) 

print(data)