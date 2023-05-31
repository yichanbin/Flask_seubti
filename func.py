import json
import requests
import pandas as pd
from datetime import date
import numpy as np
def INIT():
    cursor1 = resultlist(".venv/static/json/questions.json")
    cursor2=resultlist(".venv/static/json/type.json")

    questions=[]
    keyword=[]
    total=[0.0,0.0,0.0,0.0]
    style=[0,0,0,0]
    num=[7,5,3,5]
    Dataframe_List=[]
    Result_List=[]
    for i in cursor1:
        questions.append(i['question'])
        keyword.append(i['keyword'])

    for i in cursor2:
        Result_List.append(i)
    return questions, keyword, total, style, num,Result_List,Dataframe_List


def RecommandList(df,keywordlist):
    list=[]
    for index,row in df.iterrows():
        if row['0']==keywordlist[0] and row['1']==keywordlist[1] and row['2']==keywordlist[2] and row['3']==keywordlist[3]:
          add=[row[df.columns[0]],row['활용']]
          list.append(add)
    return list

def decimal_to_binary(decimal):
    binary_list = [0,0,0,0]
    for i in range(4):
      binary_list[3-i]=decimal%2
      decimal//=2
    return binary_list

class getdf:
    def Museum(self):

        # 딕셔너리들을 저장할 리스트
        data_list = resultlist(".venv/static/json/museum.json")

        # 각 문서를 딕셔너리로 저장하고 리스트에 추가
        title = [item["시설명"] for item in data_list]

        df = pd.DataFrame(title, columns=['시설명'])

        mark0 = df['시설명'].str.contains('박물관|역사관|기념관|미술')
        mark1 = df['시설명'].str.contains('아쿠아')
        mark2 = df['시설명'].str.contains('공예관|뮤지움|뮤지엄')
        mark3 = df['시설명'].str.contains('대학|고등학교')
        mark4 = df['시설명'].str.contains('세계골프역사박물관|코리아나화장박물관|63아트미술관아트센터나비미술관')
        mark5 = df['시설명'].str.contains('종이나라박물관|유리지공예관')
        mark6 = df['시설명'].str.contains('브이센터|피규어뮤지엄W|삼성미술관 Leeum|DDP디자인뮤지엄')

        df = df.dropna(subset=['시설명'])
        df = df[~mark3]

        df.loc[mark0|mark1,'0'] = 0
        df.loc[mark2|mark5,'0'] = 1
        df.loc[mark4|mark6,'0'] = 0 
        df.loc[mark0|~mark1|mark2,'1'] = 0
        df.loc[~mark0,'1'] = 1
        df.loc[mark1|mark2|mark4|mark5,'1'] = 1
        df.loc[mark6,'1'] = 0
        df.loc[mark0|mark1|mark2,'2'] = 0
        df.loc[~mark0&~mark1&~mark2,'2'] = 1
        df.loc[mark4|mark5|mark6,'2'] = 0
        df.loc[mark0,'3'] = 0
        df.loc[mark1|mark2,'3'] = 1
        df.loc[mark4|mark5,'3'] = 0
        df.loc[mark6,'3'] = 1
        df.loc[:,'활용'] = '서울시 박물관 미술관 정보'

        df = df.dropna(subset=['1'])
        df = df.dropna(subset=['0'])
        df = df.dropna(subset=['2'])
        df = df.dropna(subset=['3'])
        return df

    def MountainPark(self):
        url = "http://openapi.seoul.go.kr:8088/79694f754779696334396d42516547/json/SebcParkTourKor/1/1000/"

        response = requests.get(url)
        data = response.json()
        title=[i["NAME_KOR"] for i in data["SebcParkTourKor"]["row"]]

        df = pd.DataFrame(title, columns=['명칭'])

        mark0 = df['명칭'].str.contains('산|공원|수목원|숲')
        mark1 = df['명칭'].str.contains('생태|철새|생태경관보전지역')
        mark2 = df['명칭'].str.contains('서울대공원|서울어린이대공원|염창공원|영등포공원|오동공원|용마공원|월천근린공원|문정근린공원|방화공원|송파나루공원') 
        mark3 = df['명칭'].str.contains('오금공원|훈련원공원|낙산공원|남산공원|서초문화예술공원') 
        mark4 = df['명칭'].str.contains('올림픽공원|중랑캠핑숲') 
        mark5 = df['명칭'].str.contains('용산가족공원|파리공원|효창공원|도산공원|사육신공원|삼일공원|서대문독립공원|선유도공원|손기정공원|솔밭공원')

        df = df.dropna(subset=['명칭'])

        df.loc[mark0|mark1|mark2|mark3|mark5,'0'] = 0
        df.loc[mark4,'0'] = 1
        df.loc[mark0|mark1,'1'] = 0
        df.loc[mark2|mark3|mark4|mark5,'1'] = 1
        df.loc[mark0|mark1|mark2|mark3|mark4|mark5,'2'] = 1
        df.loc[mark0,'3'] = 1
        df.loc[mark1,'3'] = 0
        df.loc[mark2|mark4,'3'] = 1
        df.loc[mark3|mark5,'3'] = 0
        df.loc[:,'활용'] = '서울시 산과공원 생태관광 정보'

        df = df.dropna(subset=['1'])
        df = df.dropna(subset=['0'])
        df = df.dropna(subset=['2'])
        df = df.dropna(subset=['3'])

        return df

    def Zoo_Botanical_RecreationForest(self):
        url = "http://openapi.seoul.go.kr:8088/5a5447414a79696333316b48474955/json/SebcPleasureGroundKor1/1/1000/"

        response = requests.get(url)
        data = response.json()
        title=[i["NAME_KOR"] for i in data["SebcPleasureGroundKor1"]["row"]]
        cate=[i["CATE3_NAME"] for i in data["SebcPleasureGroundKor1"]["row"]]
    
        df = pd.DataFrame({'명칭':title, '분류3':cate})

        mark0 = df['분류3'].str.contains('동물원')
        mark1 = df['분류3'].str.contains('식물원')
        mark2 = df['분류3'].str.contains('휴양림')
        mark3 = df['명칭'].str.contains('곤충식물원')  #얘만 실내임.
        mark4 = df['명칭'].str.contains('금란조경꽃식물원|미림식물|청아식물원')   #얘는 식물 판매하는 곳이라서 버림.

        df = df.dropna(subset=['분류3'])
        df = df[~mark4]

        df.loc[mark0|mark1|mark2|mark3,'0'] = 0
        df.loc[mark0|mark3,'1'] = 1
        df.loc[mark1|mark2,'1'] = 0
        df.loc[mark0|mark1|mark2,'2'] = 1
        df.loc[mark3,'2'] = 0
        df.loc[mark3|mark1,'3'] = 0
        df.loc[mark2|mark0,'3'] = 1
        df.loc[:,'활용'] = '서울시 식물원. 동물원. 휴양림 정보'

        df = df.dropna(subset=['1'])
        df = df.dropna(subset=['0'])
        df = df.dropna(subset=['2'])
        df = df.dropna(subset=['3'])

        return df

    def TraditionalMarkets(self): 
        url = "http://openAPI.seoul.go.kr:8088/71456d506f7969633537464f437359/json/ListTraditionalMarket/1/1000/"

        response = requests.get(url)
        data = response.json()
        title=[i["ITEM_NM"] for i in data["ListTraditionalMarket"]["row"]]
        cate=[i["BUILDING_TYPE"] for i in data["ListTraditionalMarket"]["row"]]
    
        df = pd.DataFrame({'명칭':title, '형태':cate})

        mark0 = df['형태'].str.contains('건물형|지하도상가')
        mark1 = df['형태'].str.contains('골목형|상점가')
        mark2 = df['명칭'].str.contains('동문시장|청계5가지하쇼핑센터|보광시장')

        df = df.dropna(subset=['형태'])

        df.loc[mark0|mark1,'0'] = 0
        df.loc[mark0|mark1,'1'] = 1
        df.loc[mark2,'1'] = 0
        df.loc[mark0,'2'] = 0
        df.loc[mark1,'2'] = 1
        df.loc[mark2,'2'] = 0
        df.loc[mark0|mark1,'3'] = 1
        df.loc[:,'활용'] = '서울시 전통시장 현황'


        df = df.dropna(subset=['1'])
        df = df.dropna(subset=['0'])
        df = df.dropna(subset=['2'])
        df = df.dropna(subset=['3'])

        return df

    def CulturalHeritage(self): 
        url = "http://openapi.seoul.go.kr:8088/45734c44637969633931477751635a/json/SebcHistoricSiteKor/1/1000/"

        response = requests.get(url)
        data = response.json()
        title=[i["NAME_KOR"] for i in data["SebcHistoricSiteKor"]["row"]]
        df = pd.DataFrame(title,columns=['명칭'])

        mark0 = df['명칭'].str.contains('탑|왕릉')

        df = df.dropna(subset=['명칭'])


        df.loc[mark0|~mark0,'0'] = 0
        df.loc[mark0|~mark0,'1'] = 0
        df.loc[mark0|~mark0,'2'] = 1
        df.loc[mark0|~mark0,'3'] = 0
        df.loc[:,'활용'] = '서울시 유적지 현황'

        df = df.dropna(subset=['1'])
        df = df.dropna(subset=['0'])
        df = df.dropna(subset=['2'])
        df = df.dropna(subset=['3'])

        return df

    def EcologicalCulturalStreet(self):
        url = "http://openapi.seoul.go.kr:8088/4c7949567979696336384641735543/json/walkSaengtaeInfo/1/1000/"

        response = requests.get(url)
        data = response.json()
        title=[i["COURSE_NAME"] for i in data["walkSaengtaeInfo"]["row"]]
        course=[i["DETAIL_COURSE"] for i in data["walkSaengtaeInfo"]["row"]]
        df = pd.DataFrame({'코스명': title, '상세코스': course})

        mark0 = df['코스명'].str.contains('나들길|산책길')
        mark1 = df['상세코스'].str.contains('기념관|호국|박물관|릉|현충원|궁|미술관|자영비')
        mark2 = df['상세코스'].str.contains('체력장|모험의 나라|시장')
        mark4 = df['코스명'].str.contains('전쟁기념관')

        df = df.dropna(subset=['코스명'])

        df.loc[mark0|~mark0,'0'] = 0
        df.loc[mark0|~mark0,'1'] = 0
        df.loc[mark2,'1'] = 1
        df.loc[mark0|~mark0,'2'] = 1
        df.loc[mark0|~mark0,'3'] = 1
        df.loc[mark1,'3'] = 0
        df.loc[:,'활용'] = '서울시 생태문화길 코스정보'


        df = df.dropna(subset=['1'])
        df = df.dropna(subset=['0'])
        df = df.dropna(subset=['2'])
        df = df.dropna(subset=['3'])

        return df

    def SightseeingStreet(self):
        url = "http://openapi.seoul.go.kr:8088/52684e66487969633630566d555649/json/SebcTourStreetKor/1/1000/"

        response = requests.get(url)
        data = response.json()
        search=[i["NM_DP"] for i in data["SebcTourStreetKor"]["row"]]
        title = [i["NAME_KOR"] for i in data["SebcTourStreetKor"]["row"]]
        df = pd.DataFrame({'최종 표기명': title, '검색 키워드': search})

        mark0 = df['검색 키워드'].str.contains('궁|배움|문화|순국')
        mark1 = df['검색 키워드'].str.contains('축제')
        mark2 = df['최종 표기명'].str.contains('메타세콰이어길|북악산길/산책로|한강자전거도로(강서지구)|둘레길/순례길구간|둘레길2구간|돌담길|둘레길3구간|해맞이길|둘레길1구간')

        df = df.dropna(subset=['검색 키워드'])

        df.loc[mark0|mark1|~mark0|~mark1,'0'] = 0
        df.loc[~mark0,'1'] = 1
        df.loc[mark0|mark2,'1'] = 0
        df.loc[mark0|mark1|~mark0|~mark1,'2'] = 1
        df.loc[~mark0|mark1,'3'] = 1
        df.loc[mark0,'3'] = 0
        df.loc[mark2,'3'] = 1
        df.loc[:,'활용'] = '서울시 관광거리 정보'


        df = df.dropna(subset=['1'])
        df = df.dropna(subset=['0'])
        df = df.dropna(subset=['2'])
        df = df.dropna(subset=['3'])

        return df

    def LibraryLecture(self):
        url = "http://openapi.seoul.go.kr:8088/694b6c78417969633536497a625352/json/SeoulLibraryLectureInfo/1/1000/"

        response = requests.get(url)
        data = response.json()
        title=[i["TITLE"] for i in data["SeoulLibraryLectureInfo"]["row"]]
        end=[i["RECEIPT_END_DATE"] for i in data["SeoulLibraryLectureInfo"]["row"]]
        sub=[i["RECEIPT_START_DATE"] for i in data["SeoulLibraryLectureInfo"]["row"]]
        
        df = pd.DataFrame({'제목': title, '모집종료일': end, '모집시작일':sub})

        today = date.today()

        numeric_date = int(today.strftime('%Y%m%d'))
        numeric_end_date = int(today.strftime('%Y%m%d')) + 200
        numeric_start_date = int(today.strftime('%Y%m%d')) + 200

        if numeric_start_date % 10000 >= 1231:
          numeric_start_date = numeric_start_date - 1200 + 10000
        if numeric_end_date % 10000 >= 1231:
          numeric_start_date = numeric_start_date - 1200 + 10000

        df['모집종료일'] = pd.to_numeric(df['모집종료일'], errors='coerce')
        df['모집시작일'] = pd.to_numeric(df['모집시작일'], errors='coerce')   

        df = df[df['모집종료일'].isnull() | (df['모집종료일'] <= numeric_end_date)]
        df = df[df['모집종료일'].isnull() | (df['모집종료일'] >= numeric_date)]
        df = df[df['모집시작일'].isnull() | (df['모집시작일'] <= numeric_start_date)]

        mark0 = df['제목'].str.contains('만들기|꾸미기|활용')
        mark1 = df['제목'].str.contains('독서|읽기|강연|책읽는')

        df = df.dropna(subset=['제목'])

        df.loc[~mark0|mark1,'0'] = 0
        df.loc[mark0|~mark1,'0'] = 1
        df.loc[~mark0|mark1,'1'] = 1
        df.loc[mark0|~mark1,'1'] = 1
        df.loc[mark0|mark1,'2'] = 0
        df.loc[~mark0|~mark1,'2'] = 0
        df.loc[mark0|mark1,'3'] = 0
        df.loc[~mark0|~mark1,'3'] = 0
        df.loc[:,'활용'] = '서울도서관 강좌정보'

        return df

    def CulturalSpace(self):
        url = "http://openapi.seoul.go.kr:8088/45734c44637969633931477751635a/json/culturalSpaceInfo/1/1000/"

        response = requests.get(url)
        data = response.json()
        title=[i["FAC_NAME"] for i in data["culturalSpaceInfo"]["row"]]
        sub=[i["SUBJCODE"] for i in data["culturalSpaceInfo"]["row"]]
        df = pd.DataFrame({'문화시설명': title, '주제분류': sub})

        mark0 = df['주제분류'].str.contains('공연장')
        mark1 = df['주제분류'].str.contains('도서관|미술관|문화원|박물관|문화예술')
        mark2 = df['문화시설명'].str.contains('대학')
        mark3 = df['문화시설명'].str.contains('삼성미술관|LG아트센터 서울|코엑스전시장|은평구청소년문화의집|파빌리온|구캔갤러리|스페이스 이수|신도림 문화공간 다락')
        mark4 = df['문화시설명'].str.contains('서울풍물시장 전통문화체험관|종이나라박물관|난지미술창작스튜디오|가나아트스페이스|메이커시티')
        mark5 = df['문화시설명'].str.contains('예술가의집|남산예술센터드라마센터(구 동랑예술센터)|서울애니시네마|롯데월드 시네마|롯데시네마 노원')

        df = df.dropna(subset=['주제분류'])
        df = df[~mark2]
        df = df.dropna(subset=['문화시설명'])

        df.loc[mark0|mark1,'0'] = 0
        df.loc[mark3|mark5, '0'] = 0
        df.loc[mark4,'0'] = 1
        df.loc[mark0|mark1,'1'] = 1
        df.loc[mark3|mark4,'1'] = 1
        df.loc[mark5,'1'] = 0
        df.loc[mark0,'2'] = 0
        df.loc[mark1,'2'] = 0
        df.loc[mark3|mark4|mark5,'2'] = 0
        df.loc[mark0,'3'] = 1
        df.loc[mark1,'3'] = 0
        df.loc[mark3|mark4,'3'] = 0
        df.loc[mark5,'3'] = 1
        df.loc[:,'활용'] = '서울시 문화공간 정보'

        df = df.dropna(subset=['1'])
        df = df.dropna(subset=['0'])
        df = df.dropna(subset=['2'])
        df = df.dropna(subset=['3'])

        return df

    def FutureHeritage(self):
        url = "http://openapi.seoul.go.kr:8088/6d68534b6c79696334324c7259594b/json/futureCourseInfo/1/1000/"

        response = requests.get(url)
        data = response.json()
        title=[i["HT_NM"] for i in data["futureCourseInfo"]["row"]]
        sub =[i["AC_TITLE"] for i in data["futureCourseInfo"]["row"]]
        df = pd.DataFrame({'미래유산명': title, '체험코스 제목': sub})

        mark0 = df['미래유산명'].str.contains('극장|가옥', na=False)
        mark1 = df['미래유산명'].str.contains('대학|이마트', na=False)
        mark2 = df['미래유산명'].str.contains('기념관', na=False)
        mark3 = df['체험코스 제목'].str.contains('시장부터|과거도|여의도|성수동|중심도로|예술과|서민의|강남|권력의', na=False)
        mark4 = df['체험코스 제목'].str.contains('한양도성|근현대|현대사를|문화유산과|한옥과|시간|쌍문동', na=False)

        df = df[~mark1]
        df = df.dropna(subset=['미래유산명'])
        df = df.dropna(subset=['체험코스 제목'])

        df.loc[mark0|mark2|~mark0|~mark2,'0'] = 1
        df.loc[mark0|mark2|~mark0|~mark2,'1'] = 1
        df.loc[~mark3,'1'] = 0
        df.loc[mark0|mark2,'2'] = 0
        df.loc[~mark0&~mark2,'2'] = 1
        df.loc[mark0|~mark0|mark3,'3'] = 1
        df.loc[mark2|mark4,'3'] = 0
        df.loc[:,'활용'] = '서울시 서울미래유산 체험코스 정보'

        df = df.dropna(subset=['1'])
        df = df.dropna(subset=['0'])
        df = df.dropna(subset=['2'])
        df = df.dropna(subset=['3'])

        df['미래유산명'] = df['미래유산명'].replace('', np.nan)
        df['체험코스 제목'] = df['체험코스 제목'].replace('', np.nan)
        df = df.dropna(subset=['미래유산명', '체험코스 제목'])

        return df

    def CulturalEvent(self):
        url = "http://openapi.seoul.go.kr:8088/63516a735279696335384377507659/json/culturalEventInfo/1/1000/"

        response = requests.get(url)
        data = response.json()
        title=[i["TITLE"] for i in data["culturalEventInfo"]["row"]]
        end=[i["END_DATE"] for i in data["culturalEventInfo"]["row"]]
        cate=[i["CODENAME"] for i in data["culturalEventInfo"]["row"]]
        start = [i["STRTDATE"] for i in data["culturalEventInfo"]["row"]]
        df = pd.DataFrame({'공연/행사명': title, '분류': cate, '시작일': start,'종료일': end})

        today = date.today()

        numeric_date = int(today.strftime('%Y%m%d'))
        numeric_end_date = int(today.strftime('%Y%m%d')) + 200
        numeric_start_date = int(today.strftime('%Y%m%d')) + 200
        if numeric_start_date % 10000 >= 1231:
          numeric_start_date = numeric_start_date - 1200 + 10000
        if numeric_end_date % 10000 >= 1231:
          numeric_start_date = numeric_start_date - 1200 + 10000

        df['종료일'] = pd.to_datetime(df['종료일'], errors='coerce')
        df['종료일'] = df['종료일'].dt.strftime('%Y%m%d').astype(float)
        df['시작일'] = pd.to_datetime(df['시작일'], errors='coerce')
        df['시작일'] = df['시작일'].dt.strftime('%Y%m%d').astype(float)

        df = df[df['종료일'].isnull() | (df['종료일'] <= numeric_end_date)]
        df = df[df['종료일'].isnull() | (df['종료일'] >= numeric_date)]
        df = df[df['시작일'].isnull() | (df['시작일'] <= numeric_start_date)]

        mark0 = df['분류'].str.contains('클래식|독주/독창회')
        mark1 = df['분류'].str.contains('콘서트|무용')
        mark2 = df['분류'].str.contains('축제-문화/예술|축제-전통/역사')
        mark3 = df['분류'].str.contains('교육/체험')
        mark4 = df['공연/행사명'].str.contains('문화')
        mark5 = df['공연/행사명'].str.contains('특별전')
        mark6 = df['공연/행사명'].str.contains('노들공방')
        mark7 = df['공연/행사명'].str.contains('개로왕의')
        mark8 = df['공연/행사명']. str.contains('옹기테마체험관|[서울시립북서울미술관]')
        mark9 = df['공연/행사명'].str.contains('주현미|송대관|문단속|리사이틀|무대효과')
        mark10 = df['공연/행사명'].str.contains('[꿈마을체험교실]')
  

        df = df.dropna(subset=['공연/행사명'])

        df.loc[mark0|mark1,'0'] = 0
        df.loc[mark2|mark3|mark8|mark10,'0'] = 1
        df.loc[mark5|mark7,'0'] = 0
        df.loc[mark2|mark1,'1'] = 1
        df.loc[mark0|mark3,'1'] = 0
        df.loc[mark7|mark8|mark10,'1'] = 1
        df.loc[mark0|mark1|mark3,'2'] = 0
        df.loc[mark2,'2'] = 1
        df.loc[mark7|mark10,'2'] = 1
        df.loc[mark8,'2'] = 0
        df.loc[mark2|mark1,'3'] = 1
        df.loc[mark0|mark3|mark4,'3'] = 0
        df.loc[mark7|mark8|mark10,'3'] = 0
        df.loc[mark6|mark9,'3'] = 1
        df.loc[:,'활용'] = '서울시 문화행사 정보'


        df = df.dropna(subset=['1'])
        df = df.dropna(subset=['0'])
        df = df.dropna(subset=['2'])
        df = df.dropna(subset=['3'])

        return df

    def PublicEducationalServices(self):
        url = "http://openapi.seoul.go.kr:8088/636967666c79696333386847776453/json/ListPublicReservationEducation/1/1000/"

        response = requests.get(url)
        data = response.json()
        title=[i["SVCNM"] for i in data["ListPublicReservationEducation"]["row"]]
        location=[i["PLACENM"] for i in data["ListPublicReservationEducation"]["row"]]
        service=[i["SVCSTATNM"] for i in data["ListPublicReservationEducation"]["row"]]
        sub=[i["MINCLASSNM"] for i in data["ListPublicReservationEducation"]["row"]]
        start=[i["RCPTBGNDT"] for i in data["ListPublicReservationEducation"]["row"]]
        end=[i["RCPTENDDT"] for i in data["ListPublicReservationEducation"]["row"]]
        df = pd.DataFrame({'서비스명':title, '장소명': location, '서비스상태': service, '소분류명': sub, '접수시작일시':start, '접수종료일시':end})  #서비스명이 프로그램 제목인데 없길래 내가 추가함.

        today = date.today()

        numeric_date = int(today.strftime('%Y%m%d'))
        numeric_end_date = int(today.strftime('%Y%m%d')) + 200
        numeric_start_date = int(today.strftime('%Y%m%d')) + 200

        if numeric_start_date % 10000 >= 1231:
          numeric_start_date = numeric_start_date - 1200 + 10000
        if numeric_end_date % 10000 >= 1231:
          numeric_start_date = numeric_start_date - 1200 + 10000

        df['접수종료일시'] = pd.to_datetime(df['접수종료일시'], errors='coerce')
        df['접수종료일시'] = df['접수종료일시'].dt.strftime('%Y%m%d').astype(float)
        df['접수시작일시'] = pd.to_datetime(df['접수시작일시'], errors='coerce')
        df['접수시작일시'] = df['접수시작일시'].dt.strftime('%Y%m%d').astype(float)

        df = df[df['접수종료일시'].isnull() | ((df['접수종료일시'] >= numeric_date) & (df['접수종료일시'] <= numeric_end_date))]

        df = df[df['접수시작일시'].isnull() | (df['접수시작일시'] <= numeric_start_date)]


        mark0 = df['장소명'].str.contains('공원')
        mark1 = df['서비스상태'].str.contains('접수종료|예약마감')
        mark2 = df['소분류명'].str.contains('역사|자연/과학|교양/어학|청년정보|전문/자격|정보통신')
        mark3 = df['소분류명'].str.contains('스포츠|도시농업')
        mark4 = df['소분류명'].str.contains('공예/취미|미술제작')
        mark5 = df['장소명'].str.contains('방문자센터|커뮤니티센터.|녹색교실|강서한강공원>강서습지생태공원>강서습지생태공원안내센터|난지한강공원>한강야생탐사센터')                 #상세 분류를 위해 추가
        mark6 = df['서비스명'].str.contains('[월드컵공원]|[매헌시민의숲]')
        mark7 = df['서비스명'].str.contains('오르골|숲치유(6월)|디저트|라이프|가짜커피')
        mark8 = df['서비스명'].str.contains('모내기|곤충체험교실')
        mark9 = df['서비스명'].str.contains('서울반려식물병원|서울청년센터|라인댄스|탁구|줌바댄스')
        mark10 = df['서비스명'].str.contains('관악도시농업공원')
        mark11 = df['서비스명'].str.contains('전원생활교육')
        mark12 = df['서비스명'].str.contains('한강')
        mark13 = df['서비스명'].str.contains('한강야생탐사센터')
        mark14 = df['서비스명'].str.contains('요가')

        df = df.dropna(subset=['장소명'])
        df = df.dropna(subset=['소분류명'])
        df = df.dropna(subset=['서비스상태'])
        df = df[~mark1]

        df.loc[mark2,'0'] = 0
        df.loc[mark4|mark3|mark14,'0'] = 1
        df.loc[mark11|mark13,'0'] = 0
        df.loc[mark3,'1'] = 1
        df.loc[mark2|mark4,'1'] = 0
        df.loc[mark10|mark14,'1'] = 0
        df.loc[mark12|mark13,'1'] = 1
        df.loc[mark2|mark4|mark5,'2'] = 0
        df.loc[mark0|mark3|mark6,'2'] = 1
        df.loc[mark9|mark11|mark14, '2'] = 0
        df.loc[mark12|mark13,'2'] = 1
        df.loc[mark2,'3'] = 0
        df.loc[mark3|mark4|mark7,'3'] = 1
        df.loc[mark8|mark10|mark13,'3'] = 0
        df.loc[mark7|mark12|mark14,'3'] = 1
        df.loc[:,'활용'] = '서울시 교육 공공서비스예약 정보'


        df = df.dropna(subset=['1'])
        df = df.dropna(subset=['0'])
        df = df.dropna(subset=['2'])
        df = df.dropna(subset=['3'])
        return df

def resultlist(file_path):
    with open(file_path, 'r',encoding='utf-8') as file:
        data = json.load(file)
    json_list = list(data)
    return json_list

    