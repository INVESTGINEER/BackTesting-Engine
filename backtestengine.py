from arctic import Arctic, TICK_STORE
import warnings
import pandas as pd
import numpy as np
#import talib
#from talib.abstract import *
#from talib import abstract
import matplotlib.pyplot as plts
from tabulate import tabulate
from pandas.util.testing import assert_frame_equal


uri = "mongodb://invsto:INVSTOdata@ec2-18-222-142-78.us-east-2.compute.amazonaws.com:27017/arctic?authSource=test"
warnings.filterwarnings("ignore")
store = Arctic(uri)
ARCTIC_NAME = 'loading'
store.initialize_library(ARCTIC_NAME, lib_type=TICK_STORE)
library = store[ARCTIC_NAME]

def round_it(x):
    x=(round(x, 2)*100//5*5)/100
    return x
    
def Instruments(Instrument_ID,Timeframe): 

    Equity=library.read(Instrument_ID)
    Equity=Equity.rename(columns={"o": "open",'h': "high",'l': "low",'c': "close"})

    dopen = pd.DataFrame({'value':Equity.open}, index=pd.DatetimeIndex(Equity.index), dtype=float)
    dhigh = pd.DataFrame({'value':Equity.high}, index=pd.DatetimeIndex(Equity.index), dtype=float)
    dlow = pd.DataFrame({'value':Equity.low}, index=pd.DatetimeIndex(Equity.index), dtype=float)
    dclose = pd.DataFrame({'value':Equity.close}, index=pd.DatetimeIndex(Equity.index), dtype=float)


    #Timeframe='15T'                     # use T for Mins and S for seconds and D for day and M for month conversion e.g 15T = 15 Min

    dopen=dopen.resample(Timeframe).ohlc()
    dhigh=dhigh.resample(Timeframe).ohlc()
    dlow=dlow.resample(Timeframe).ohlc()         
    dclose=dclose.resample(Timeframe).ohlc()            
    dvolume = Equity['volume'].resample(Timeframe).sum()

    df_ohlcv = pd.merge(dopen['value']['open'],dhigh['value']['high'], on=dopen.index)
    df_ohlcv.set_index("key_0", inplace = True)
    df_ohlcv = pd.merge(df_ohlcv,dlow['value']['low'], on=df_ohlcv.index)
    df_ohlcv.set_index("key_0", inplace = True)
    df_ohlcv = pd.merge(df_ohlcv,dclose['value']['close'], on=df_ohlcv.index)
    df_ohlcv.set_index("key_0", inplace = True)
    df_ohlcv = pd.merge(df_ohlcv,dvolume, on=df_ohlcv.index)
    df_ohlcv=df_ohlcv.rename(columns={'key_0':'datetime'})
    df_ohlcv.set_index("datetime", inplace = True)
    df_ohlcv.dropna(inplace = True)
    print(df_ohlcv)
    Equity=df_ohlcv.copy()    
    Equity['open'] = Equity['open'].astype(float)
    Equity['high'] = Equity['high'].astype(float)
    Equity['low'] = Equity['low'].astype(float)
    Equity['close'] = Equity['close'].astype(float)
    #df['DataFrame Column'] = df['DataFrame Column'].astype(float)

    np_open = np.array(Equity.open, dtype='f8')
    np_close = np.array(Equity.close, dtype='f8')
    np_high = np.array(Equity.high, dtype='f8')
    np_low = np.array(Equity.low, dtype='f8')
    np_volume = np.array(Equity.volume, dtype='f8')
    inputs = {
        'open': np_open,
        'high': np_high,
        'low': np_low,
        'close': np_close,
        'volume': np_volume
    }

    return Equity
                          


order_book=[]

def Place_Order(Instrument_ID,date,CMP,signal,quantity):
    global order_book
    if signal=='BUY':
        order_book.append([Instrument_ID,date,'BUY',CMP,quantity])
    elif signal=='SELL':
        order_book.append([Instrument_ID,date,'SELL',CMP,quantity])







def Performance_metrics(Instrument_ID):
    global PROFIT_FACTOR,EQUITY_CURVE
    Instrument_order_book=[]
    Instrument_long_order_book=[]
    Instrument_short_order_book=[]
    for i in range (len(order_book)):
        if order_book[i][0]==Instrument_ID:
            Instrument_order_book.append(order_book[i])

    Instrument_order_book=pd.DataFrame(Instrument_order_book)
    #print(Instrument_order_book)
    Instrument_order_book.columns=['Instrument_ID','date','order_type','order_price','quantity']
    total_return=[]
    total_long_return=[]
    total_short_return=[]
    long_profit=0
    long_loss=0
    short_profit=0
    short_loss=0
    NET_PROFIT=0
    GROSS_PROFIT=0
    GROSS_LOSS=0
    #Instrument_long_order_book.columns=['Instrument_ID','date','order_type','order_price','quantity']
    #Instrument_short_order_book.columns=['Instrument_ID','date','order_type','order_price','quantity']
    
    no_of_buy_trades,no_of_sell_trades,no_of_win_trades,no_of_loss_trades=0,0,0,0
    long_of_loss_trades,short_of_loss_trades,short_of_win_trades,long_of_win_trades=0,0,0,0

    for i in range(1,len(Instrument_order_book),2):
        if Instrument_order_book.order_type[i]=='BUY':
            no_of_sell_trades=no_of_sell_trades+1
            Instrument_short_order_book.append(order_book[i-1])
            Instrument_short_order_book.append(order_book[i])
            change=order_book[i-1][3]-order_book[i][3]
            NET_PROFIT=NET_PROFIT+change
            if change>0:
                no_of_win_trades=no_of_win_trades+1
                short_of_win_trades=short_of_win_trades+1
                short_profit=short_profit+change
                total_return.append(change/order_book[i-1][3])
                total_short_return.append(change/order_book[i-1][3])
                GROSS_PROFIT=GROSS_PROFIT+change
            else:
                no_of_loss_trades=no_of_loss_trades+1
                short_of_loss_trades=short_of_loss_trades+1
                short_loss=short_loss+change
                total_return.append(change/order_book[i-1][3])
                total_short_return.append(change/order_book[i-1][3])
                GROSS_LOSS=GROSS_LOSS+change

        else:
            no_of_buy_trades=no_of_buy_trades+1
            Instrument_long_order_book.append(order_book[i-1])
            Instrument_long_order_book.append(order_book[i])
            change=order_book[i][3]-order_book[i-1][3]
            NET_PROFIT=NET_PROFIT+change
            if change>0:
                no_of_win_trades=no_of_win_trades+1
                long_of_win_trades=long_of_win_trades+1
                long_profit=long_profit+change
                total_return.append(change/order_book[i-1][3])
                total_long_return.append(change/order_book[i-1][3])
                GROSS_PROFIT=GROSS_PROFIT+change
            
            else:
                no_of_loss_trades=no_of_loss_trades+1
                long_of_loss_trades=long_of_loss_trades+1
                long_loss=long_loss+change
                total_return.append(change/order_book[i-1][3])
                total_long_return.append(change/order_book[i-1][3])
                GROSS_LOSS=GROSS_LOSS+change
    
    
    #total_return=[]
    #total_return= pd.DataFrame(Instrument_order_book['order_price'].pct_change())
    total_return=pd.DataFrame(total_return)
    total_return.columns=['returns']
    total_long_return=pd.DataFrame(total_long_return)
    total_long_return.columns=['returns']
    total_short_return=pd.DataFrame(total_short_return)
    total_short_return.columns=['returns']
    PROFIT_FACTOR=GROSS_PROFIT/-(GROSS_LOSS)
    EQUITY_CURVE= (1.0+total_return).cumprod()

    def equity_sharpe(total_return):
        global annualised_sharpe
        # Assume an average annual risk-free rate over the period of 5%
        excess_daily_return =pd.DataFrame(total_return - 0.05/252)

        # Return the annualised Sharpe ratio based on the excess daily returns
        annualised_sharpe=np.sqrt(252) * excess_daily_return.mean() / excess_daily_return.std()
        #print("Sharpe Ratio            ",annualised_sharpe['returns'])
        return annualised_sharpe
    def create_drawdowns(daily_return):

        """
        Calculate the largest peak-to-trough drawdown of the PnL curve
        as well as the duration of the drawdown. Requires that the 
        pnl_returns is a pandas Series.

        Returns:
        drawdown, duration - Highest peak-to-trough drawdown and duration.
        """

        # Calculate the cumulative returns curve 
        # and set up the High Water Mark
        # Then create the drawdown and duration series
        global drawdown
        global duration
        hwm=[0]
        eq_idx = daily_return.index

        drawdown = pd.Series(index = eq_idx)
        duration = pd.Series(index = eq_idx)
        # Loop over the index range
        for t in range(1, len(eq_idx)):

            hwm.append(max(hwm[t-1], daily_return['returns'][t] ))
            drawdown[t]= (hwm[t]-daily_return.iloc[t])
            duration[t]= (0 if drawdown[t] == 0 else duration[t-1]+1)
    
        return drawdown,duration
    

    def value_at_risk(daily_return):
        global var_90,var_95,var_99
        daily_return=daily_return.dropna()
      #plt.figure(figsize=(6,4))
      #plt.hist(daily_return.returns,bins=40)
      #plt.xlabel('RETURNS')
      #plt.ylabel('FREQUENCY')
      #plt.grid(True)
      #plt.show
        daily_return.sort_values('returns', inplace=True,ascending=True)
        var_90=daily_return['returns'].quantile(0.1)
        var_95=daily_return['returns'].quantile(0.05)
        var_99=daily_return['returns'].quantile(0.01)
        return var_90,var_95,var_99

       
    def output_summary():
        print (tabulate([["Sharpe Ratio",annualised_sharpe['returns'],long_annualised_sharpe['returns'],short_annualised_sharpe['returns']],
        ["max drawdown", drawdown.max(),long_drawdown.max(),short_duration.max()],
        ["max duration", duration.max(),long_duration.max(),short_duration.max()],
        ["no of trades",int(len(Instrument_order_book)/2),long_of_win_trades+long_of_loss_trades,short_of_win_trades+short_of_loss_trades],
        ["no of buy trades",no_of_buy_trades,(long_of_win_trades+long_of_loss_trades)/2,(short_of_win_trades+short_of_loss_trades)/2],
        ["no of sell trades",no_of_sell_trades,(long_of_win_trades+long_of_loss_trades)/2,(short_of_win_trades+short_of_loss_trades)/2],
        ["no of winning trades",no_of_win_trades,long_of_win_trades,short_of_win_trades],
        ["no of lossing trades",no_of_loss_trades,long_of_loss_trades,short_of_loss_trades],      
        ["NET PROFIT", NET_PROFIT,long_profit+long_loss,short_profit+short_loss],
        ["GROSS PROFIT", GROSS_PROFIT,long_profit,short_profit],
        ["GROSS LOSS", GROSS_LOSS,long_loss,short_loss],
        ["PROFIT FACTOR", PROFIT_FACTOR,long_profit/-(long_loss),short_profit/-(short_loss)],
        ["var_90",var_90,long_var_90,short_var_90],
        ['var_95',var_95,long_var_95,short_var_95],
        ['var_99',var_99,long_var_99,short_var_99]], headers=['Performance metrics', 'Overall Values','Long position','Short position']))
        print()
        print("--------------------EQUITY CURVE & DRAWDOWN CURVE----------------------")
        plt.figure(figsize=(8,5))
        plt.plot(EQUITY_CURVE.index,EQUITY_CURVE.returns)
        plt.xlabel('NO OF TRADES')
        plt.ylabel('PERCENTAGE RETURN')
        plt.grid(True)
        plt.show
        print("-----------------------------------------------------------------------")
        plt.figure(figsize=(8,5))
        plt.plot(drawdown.index,drawdown)
        plt.xlabel('NO OF TRADES')
        plt.ylabel('DRAWDOWN CURVE')
        plt.grid(True)
        plt.show

    total_annualised_sharpe=equity_sharpe(total_return)
    long_annualised_sharpe=equity_sharpe(total_long_return)
    short_annualised_sharpe=equity_sharpe(total_short_return)
    drawdown,duration=create_drawdowns(total_return)
    long_drawdown,long_duration=create_drawdowns(total_long_return)
    short_drawdown,short_duration=create_drawdowns(total_short_return)    

    var_90,var_95,var_99=value_at_risk(total_return)
    long_var_90,long_var_95,long_var_99=value_at_risk(total_long_return)
    short_var_90,short_var_95,short_var_99=value_at_risk(total_short_return)

    output_summary()
