#       _                 _       _   _             
#   ___(_)_ __ ___  _   _| | __ _| |_(_) ___  _ __  
#  / __| | '_ ` _ \| | | | |/ _` | __| |/ _ \| '_ \ 
#  \__ \ | | | | | | |_| | | (_| | |_| | (_) | | | |
#  |___/_|_| |_| |_|\__,_|_|\__,_|\__|_|\___/|_| |_|
# 

#==================================================================================================================================
# IMPORTS & CONFIGURATION
#==================================================================================================================================

import sqlite3
import random

#==================================================================================================================================
# CLASSES
#==================================================================================================================================

class MarketData:
  def __init__(self, turn = 0, turnIncrement = 1):
    sqlConnection = sqlite3.connect("data.db")
    self.sqlCursor = sqlConnection.cursor()
    self.currentTurn = turn
    self.turns = {}
    self.numStocks = 0
    self.stocks = {}
    self.addTurn(turnIncrement)

  def addTurn(turnIncrement = 1):
    t = (self.currentTurn,)
    self.sqlCursor.execute('SELECT * FROM stocks WHERE turn=?', t)
    arrayRows = self.sqlCursor.fetchall()
    turn = {}
    self.numStocks = 0
    for row in arrayRows:
      name = row[1]
      price = row[2]
      dictRow = {'name' : name, 'turn' : self.currentTurn, 'price' : price}
      turn[name] = dictRow
      stockData = self.stocks[name]
      if stockData:
        stockData[str(self.currentTurn)] = dictRow
      else:
        self.stocks[name][str(self.currentTurn)] = dictRow
      self.numStocks += 1
    self.turns[str(self.currentTurn)] = turn
    self.currentTurn += turnIncrement
    #self.turns['6']['APPL']
    #self.stocks['TASR']['3']

    def getPrice(self, name, turn = self.currentTurn):
      return self.stocks[name][str(turn)]['price']

    def getRandomStockData(self, turn = self.currentTurn):
      return random.choice(self.turns[str(turn)])

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
  def __init__(self, name, quantity, turn):
    self.name = name
    self.quantity = quantity
    self.buyTurn = turn
  
class Portfolio:
  def __init__(self, cash = 1000, cashDelay = 0, positions = {}, tradeFee = 0):
    self.cash = cash
    self.cashDelay = cashDelay
    self.positions = positions
    self.delayedCashes = []
    self.tradeFee = tradeFee
    self.history = []
    self.startingValue = cash
  
  def getPositionsValue(self, data):
    total = 0
    for position in self.positions:
      total += data.getPrice(position.name)
    return total

  def getTotalValue(self, data):
    return self.getPositionsValue(data) + self.cash

  def getROI(self, data):
    return (self.getTotalValue(data) - self.startingValue) / self.startingValue

  def buyPosition(self, position, data):
    currentValue = data.getPrice(position.name)
    if currentValue > self.cash:
      return False  
    currentPosition = self.positions[position.name]
    if currentPosition:
      currentPosition.quantity += position.quantity
      currentPosition.buyTurn = data.currentTurn
    else:
      self.positions[position.name] = position
    self.cash -= currentValue
    return True

  def sellPosition(self, position, data):
    currentPosition = self.positions[position.name]
    if not currentPosition:
      return False
    if position.quantity > currentPosition.quantity:
      return False
    currentPosition.quantity -= position.quantity
    if currentPosition.quantity == 0:
      positions.pop(position.name)
    self.cash += position.quantity * data.getPrice(position.name)
    return True

  def sellAll(self, data):
    for position in self.positions:
      self.sellPosition(position, data)

#==================================================================================================================================
# MAIN SIMULATION FUNCTION
#==================================================================================================================================

def runSimulation(portfolio, strategy, startTurn = 0, endTurn = 47, turnIncrement = 1):
  data = MarketData(startTurn, turnIncrement)
  while data.currentTurn <= endTurn:
    strategy(portfolio, data)
    data.addTurn(turnIncrement)
  #print "This portfolio had an ROI of " + str(portfolio.getROI(data)) +"%"
  return portfolio.getROI(data)

#==================================================================================================================================
# END
#==================================================================================================================================