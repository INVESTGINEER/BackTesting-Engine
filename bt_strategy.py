import backtestengine as bt
import bt_indicator as bti


def sma_crossover (Equity,Instrument_ID):
  span1=7
  span2=15
  value1=bti.SMA(Equity,span1)
  value2=bti.SMA(Equity,span2)

  bt.Crossover_strategy(Equity.close,Equity.index,value1,value2,Instrument_ID)

def hma_crossover (Equity,Instrument_ID):
  span1=7
  span2=15
  value1=bti.HMA(Equity,span1)
  value2=bti.HMA(Equity,span2)

  print(Equity.close)
  bt.Crossover_strategy(Equity.close,Equity.index,value1,value2,Instrument_ID)

def ema_crossover (Equity,Instrument_ID):
  span1=7
  span2=15
  value1=bti.EMA(Equity,span1)
  value2=bti.EMA(Equity,span2)

  print(Equity.close)
  bt.Crossover_strategy(Equity.close,Equity.index,value1,value2,Instrument_ID)

def dema_crossover (Equity,Instrument_ID):
  span1=7
  span2=15
  value1=bti.DEMA(Equity,span1)
  value2=bti.DEMA(Equity,span2)

  print(Equity.close)
  bt.Crossover_strategy(Equity.close,Equity.index,value1,value2,Instrument_ID)

def RSI_STRATEGY(records,Instrument_ID=0,periods=14):

  last_order_placed = None
  last_order_price = 0

  rsi= bti.RSI(records,periods)
  for i in range(periods+2,len(records)):
    #Placing buy order
    if rsi[i]>20 and rsi[i-1]<20 and last_order_placed!='BUY':
      #print("Enter buy ",rsi[i],"    ",rsi[i-1],"    ",records.index[i])
      bt.Place_Order(Instrument_ID,date=records.index[i],CMP=records.close[i],signal="BUY",quantity=100) 
      last_order_placed='BUY'
      last_order_price=records.close[i]
    
    #Placing sell order
    if rsi[i]<80 and rsi[i-1]>80 and last_order_placed!='SELL':
      #print("Enter sell ",rsi[i],"    ",rsi[i-1],"    ",records.index[i])
      bt.Place_Order(Instrument_ID,date=records.index[i],CMP=records.close[i],signal="SELL",quantity=-100)
      last_order_placed='SELL'
      last_order_price=records.close[i]
    
    #Closing sell order
    if rsi[i]<20 and rsi[i-1]>20 and last_order_placed=='SELL':
      #print("Close sell ",rsi[i],"    ",rsi[i-1],"    ",records.index[i])
      bt.Place_Order(Instrument_ID,date=records.index[i],CMP=records.close[i],signal="BUY",quantity=100) 

      last_order_placed=None
      last_order_price=0
    
    #Closing buy order
    if rsi[i]>80 and rsi[i-1]<80 and last_order_placed=='BUY':
      #print("Close buy ",rsi[i],"    ",rsi[i-1],"    ",records.index[i])
      bt.Place_Order(Instrument_ID,date=records.index[i],CMP=records.close[i],signal="SELL",quantity=-100) 

      
      last_order_placed=None
      last_order_price=0

def KELTNER_STRATEGY(records,Instrument_ID=0,periods=14):
    KELTNER_CHANNEL=bti.KeltnerChannel(records,periods)
    KELTNER_CHANNEL.rename(columns={'Keltner Lower Band':'lower'}, inplace=True)
    KELTNER_CHANNEL.rename(columns={'Keltner Upper Band':'upper'}, inplace=True)
    BAND_STRATEGY(records,KELTNER_CHANNEL,Instrument_ID)

def BOLLINGER_STRATEGY(records,Instrument_ID=0,periods=14):
    BOLLINGER_BAND=bti.BollingerBands(records,periods)
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
                bt.Place_Order(Instrument_ID,date=records.index[i],CMP=Equity.close[i],signal="BUY",quantity=100) 
                last_order_placed='BUY'
            elif last_order_placed=='SELL':    
                bt.Place_Order(Instrument_ID,date=records.index[i],CMP=Equity.close[i],signal="BUY",quantity=100) 
                bt.Place_Order(Instrument_ID,date=records.index[i],CMP=Equity.close[i],signal="BUY",quantity=100) 
                last_order_placed='BUY'


          
        #Placing sell order and closing buy order
        if Equity.close[i]>band['upper'][i] :
            if last_order_placed=='BUY':
                bt.Place_Order(Instrument_ID,date=records.index[i],CMP=Equity.close[i],signal="SELL",quantity=-100) 
                bt.Place_Order(Instrument_ID,date=records.index[i],CMP=Equity.close[i],signal="SELL",quantity=-100) 
                last_order_placed='SELL'
            elif last_order_placed==None: 
                bt.Place_Order(Instrument_ID,date=records.index[i],CMP=Equity.close[i],signal="SELL",quantity=-100)
                last_order_placed='SELL'
            elif last_order_placed=='SELL':    
                pass  


