#------------------bt_Indicator----------------------------#

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
    
    MiddleLine = pd.Series(((Equity.high + Equity.low + Equity.close)/3).rolling(span).mean(),name="Keltner Middle Line")
    LowerBand = pd.Series(((-2*Equity.high + 4*Equity.low + Equity.close)/3).rolling(span).mean(),name="Keltner Lower Band")
    UpperBand = pd.Series(((4*Equity.high - 2*Equity.low + Equity.close)/3).rolling(span).mean(),name="Keltner Upper Band")
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

def make_ichimoku(Equity,a,b,c):
    "function to calculate ichimoku"
    "a = 9,b = 26,c = 52"
    x = Equity.copy()
    nine_avg = (x['high'].rolling(window=a).max() + x['low'].rolling(window=a).min())/2
    twentysix_avg = (x['high'].rolling(window=b).max() + x['low'].rolling(window=b).min())/2
    fiftytwo_avg = (x['high'].rolling(window=c).max() + x['low'].rolling(window=c).min())/2
    
    x['conversion'] = nine_avg
    x['base'] = twentysix_avg
    x['leading_a'] = ((nine_avg + twentysix_avg)/2).shift(b)
    x['leading_b'] = (fiftytwo_avg).shift(b)
    return x
    # Lagging is not calculated separetely.

def ATR(Equity,n):
    "function to calculate True Range and Average True Range"
    df = Equity.copy()
    df['H-L']=abs(df['high']-df['low'])
    df['H-PC']=abs(df['high']-df['close'].shift(1))
    df['L-PC']=abs(df['low']-df['close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1)
    df['ATR'] = df['TR'].rolling(n).mean()#rolling mean of TR is ATR
    df = df.drop(['H-L','H-PC','L-PC'],axis=1,inplace = True)
    return df

def MACD(Equity,a,b,c):
    """function to calculate MACD
       typical values a = 12; b =26, c =9"""
    df = Equity.copy()
    df["MA_Fast"]=df["close"].ewm(span=a,min_periods=a).mean()
    df["MA_Slow"]=df["close"].ewm(span=b,min_periods=b).mean()
    df["MACD"]=df["MA_Fast"]-df["MA_Slow"]
    df["Signal"]=df["MACD"].ewm(span=c,min_periods=c).mean()
    df.dropna(inplace=True)
    return df


def StochasticOscillator(Equity,window,span):
    #List containg adjusted low prices
    b=np.zeros(len(Equity))#Empty temporary array

    count=0# Will be used to access each index of the list 


    for count in range(0,len(Equity)-(span+1)):

        MaxHigh=Equity['high'][count]#Used to store maximum high of 14 day period
        MinLow=Equity['low'][count]#We are arbitrarily choosing lowest price of 1st day of 14 day period as minimum low for each period
    
        for i in range(count,count+span):
            if(Equity['high'][i]>MaxHigh):
                MaxHigh=Equity['high'][i]#Storing Maximum high
            
            
            if(Equity['low'][i]<MinLow):
                MinLow=Equity['low'][i]#Storing Minimum low
    
        k=((Equity['close'][count+span]-MinLow)/(MaxHigh-MinLow))#calculating the stochastic oscillator
        b[count+14] = k*100
 
    Equity['%k']=b
    
    Equity['%d']= Equity['%k'].rolling(window).mean()
    return Equity

def choppiness(Equity,tp):
    high = Equity["high"]
    low = Equity["low"]
    close = Equity["close"]
    atr = Equity(Equity,tp)['ATR']
    Timestamp = []
    CP = []
    for i in range(len(Equity)):
        if i < tp*2:
            Timestamp.append(Equity.index[i])
            CP.append(0)
        else:
            nmrt = np.log10(np.sum(atr[i-tp:i])/(max(high[i-tp:i])-min(low[i-tp:i])))
            dnmnt = np.log10(tp)
            Timestamp.append(candlestick.index[i])
            CP.append(round(100*nmrt / dnmnt))
    CP = pd.DataFrame({"CP" : CP}, index=Timestamp)
    return CP    

def TSI(Equity,r,s):
    "r = 25 and s  = 13 generally"
    M = Equity['close'].diff(1) 
    aM = abs(M)  
    EMA1 = M.ewm(span = r).mean()
    aEMA1 = aM.ewm(span = r).mean()  
    EMA2 = EMA1.ewm(span = s).mean()
    aEMA2 = aEMA1.ewm(span = s).mean()
    TSI = pd.Series(EMA2 / aEMA2, name = 'TSI_' + str(r) + '_' + str(s))  
    Equity = Equity.join(TSI)
    return TSI

def HA(df):
    df['HA_Close']=(df['open']+ df['high']+ df['low']+ df['close'])/4
    df['HA_Open']=(df['open']+df['close'])/2   
    for i in range(1, len(df)):
        df['HA_Open'][i]=(df['HA_Open'][i-1]+df['HA_Close'][i-1])/2 
    df['HA_High']=df[['HA_Open','HA_Close','High']].max(axis=1)
    df['HA_Low']=df[['HA_Open','HA_Close','Low']].min(axis=1)
    return df

def chande_momentum_oscillator(Equity, period):
    """
    Chande Momentum Oscillator.
    Formula:
    cmo = 100 * ((sum_up - sum_down) / (sum_up + sum_down))
    """
    close_data = np.array(Equity['close'])
    moving_period_diffs = [[(close_data[idx+1-period:idx+1][i] -
                 close_data[idx+1-period:idx+1][i-1]) for i in range(1, len(close_data[idx+1-period:idx+1]))] for idx in range(0, len(close_data))]
    sum_up = []
    sum_down = []
    for period_diffs in moving_period_diffs:
        ups = [val if val > 0 else 0 for val in period_diffs]
        sum_up.append(sum(ups))
        downs = [abs(val) if val < 0 else 0 for val in period_diffs]
        sum_down.append(sum(downs))

    sum_up = np.array(sum_up)
    sum_down = np.array(sum_down)
    # numpy is able to handle dividing by zero and makes those calculations
    # nans which is what we want, so we safely suppress the RuntimeWarning
    cmo = pd.DataFrame(100 * ((sum_up - sum_down) / (sum_up + sum_down)))
    return cmo

def slope(Equity,n):
    Equity['close'] = ser
    "function to calculate the slope of regression line for n consecutive points on a plot"
    ser= (ser - ser.min())/(ser.max() - ser.min())
    x = np.array(range(len(ser)))
    x = (x - x.min())/(x.max() - x.min())
    slopes = [i*0 for i in range(n-1)]
    for i in range(n,len(ser)+1):
        y_scaled = ser[i-n:i]
        x_scaled = x[i-n:i]
        x_scaled = sm.add_constant(x_scaled)
        model = sm.OLS(y_scaled,x_scaled)
        results = model.fit()
        slopes.append(results.params[-1])
    slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))
    return np.array(slope_angle)

def SSL(Equity,tp):
    smaHigh = Equity['high'].rolling(window = tp).mean()
    smaLow = Equity['low'].rolling(window = tp).mean()
    Equity.dropna(inplace = True)
    Equity['sslDown'] = np.NaN
    Equity['sslUp'] = np.NaN
    for row in range(tp,len(Equity)):
        if Equity['close'][row]> smaHigh[row]:
            HIV[row] = 1
        elif Equity['close'][row] < smaLow[row]:
            HIV[row] = -1
        else :
            HIV[row] = HIV[1]
    for row in range(tp,len(Equity)):
        if HIV[row]<0:
            Equity['sslDown'][row] = smaHigh[row]
        else :
            Equity['sslDown'][row] = smaLow[row]
    for row in range(tp,len(Equity)):
        if HIV[row]<0:
            Equity['sslUp'][row] = smaLow[row]
        else :
            Equity['sslUp'][row] = smaHigh[row]
        
    return Equity    
