#파일하나에 1.only 변동성돌파 + 2. 변동성돌파+5ma 3. 변동성돌파+5ma+10ma  4.변동성돌파+10ma
##변동성돌파전략 백테스트 + 이동평균 + 한꺼번에 출력


from pykrx import stock
import numpy as np

df = stock.get_market_ohlcv_by_date(fromdate="20160101", todate="20210611", ticker="261250")
        #A226490코스피(kodex) #A114800코스피인버스(kodex)  
        #A229200코스닥(kodex) #A251340:코스닥인버스(kodex)  
        #A261220원유(kodex)   #A271050원유인버스(kodex)

        #A122630:코스피레버리지(kodex)  #A252670:코스피인버스X2(kodex)
        #A233740:코스닥레버리지(kodex)  #A251340:코스닥인버스(kodex)
            #A261250달러레버리지(kodex)     #A261120달러인버스X2(tiger)
        #A261220원유(kodex)            #A271050원유인버스(kodex) 
df['변동폭'] = (df['고가'] - df['저가']) * 0.7
df['목표가'] = df['시가'] + df['변동폭'].shift(1)

#이동평균ma5, ma10 컬럼추가
#목표가와 비교 후 현재가가 낮으면 1, 높으면 수익률 계산
#현재가와 ma5 대조, 현재가와 ma5, ma10 둘다 대조, 현재가와 ma10 대조(세가지 경우) 모두 해보기
df['5일이동평균'] = df['종가'].rolling(window=5).mean()
df['10일이동평균'] = df['종가'].rolling(window=10).mean()

cond_1 = df['고가'] > df['목표가']
cond_2 = df['목표가'] > df['5일이동평균']
cond_3 = df['목표가'] > df['10일이동평균']

#수익률 계산_1 변동성돌파전략
df['수익률_vb'] = np.where(cond_1,   #당일고가가 타겟가격보다 높으면 매수 진행
                     df['종가'] / df['목표가'] - 0.26%, 1) #- fee :매수시 수수료 0.015%, 매도시 수수료 0.015%, 거래세 매도시 0.23% 총(0.26%) #종가/타겟가격: 수익률
                       #조건에 맞지 않아 매수없으면 수익률은 그대로 1.
df['누적수익률_vb'] = df['수익률_vb'].cumprod()
df['낙폭'] = (df['누적수익률_vb'].cummax() - df['누적수익률_vb']) / df['누적수익률_vb'].cummax() * 100
print("MDD_vb(%): ", df['낙폭'].max())

#수익률 계산_2 변동성돌파전략+5MA
df['수익률_vb+5MA'] = np.where(cond_1 & cond_2, 
                     df['종가'] / df['목표가'] - 0.26%, 1)
df['누적수익률_vb+5MA'] = df['수익률_vb+5MA'].cumprod()
df['낙폭'] = (df['누적수익률_vb+5MA'].cummax() - df['누적수익률_vb+5MA']) / df['누적수익률_vb+5MA'].cummax() * 100
print("MDD_vb+5MA(%): ", df['낙폭'].max())


#수익률 계산_3 변동성돌파전략+5MA+10MA
df['수익률_vb+5MA+10MA'] = np.where(cond_1 & cond_2 & cond_3, 
                     df['종가'] / df['목표가'] - 0.26%, 1)
df['누적수익률_vb+5MA+10MA'] = df['수익률_vb+5MA+10MA'].cumprod()
df['낙폭'] = (df['누적수익률_vb+5MA+10MA'].cummax() - df['누적수익률_vb+5MA+10MA']) / df['누적수익률_vb+5MA+10MA'].cummax() * 100
print("MDD_vb+5MA+10MA(%): ", df['낙폭'].max())

#수익률 계산_4 변동성돌파전략+10MA
df['수익률_vb+10MA'] = np.where(cond_1 & cond_3, 
                     df['종가'] / df['목표가'] - 0.26%, 1)
df['누적수익률_vb+10MA'] = df['수익률_vb+10MA'].cumprod()
df['낙폭'] = (df['누적수익률_vb+10MA'].cummax() - df['누적수익률_vb+10MA']) / df['누적수익률_vb+10MA'].cummax() * 100
print("MDD_vb+10MA(%): ", df['낙폭'].max())

#엑셀로 출력
df.to_excel("216250_3.xlsx") 
df
