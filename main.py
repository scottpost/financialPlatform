#                   _             
#   _ __ ___   __ _(_)_ __  
#  | '_ ` _ \ / _` | | '_ \ 
#  | | | | | | (_| | | | | |
#  |_| |_| |_|\__,_|_|_| |_|
# 

#==================================================================================================================================
# IMPORTS & CONFIGURATION
#==================================================================================================================================

import sqlite3
import simulation
import strategies

#==================================================================================================================================
# MAIN SIMULATION FUNCTION
#==================================================================================================================================

sqlConnection = sqlite3.connect("data.db")
sqlCursor = sqlConnection.cursor()
sqlCursor.execute('SELECT MIN(turn) FROM stocks')
defaultStartTurn = sqlCursor.fetchone()[0]
sqlCursor.execute('SELECT MAX(turn) FROM stocks')
defaultEndTurn = sqlCursor.fetchone()[0]
defaultTurnIncrement = 1
defaultStartingCash = 1000

reset = 'yes'

while reset == 'yes' or reset == 'y' or reset == 'Yes' or reset == 'Y':

  startTurn = raw_input("\nStart Turn [" + str(defaultStartTurn) + "]: ")
  if startTurn == '':
    startTurn = defaultStartTurn
  else:
    startTurn = int(startTurn)

  endTurn = raw_input("End Turn: [" + str(defaultEndTurn) + "]: " )
  if endTurn == '':
    endTurn = defaultEndTurn
  else:
    endTurn = int(endTurn)

  turnIncrement = raw_input("Turn Increment [" + str(defaultTurnIncrement) + "]: ")
  if turnIncrement == '':
    turnIncrement = defaultTurnIncrement
  else:
    turnIncrement = int(turnIncrement)

  startingCash = raw_input("Starting Cash [" + str(defaultStartingCash) + "]: ")
  if startingCash == '':
    startingCash = defaultStartingCash
  else:
    startingCash = int(startingCash)

  buyAndHoldPortfolio = simulation.Portfolio(startingCash)
  buyAndHoldROI = simulation.runSimulation(buyAndHoldPortfolio, strategies.buyAndHoldStrategy, startTurn, endTurn, turnIncrement)
  print "The Buy and Hold Strategy ROI was: " + str(100 * buyAndHoldROI) + "%"

  randomSimulationCount = raw_input("Number of Random Simulations [100]: ")
  if randomSimulationCount == '':
    randomSimulationCount = 100
  else:
    randomSimulationCount = int(randomSimulationCount)

  randomWins = 0
  totalRandomROI = 0
  for i in range(randomSimulationCount):
    randomPortfolio = simulation.Portfolio(startingCash)
    randomROI = simulation.runSimulation(randomPortfolio, strategies.randomStrategy, startTurn, endTurn, turnIncrement)
    totalRandomROI += randomROI
    if randomROI > buyAndHoldROI:
      randomWins += 1

  print "The Random Strategy beat the Buy and Hold Strategy at a rate of: " + str(100 * randomWins / randomSimulationCount) + "% "
  print "With an Average ROI of: " + str(totalRandomROI / randomSimulationCount)

  reset = raw_input("Do you want to start over ['y']? ")

#==================================================================================================================================
# END
#==================================================================================================================================