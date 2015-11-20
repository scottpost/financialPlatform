#       _             _             _           
#   ___| |_ _ __ __ _| |_ ___  __ _(_) ___  ___ 
#  / __| __| '__/ _` | __/ _ \/ _` | |/ _ \/ __|
#  \__ \ |_| | | (_| | ||  __/ (_| | |  __/\__ \
#  |___/\__|_|  \__,_|\__\___|\__, |_|\___||___/
#                             |___/             

#==================================================================================================================================
# MARKET STRATEGIES
#==================================================================================================================================

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

#==================================================================================================================================
# 
#==================================================================================================================================                       
