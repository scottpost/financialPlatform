from googlefinance import getQuotes
from yahoo_finance import Share
from datetime import datetime
import sched
import time
import json
import os
import sqlite3
import random

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
