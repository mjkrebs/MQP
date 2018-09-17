import xlrd
import xlsxwriter
from random import randint
import numpy as np

#function which can get any metric based on the parameter, calls the appropriate function.
#currently only supports percentile
def getPlayerMetricCareer(name,metric):
	if(metric == "percentile"):
		value = getPercentileMetricCareer(name)
	else:
		print("This is not a valid metric.")
	return value

#go through all percentile files, if found, add the value to a cumulative and increment a count. 
#return a pair [cumulative percentile, numSeasons]. currently returns a random number for testing.
def getPercentileMetricCareer(name):
	return randint(1,101)

#creates a set of all players.
def addPlayers():
	players = set()
	x = 1
	for year in range(1990,2019):
		master = xlrd.open_workbook("Resources/" + str(year) + "/Master_" + str(year) + ".xlsx")
		m_sheet = master.sheet_by_index(0)
		for i in range(1,m_sheet.nrows):
			result = m_sheet.cell(i,0).value
			if(result not in players):
				players.add(result)       
				x = x+1
	return players


#create a workbook with 61 worksheets, one for each draft pick AND one for undrafted.
def createWorkbook():
	workbook = xlsxwriter.Workbook("Resources/PlayersByDraftPosition.xlsx")
	for x in range(1,62):
		worksheet = workbook.add_worksheet("Pick " + str(x))
		worksheet.write(0,0,"Name")
		worksheet.write(0,1,"metric=percentile")
	return workbook

#look up name in draft workbook. 61 == undrafted.
def getPlayerDraftPosn(playerName):
	for year in range(1990,2019):
		master = xlrd.open_workbook("Resources/" + str(year) + "/Draft_" + str(year) + ".xlsx")
		m_sheet = master.sheet_by_index(0)
		for i in range(1,m_sheet.nrows):
			result = m_sheet.cell(i,2).value
			if(result == playerName):
				draftPos = m_sheet.cell(i,0).value
				return int(draftPos)
	return 61




#start code

#this isn't necessary in the end, but for testing just add a switch.
metric = input("enter metric: options = percentile")

playerSet = addPlayers()
playersByDraftPosition = createWorkbook()
#currentRow tracks the correct row to insert the next player for each pick. just an array of ones initially.
currentRow = np.ones(61, dtype=int)

for playerName in playerSet:
	percentileValue = getPlayerMetricCareer(playerName, metric)
	draftPos = getPlayerDraftPosn(playerName)
	#testing print statement
	print("Name: " + playerName + " draftPos: " + str(draftPos) + " percentileValue: " + str(percentileValue))
	#open the excel file to the right worksheet
	worksheet = playersByDraftPosition.get_worksheet_by_name("Pick " + str(draftPos))
	#add name and metric. need to find a way to better abstract this, perhaps create an array of all metrics
	#then write an addRow function.
	worksheet.write(currentRow[draftPos-1],0,playerName)
	worksheet.write(currentRow[draftPos-1],1, percentileValue)
	#increment the count. zero-indexed array so the first pick is the zero'th array, etc. 
	currentRow[draftPos-1] = currentRow[draftPos-1] + 1
playersByDraftPosition.close()



