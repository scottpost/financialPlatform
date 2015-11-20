#   _ __   __ _ _ __ ___  ___ _ __ 
#  | '_ \ / _` | '__/ __|/ _ \ '__|
#  | |_) | (_| | |  \__ \  __/ |   
#  | .__/ \__,_|_|  |___/\___|_|   
#  |_| 
#

#==================================================================================================================================
# IMPORTS & CONFIGURATION
#==================================================================================================================================   

from googlefinance import getQuotes
from yahoo_finance import Share
import time
import sqlite3
con = sqlite3.connect("data.db")
cur = con.cursor()
STOCKS = ["VDSI", "TASR", "S", "GS", "MDXG", "SBUX", "AAPL", "DUST", "NUGT", "SPY", "ATVI", "SUNE", "GE"]

#==================================================================================================================================
# PARSING FUNCTIONS
#==================================================================================================================================

def parseMarketData(stocks = STOCKS):
  turn = 0
  while(True):  
    for stock in stocks:
      parseStockData(stock, turn)
    turn += 1
    time.sleep(60)

#start when the market opens 
def parseStockData(name, turn):
  yahooStock = Share(name)
  #per day
  avgDayVol = yahooStock.get_avg_daily_volume()
  avg50Day = yahooStock.get_50day_moving_avg()
  avg200Day = yahooStock.get_200day_moving_avg()
  #per minute
  price = yahooStock.get_price()
  change = yahooStock.get_change()
  volume = yahooStock.get_volume()
  shortRatio = yahooStock.get_short_ratio()
  print name, price, change, volume
  cur.execute("INSERT or IGNORE INTO stocks VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (turn, name, price, change, volume, shortRatio, avgDayVol, avg50Day, avg200Day))
  con.commit()

#==================================================================================================================================
# 
#==================================================================================================================================                       

parseMarketData()





