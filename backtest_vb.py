#주피터 구동. (vscode는 왜 안되는지 모르겠음)

from pykrx import stock
import numpy as np

df = stock.get_market_ohlcv_by_date(fromdate="20160101", todate="20210611", ticker="114800")
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

fee = 0.0026

df['수익률'] = np.where(df['고가'] > df['목표가'],   #당일고가가 타겟가격보다 높으면 매수 진행
                     df['종가'] / df['목표가'] - fee, 1) #- fee :매수시 수수료 0.015%, 매도시 수수료 0.015%, 거래세 매도시 0.23% 총(0.26%) #종가/타겟가격: 수익률
                       #조건에 맞지 않아 매수없으면 수익률은 그대로 1.
df['누적수익률'] = df['수익률'].cumprod()
df['낙폭'] = (df['누적수익률'].cummax() - df['누적수익률']) / df['누적수익률'].cummax() * 100
print("MDD(%): ", df['낙폭'].max())
df
