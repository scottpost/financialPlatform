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

#==================================================================================================================================
# RUN MAIN PARSE FUNCTION
#==================================================================================================================================

#start when the market opens 
def collectData(name):
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
  cur.execute("INSERT or IGNORE INTO stocks VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (time.time(), name, price, change, volume, shortRatio, avgDayVol, avg50Day, avg200Day))
  con.commit()
  
#==================================================================================================================================
# 
#==================================================================================================================================                       