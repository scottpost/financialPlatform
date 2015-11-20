#
#   ___| |_ _ __ __ _| |_ ___  __ _(_) ___  ___ 
#  / __| __| '__/ _` | __/ _ \/ _` | |/ _ \/ __|
#  \__ \ |_| | | (_| | ||  __/ (_| | |  __/\__ \
#  |___/\__|_|  \__,_|\__\___|\__, |_|\___||___/
#

#==================================================================================================================================
# MARKET STRATEGIES
#==================================================================================================================================

def randomStrategy(portfolio, data):
  portfolio.sellAll(data)
  for x in range(2):
    name = data.randomStockData()['name']
    position = Position(name, 1, data.currentTurn)
    if not portfolio.buyPosition(position, data):
      break

def buyAndHoldStrategy(portfolio, data, startTurn = 1):
  if data.currentTurn == startTurn:
    for stockData in data.stocks:
      name = stockData[str(startTurn)]['name']
      position = Position(name, 1, data.currentTurn)
      if not portfolio.buyPosition(position, stockData):
        break

#==================================================================================================================================
# END
#==================================================================================================================================