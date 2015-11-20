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
