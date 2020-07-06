# SAMPLE USER BUILD STRATEGY

#import BACKTESTENGINE as bt

Instrument_ID='EUR_USD'             # DEFINE INSTRUMENT NAME
Timeframe='15T'                     # DEFINE CANDLE STICK TIMEFRAME , use T for Mins and S for seconds and D for day and M for month conversion e.g 15T = 15 Min

Equity=Instruments(Instrument_ID,Timeframe) # GET OHLCV DATA

                                    #define your strategy
def is_time_between(dt,start,end):
    return (start <= dt.time() <= end)

def ORB_STRATEGY(records):
  length=len(records)
  last_order_placed = None
  flag=0
  high=1000000
  low=0
  
  for i in range(length):
    
    if is_time_between(records.index[i],datetime.time(9,15),datetime.time(15,29)):
      
      if records.index[i].time() == datetime.time(9,15):
        #print(records.index[i])
        high=records.high[i]
        low=records.low[i]
        flag=1

      if records.close[i]>high and flag==1:
        Place_Order(Instrument_ID,date=records.index[i],CMP=records.close[i],signal="BUY",quantity=100) # For placing order
        last_order_placed = 'BUY'
        flag=0
        
      if records.close[i]<low and flag==1:
        Place_Order(Instrument_ID,date=records.index[i],CMP=records.close[i],signal="SELL",quantity=100) # For placing order
        last_order_placed = 'SELL'
        flag=0
      
      if last_order_placed == 'BUY' :
        if records.close[i] < low:
          Place_Order(Instrument_ID,date=records.index[i],CMP=records.close[i],signal="SELL",quantity=100) # For placing order
          last_order_placed = None
          
      if last_order_placed == 'SELL' :
        if records.close[i] > high:
          Place_Order(Instrument_ID,date=records.index[i],CMP=records.close[i],signal="BUY",quantity=100) # For placing order
          last_order_placed = None
      
      if records.index[i].time() == datetime.time(15,15):
        if last_order_placed == None:
          pass
        elif last_order_placed == 'BUY':
          Place_Order(Instrument_ID,date=records.index[i],CMP=records.close[i],signal="SELL",quantity=100) # For placing order
        elif last_order_placed == 'SELL':
          Place_Order(Instrument_ID,date=records.index[i],CMP=records.close[i],signal="BUY",quantity=100) # For placing order
        last_order_placed = None
#print(Equity.head(195))
ORB_STRATEGY(Equity)
Performance_metrics(Instrument_ID)                                   #Get the Performance metrics calculated
