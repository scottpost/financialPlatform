#       _                 _       _   _             
#   ___(_)_ __ ___  _   _| | __ _| |_(_) ___  _ __  
#  / __| | '_ ` _ \| | | | |/ _` | __| |/ _ \| '_ \ 
#  \__ \ | | | | | | |_| | | (_| | |_| | (_) | | | |
#  |___/_|_| |_| |_|\__,_|_|\__,_|\__|_|\___/|_| |_|
# 

#==================================================================================================================================
# IMPORTS & CONFIGURATION
#==================================================================================================================================

import time
import json
import sqlite3
import strategies 
con = sqlite3.connect("data.db")
cur = con.cursor()                                           

#==================================================================================================================================
# RUN MAIN SIMULATION
#==================================================================================================================================

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

#==================================================================================================================================
# CLASS REPRESENTATIONS
#==================================================================================================================================

class MarketData:
  def __init__(self, turn = 0):
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

  #WE NEED TO GET RID OF THIS STUPID FUNCTION
  def getStockData(turnData, name):
      for stockData in turnData:
        if stockData[1] == name:
          return stockData
      return None

#==================================================================================================================================
# 
#==================================================================================================================================                       