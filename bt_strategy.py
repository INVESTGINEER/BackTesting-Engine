#-------------------------------bt-strategy------------------------#

#import backtest_engine as bt
#import backtest_indicator as indicator


def sma_crossover (Equity,Instrument_ID):
  span1=7
  span2=15
  value1=SMA(Equity,span1)
  value2=SMA(Equity,span2)

  Crossover_strategy(Equity.close,Equity.index,value1,value2,Instrument_ID)

def hma_crossover (Equity,Instrument_ID):
  span1=7
  span2=15
  value1=HMA(Equity,span1)
  value2=HMA(Equity,span2)

  print(Equity.close)
  bt.Crossover_strategy(Equity.close,Equity.index,value1,value2,Instrument_ID)

def ema_crossover (Equity,Instrument_ID):
  span1=7
  span2=15
  value1=EMA(Equity,span1)
  value2=EMA(Equity,span2)

  print(Equity.close)
  Crossover_strategy(Equity.close,Equity.index,value1,value2,Instrument_ID)

def dema_crossover (Equity,Instrument_ID):
  span1=7
  span2=15
  value1=DEMA(Equity,span1)
  value2=DEMA(Equity,span2)

  print(Equity.close)
  Crossover_strategy(Equity.close,Equity.index,value1,value2,Instrument_ID)

def RSI_STRATEGY(records,Instrument_ID=0,periods=14):

  last_order_placed = None
  last_order_price = 0

  rsi= RSI(records,periods)
  for i in range(periods+2,len(records)):
    #Placing buy order
    if rsi[i]>20 and rsi[i-1]<20 and last_order_placed!='BUY':
      #print("Enter buy ",rsi[i],"    ",rsi[i-1],"    ",records.index[i])
      Place_Order(Instrument_ID,date=records.index[i],CMP=records.close[i],signal="BUY",quantity=100) 
      last_order_placed='BUY'
      last_order_price=records.close[i]
    
    #Placing sell order
    if rsi[i]<80 and rsi[i-1]>80 and last_order_placed!='SELL':
      #print("Enter sell ",rsi[i],"    ",rsi[i-1],"    ",records.index[i])
      Place_Order(Instrument_ID,date=records.index[i],CMP=records.close[i],signal="SELL",quantity=-100)
      last_order_placed='SELL'
      last_order_price=records.close[i]
    
    #Closing sell order
    if rsi[i]<20 and rsi[i-1]>20 and last_order_placed=='SELL':
      #print("Close sell ",rsi[i],"    ",rsi[i-1],"    ",records.index[i])
      Place_Order(Instrument_ID,date=records.index[i],CMP=records.close[i],signal="BUY",quantity=100) 

      last_order_placed=None
      last_order_price=0
    
    #Closing buy order
    if rsi[i]>80 and rsi[i-1]<80 and last_order_placed=='BUY':
      #print("Close buy ",rsi[i],"    ",rsi[i-1],"    ",records.index[i])
      Place_Order(Instrument_ID,date=records.index[i],CMP=records.close[i],signal="SELL",quantity=-100) 

      
      last_order_placed=None
      last_order_price=0

def KELTNER_STRATEGY(records,Instrument_ID=0,periods=14):
    KELTNER_CHANNEL=KeltnerChannel(records,periods)
    KELTNER_CHANNEL.rename(columns={'Keltner Lower Band':'lower'}, inplace=True)
    KELTNER_CHANNEL.rename(columns={'Keltner Upper Band':'upper'}, inplace=True)
    BAND_STRATEGY(records,KELTNER_CHANNEL,Instrument_ID)

def BOLLINGER_STRATEGY(records,Instrument_ID=0,periods=14):
    BOLLINGER_BAND=BollingerBands(records,periods)
    BOLLINGER_BAND.rename(columns={'First Band for span '+str(periods):'lower'}, inplace=True)
    BOLLINGER_BAND.rename(columns={'Second Band for span '+str(periods):'upper'}, inplace=True)
    print(BOLLINGER_BAND.lower[300:310])
    print(BOLLINGER_BAND.upper[300:310])
    BAND_STRATEGY(records,BOLLINGER_BAND,Instrument_ID)


def BAND_STRATEGY(Equity,band,Instrument_ID):
    print(Equity.head())
    print(band.head(20))
    print(Instrument_ID)
    last_order_placed=None
    for i in range(len(Equity)):
        #Placing buy order and closing sell order
        if Equity.close[i]<band['lower'][i] :
            if last_order_placed=='BUY':
                pass
            elif last_order_placed==None:
                Place_Order(Instrument_ID,date=records.index[i],CMP=Equity.close[i],signal="BUY",quantity=100) 
                last_order_placed='BUY'
            elif last_order_placed=='SELL':    
                Place_Order(Instrument_ID,date=records.index[i],CMP=Equity.close[i],signal="BUY",quantity=100) 
                Place_Order(Instrument_ID,date=records.index[i],CMP=Equity.close[i],signal="BUY",quantity=100) 
                last_order_placed='BUY'


          
        #Placing sell order and closing buy order
        if Equity.close[i]>band['upper'][i] :
            if last_order_placed=='BUY':
                Place_Order(Instrument_ID,date=records.index[i],CMP=Equity.close[i],signal="SELL",quantity=-100) 
                Place_Order(Instrument_ID,date=records.index[i],CMP=Equity.close[i],signal="SELL",quantity=-100) 
                last_order_placed='SELL'
            elif last_order_placed==None: 
                Place_Order(Instrument_ID,date=records.index[i],CMP=Equity.close[i],signal="SELL",quantity=-100)
                last_order_placed='SELL'
            elif last_order_placed=='SELL':    
                pass  

def strategy_ichimoku(Equity,Instrument_ID,a,b,c):
    Equity = make_ichimoku(Equity,a,b,c)
    last_order_placed = None
    last_order_price = 0
    for row in range(len(Equity)):
        if last_order_placed =='SELL':
            if (Equity['conversion'].iloc[row-1] <= Equity['base'].iloc[row-1]) and  (Equity['conversion'].iloc[row] > Equity['base'].iloc[row]) and (Equity['close'].iloc[row] > max(Equity['leading_a'].iloc[row],Equity['leading_b'].iloc[row])) and (Equity['close'].iloc[row] > max(Equity['leading_a'].iloc[row-b],Equity['leading_b'].iloc[row-b])):
                Place_Order(Instrument_ID,date = Equity.index[row],CMP = Equity['close'][row],signal = "BUY",quantity = 100)
                Place_Order(Instrument_ID,date = Equity.index[row],CMP = Equity['close'][row],signal = "BUY",quantity = 100)
                last_order_placed = "BUY"
                last_order_price = 0

            if (Equity['conversion'].iloc[row-1] >= Equity['base'].iloc[row-1]) and  (Equity['conversion'].iloc[row] < Equity['base'].iloc[row]) and (Equity['close'].iloc[row] < min(Equity['leading_a'].iloc[row],Equity['leading_b'].iloc[row])) and (Equity['close'].iloc[row] < min(Equity['leading_a'].iloc[row-b],Equity['leading_b'].iloc[row-b])):
                Place_Order(Instrument_ID,date = Equity.index[row],CMP = Equity['close'][row],signal = "SELL",quantity = -100)
                last_order_placed = "SELL"
                last_order_price = Equity['close'][row]
        
        elif last_order_placed =='BUY':
            if(Equity['close'].iloc[row-1] > max(Equity['leading_a'].iloc[row],Equity['leading_b'].iloc[row]) and (Equity['close'].iloc[row] <= max(Equity['leading_a'].iloc[row],Equity['leading_b'].iloc[row]))):
                Place_Order(Instrument_ID,date = Equity.index[row],CMP = Equity['close'][row],signal = "SELL",quantity = -100) 
                last_order_placed = None
                last_order_price = 0
            else :
                Place_Order(Instrument_ID,date = Equity.index[row],CMP = Equity['close'][row],signal = "BUY",quantity = 100)
                last_order_placed = "BUY"
                last_order_price = Equity['close'][row]
                
        
        else :
            if(Equity['close'].iloc[row-1] < min(Equity['leading_a'].iloc[row],Equity['leading_b'].iloc[row]) and (Equity['close'].iloc[row] >= min(Equity['leading_a'].iloc[row],Equity['leading_b'].iloc[row]))):
                pass
            else :
                Place_Order(Instrument_ID,date = Equity.index[row],CMP = Equity['close'][row],signal = "SELL",quantity = -100)
                last_order_placed = "SELL"
                last_order_price = Equity['close'][row]
              

def ATR_strategy(Equity,Instrument_ID):
    Equity['ATR'] = ATR(Equity,14)
    ema = EMA(Equity,20)
    last_order_placed = None
    last_order_price = 0
    for row in range(1,len(Equity)):
        if Equity['close'].iloc[row]> Equity['close'].iloc[row-1] and Equity['ATR'][row]>ema[row]:
            if last_order_placed == "BUY":
                pass
            elif last_order_placed == None:
                Place_Order(Instrument_ID,date = Equity.index[row],CMP = Equity['close'][row],signal = "BUY",quantity = 100)
                last_order_placed = "BUY"
                last_order_price =Equity['close'].iloc[row]
            else :
                Place_Order(Instrument_ID,date = Equity.index[row],CMP = Equity['close'][row],signal = "BUY",quantity = 100)
                last_order_placed = None
                last_order_price =0
     
        elif  Equity['ATR'][row]<ema[row] and  Equity['close'].iloc[row]<Equity['close'].iloc[row-1]:
            if last_order_placed== "SELL" :
                pass
            elif last_order_placed == None:
                Place_Order(Instrument_ID,date = Equity.index[row],CMP = Equity['close'][row],signal = "SELL",quantity = -100)
                last_order_placed = "SELL"
                last_order_price =Equity['close'].iloc[row]
            else :
                Place_Order(Instrument_ID,date = Equity.index[row],CMP = Equity['close'][row],signal = "BUY",quantity = 100)
                last_order_placed = None
                last_order_price =0   


def MACD_strategy(Equity,Instrument_ID):
    last_order_placed = None
    last_order_price = 0
    Equity = MACD(Equity,12,26,9)
    df = Equity.copy()
    for row in range(len(df)):
            if df['MACD'].iloc[row-1]<df['Signal'].iloc[row-1] and df['MACD'].iloc[row]>df['Signal'].iloc[row]:
                if last_order_placed == "BUY":
                    pass
                elif last_order_placed == "None":
                    Place_Order(Instrument_ID,date = df.index[row],CMP = df['close'][row],signal = "BUY",quantity = 100)
                    last_order_price = df['close'][row]
                    last_order_placed = "BUY"
                else:
                    Place_Order(Instrument_ID,date = df.index[row],CMP = df['close'][row],signal = "BUY",quantity = 100)
                    last_order_price = 0
                    last_order_placed = None
                    
            elif df['MACD'].iloc[row-1]>df['Signal'].iloc[row-1] and df['MACD'].iloc[row]<df['Signal'].iloc[row]:
                if last_order_placed == "SELL":
                    pass
                elif last_order_placed== "None":
                    Place_Order(Instrument_ID,date = df.index[row],CMP = df['close'][row],signal = "SELL",quantity = -100)
                    last_order_price = df['close'][row]
                    last_order_placed = "BUY"
                else:
                    Place_Order(Instrument_ID,date = df.index[row],CMP = df['close'][row],signal = "SELL",quantity = -100)
                    last_order_price = 0
                    last_order_placed = None

def Stochastic_Strategy(Equity,Instrument_ID):
    last_order_placed = None
    last_order_price = 0
    Equity = StochasticOscillator(Equity,window  = 3,span = 14)
    for row in range(len(Equity)):
        if Equity['%k'].iloc[row]> Equity['%d'].iloc[row] and Equity['close'].iloc[row] > Equity['close'].iloc[row-1]:
            if last_order_placed == "BUY":
                pass
            elif last_order_placed == None:
                Place_Order(Instrument_ID,date = Equity.index[row],CMP = Equity['close'][row],signal = "BUY",quantity = 100)
                last_order_placed = "BUY"
                last_order_price =Equity['close'].iloc[row]
            else :
                Place_Order(Instrument_ID,date = Equity.index[row],CMP = Equity['close'][row],signal = "BUY",quantity = 100)
                last_order_placed = None
                last_order_price =0
     
        elif Equity['%k'].iloc[row]> Equity['%d'].iloc[row] and Equity['close'].iloc[row] > Equity['close'].iloc[row]:
            if last_order_placed== "SELL" :
                pass
            elif last_order_placed == None:
                Place_Order(Instrument_ID,date = Equity.index[row],CMP = Equity['close'][row],signal = "SELL",quantity = -100)
                last_order_placed = "SELL"
                last_order_price =Equity['close'].iloc[row]
            else :
                Place_Order(Instrument_ID,date = Equity.index[row],CMP = Equity['close'][row],signal = "BUY",quantity = 100)
                last_order_placed = None
                last_order_price =0       
            
