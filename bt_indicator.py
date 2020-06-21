import numpy as np
import pandas as pd
import math


# Double Exponential Moving Average
def DEMA(Equity,span):
    EMA = pd.Series((Equity.close).ewm(span=span).mean()) 
    N = len(EMA)
    DEMA = []
    for i in range(N):
        DEMA.append(2*EMA[i]-EMA[int(round(EMA[i]))])
    dataframe = pd.DataFrame(pd.Series(Equity.index,name='Date'))
    DEMA = dataframe.join(pd.Series(DEMA,name="DEMA"))
    return DEMA

# Exponential Moving Average
def EMA(Equity,span):
    dataframe = pd.DataFrame((Equity.close).ewm(span=span).mean().rename("EMA"))
    return dataframe

# Hull Moving Average

def HMA(Equity,span):
    WMA1 = pd.Series((Equity.close).ewm(span=span/2).mean()) 
    WMA2 = pd.Series((Equity.close).ewm(span=span).mean())
    WMA3 = (2*WMA1) - WMA2
    HMA = WMA3.ewm(span=math.sqrt(span)).mean().rename("HMA")
    dataframe = pd.DataFrame(HMA)
    return dataframe

# Short Moving Average

def SMA(Equity,span):
    dataframe = pd.DataFrame((Equity.close).rolling(span).mean().rename("SMA"))
    return dataframe

# Bollinger Bands

def BollingerBands(Equity,span):
    MA = pd.Series((Equity.close).rolling(span).mean())
    MSD = pd.Series((Equity.close).rolling(span).std())
    BAND1 = pd.Series(4*MSD/MA,name='First Band for span {}'.format(span))
    BAND2 = pd.Series((Equity.close - MA + (2*MSD))/(4*MSD),name='Second Band for span {}'.format(span))
    dataframe = pd.DataFrame(Equity.close)
    dataframe = dataframe.join(BAND1)
    dataframe = dataframe.join(BAND2)
    return dataframe

# Keltner Channel

def KeltnerChannel(Equity,span):
    MiddleLine = pd.Series(((Equity.High + Equity.Low + Equity.close)/3).rolling(span).mean(),name="Keltner Middle Line")
    LowerBand = pd.Series(((-2*Equity.High + 4*Equity.Low + Equity.close)/3).rolling(span).mean(),name="Keltner Lower Band")
    UpperBand = pd.Series(((4*Equity.High - 2*Equity.Low + Equity.close)/3).rolling(span).mean(),name="Keltner Upper Band")
    dataframe = pd.DataFrame()
    dataframe = pd.DataFrame(pd.Series(Equity.close,name="Closing Prices"))
    dataframe = dataframe.join(LowerBand)
    dataframe = dataframe.join(MiddleLine)
    dataframe = dataframe.join(UpperBand)
    return dataframe

# RSI
def RSI(Equity,span=14):
    rsi=[]
    data=Equity.close
    periods=span
    data=data.to_numpy(copy=True)
    start=(data[1:periods+1]-data[0:periods])

    z1=start.copy()
    z2=start.copy()
    for i in range(periods+1):
        rsi.append(None)
    z1[z1>0]=0
    z2[z2<0]=0
    z1=z1*-1
    AUM=z2.sum()/periods
    ADM=z1.sum()/periods

    for i in range(periods+1,len(data)):
        change=(data[i]-data[i-1])
        CUM=change if change>0 else 0
        CDM=-change if change<0 else 0
        AUM=(AUM*(periods-1)+CUM)/periods
        ADM=(ADM*(periods-1)+CDM)/periods
        RS=AUM/ADM
        rsi.append(100*RS/(1+RS))
    

    return rsi




