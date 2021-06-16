from pykrx import stock
import numpy as np

df = stock.get_market_ohlcv_by_date(fromdate="20160101", todate="20210611", ticker="261250")
        #A226490코스피(kodex) #A114800코스피인버스(kodex)   + -
        #A229200코스닥(kodex) #A251340:코스닥인버스(kodex)  -  +19%
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
df['수익률'] = np.where(cond_1 & cond_2 & cond_3, 
                     df['종가'] / df['목표가'],1)
df['누적수익률'] = df['수익률'].cumprod()
df['낙폭'] = (df['누적수익률'].cummax() - df['누적수익률']) / df['누적수익률'].cummax() * 100
print("MDD(%): ", df['낙폭'].max())
df
