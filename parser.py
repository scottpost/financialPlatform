from googlefinance import getQuotes
from yahoo_finance import Share
import time
import json
import sqlite3

con = sqlite3.connect("data.db")
cur = con.cursor()

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