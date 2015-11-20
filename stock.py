from googlefinance import getQuotes
from yahoo_finance import Share
from datetime import datetime
import sched
import time
import json
import os
import sqlite3
import random

con = sqlite3.connect("data.db")
cur = con.cursor()

class MarketData:
  __init__(self, turn = 0):
    sqlConnection = sqlite3.connect("data.db")
    self.sqlCursor = sqlConnection.cursor()
    self.turns = []
    self.data = {}
    self.addTurn()

  def addTurn(turnIncrement = 1):
    t = (self.turn,)
    cur.execute('SELECT * FROM stocks WHERE turn=?', t)
    arrayRows = cur.fetchall()
    turn = []
    for row in arrayRows:
      dictRow = {'name' : row[1], 'price' : row[2], 'turn' : row[3]}
      turn.append(dictRow)
      stockData = self.data[row[1]]
      if stockData:
        stockData.append(dictRow)
      else:
        self.data[row[1]] = [dictRow]
    self.turns.append(turn)
    self.turn += turnIncrement


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

def randomStrategy(portfolio, turnData, currentDate):
    portfolio.sellAll(turnData)
    for x in range(2):
      stockData = random.choice(turnData)
      stock = stockData[1]
      position = Position(stock, 1, currentDate)
      if (portfolio.buyPosition(position, stockData) == "No Buy"):
        break

def buyAndHoldStrategy(portfolio, turnData, currentDate):
  if currentDate == 1:
    for stockData in turnData:
      stock = stockData[1]
      position = Position(stock, 1, currentDate)
      if (portfolio.buyPosition(position, stockData) == "No Buy"):
        break

def getStockData(turnData, name):
    for stockData in turnData:
      if stockData[1] == name:
        return stockData
    return None

def runSimulation(portfolio, strategy, startTurn = 1, endTurn = 47, turnIncrement = 1):
  #print "This portfolio started with $" + str(portfolio.cash)
  turn = startTurn
  turnData = []
  while (turn <= endTurn):
    turnData = retrieveData(turn)
    strategy(portfolio, turnData, turn)
    turn += 1
  #print "This portfolio had an ROI of " + str(portfolio.getROI(turnData)) +"%"
  return portfolio.getROI(turnData)

class DelayedCash:
  def __init__(self, cash, delay):
    self.cash = cash
    self.delay = delay
  
  def reduceDelayGetCash(self, days = 1):
    self.delay -= days
    if self.delay <= 0:
      return self
    else:
      return null

    
class Position:
  def __init__(self, name, quantity, currentDate):
    self.name = name
    self.quantity = quantity
    self.buyDate = currentDate

  def __repr__(self):
    return str([self.name, self.quantity])
    
  def getValue(self):
    return self.quantity * getPrice(self.name)
  
  def getValue(self, time):
    return self.quantity * getPrice(self.name, time)
  
  
class Portfolio:
  def __init__(self, cash, cashDelay, positions, tradeFee = 0):
    self.cash = cash
    self.cashDelay = cashDelay
    self.positions = positions
    self.delayedCashes = []
    self.tradeFee = tradeFee
    self.history = []
    self.startingValue = cash
  
  def getPositionsValue(self, turnData):
    total = 0
    for position in self.positions:
      total += getStockData(turnData, position.name)[2]
    return total

  def getTotalValue(self, turnData):
    return self.getPositionsValue(turnData) + self.cash

  def isHolding(self, position):
    for currentPosition in self.positions:
      if currentPosition.name is position.name:
        return currentPosition
    return None

  def getROI(self, turnData):
    return (self.getTotalValue(turnData) - self.startingValue) / self.startingValue
    
  def buyPosition(self, position, stockData):
    currentValue = stockData[2]
    if currentValue > self.cash:
      return 'No Buy'  
    currentPosition = self.isHolding(position)
    if currentPosition:
      currentPosition.quantity += position.quantity
      print "Bought " + currentPosition.name
    else:
      self.positions.append(position)
      print "Bought " + position.name
    self.cash -= currentValue
    return 'Buy'

  def sellPosition(self, position, stockData):
    currentPosition = self.isHolding(position)
    if not currentPosition:
      return 'No Sell'
    if currentPosition.quantity < position.quantity:
      return 'No Sell'
    currentPosition.quantity -= position.quantity
    self.cash += position.quantity * stockData[2]
    print "Sold " + currentPosition.name
    return 'Sell'

  def sellAll(self,turnData):
    for position in self.positions:
      self.sellPosition(position, getStockData(turnData, position.name))

for i in range(1):
  portfolio1 = Portfolio(250, 0, [])
  roi = runSimulation(portfolio1, randomStrategy)

