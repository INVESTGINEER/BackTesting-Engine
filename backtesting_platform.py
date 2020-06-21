#SMA CROSSOVER-STRATEGY
#Instrument_ID AVAILABLE ['20MICRONS', '21STCENMGM', '3IINFOTECH', '3MINDIA', '5PAISA', '63MOONS', 'A2ZINFRA', 'AARTIDRUGS', 'AARTIIND', 'AARVEEDEN', 'AAVAS', 'ABAN', 'ABB', 'ABBOTINDIA', 'ABCAPITAL', 'ABFRL', 'ABMINTLTD', 'ACC', 'ACCELYA', 'ADANIENT', 'ADANIGAS', 'ADANIGREEN', 'ADANIPORTS', 'ADANIPOWER', 'ADANITRANS', 'ADFFOODS', 'ADHUNIKIND', 'ADORWELD', 'ADROITINFO', 'ADSL', 'ADVANIHOTR', 'ADVENZYMES', 'AEGISCHEM', 'AFFLE', 'AGARIND', 'AGCNET', 'AGRITECH']
'''
!pip install arctic
!wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
!tar -xzvf ta-lib-0.4.0-src.tar.gz
%cd ta-lib
!./configure --prefix=/usr
!make
!make install
!pip install Ta-Lib
'''

import backtestengine as bt
import bt_strategy as bts

Instrument_ID='EUR_USD'#'ACC'
Timeframe='15T'                     # use T for Mins and S for seconds and D for day and M for month conversion e.g 15T = 15 Min
records=bt.Instruments(Instrument_ID,Timeframe)

bts.sma_crossover (records,Instrument_ID)
#bts.RSI_STRATEGY(records,Instrument_ID,periods=14)

bt.Performance_metrics(Instrument_ID)