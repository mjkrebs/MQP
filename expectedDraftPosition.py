import xlrd
import xlsxwriter
from random import randint
import numpy as np

#function which can get any metric based on the parameter, calls the appropriate function.
#currently only supports percentile
def getPlayerMetricCareer(name,metric, year):
	if(metric == "percentile"):
		value = getPercentileMetricCareer(name, year)
	else:
		print("This is not a valid metric.")
	return value

#go through all percentile files, if found, add the value to a cumulative and increment a count. 
#return a pair [cumulative percentile, numSeasons]. TO
def getPercentileMetricCareer(name, rookieYear):
	cumulative = 0
	numSeasons = 0
	for year in range(rookieYear,2018):
		master = xlrd.open_workbook("Resources/" + str(year) + "/Percentile_" + str(year) + ".xlsx")
		m_sheet = master.sheet_by_index(0)
		for i in range(1,m_sheet.nrows):
			if(name == m_sheet.cell(i,0).value):
				cumulative = cumulative + m_sheet.cell(i,1).value
				numSeasons = numSeasons + 1
				break
	return cumulative, numSeasons

#creates a set of all players. cyrrently bottlenecks
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

#look up name in draft workbook. 61 == undrafted (rookie year == 1990)
def getPlayerDraftPosn(playerName):
	for year in range(1990,2019):
		master = xlrd.open_workbook("Resources/" + str(year) + "/Draft_" + str(year) + ".xlsx")
		m_sheet = master.sheet_by_index(0)
		for i in range(1,m_sheet.nrows):
			result = m_sheet.cell(i,2).value
			if(result == playerName):
				draftPos = m_sheet.cell(i,0).value
				return int(draftPos), year
	return 61, 1990

#given a draft position and name of a metric, will go into that workbook and return the average value.
def getAverageFromCol(draftPosition, metric):
	master = xlrd.open_workbook("Resources/PlayersByDraftPosition.xlsx")
	worksheet = master.sheet_by_name("Pick " + str(draftPosition))
	numRows = worksheet.nrows
	numCols = worksheet.ncols
	colNum = -1
	result = 0
	divisor = 0
	for i in range(0,numCols):
		if(worksheet.cell(0,i).value == "metric=" + metric):
			colNum = i
	if(colNum == -1):
		return -1
	for n in range(1,numRows):
		result = result + worksheet.cell(n,colNum).value
		divisor = divisor + 1
	return result / divisor

#creates the master workbook, adds the percentile metric 
#(this takes an extremely long time to run currently, needs optimization)
def createWorkbookAndAddPercentile(playerSet):
	playersByDraftPosition = createWorkbook()
	#currentRow tracks the correct row to insert the next player for each pick. just an array of ones initially.
	currentRow = np.ones(61, dtype=int)

	for playerName in playerSet:
		#add lines to get metric values here

		



		draftPos, year = getPlayerDraftPosn(playerName)
		#easy lookup in same order as playerSet.
		playerDraftPosnSet.add(draftPos)
		playerRookieYearSet.add(year)

		
		#open the excel file to the right worksheet
		worksheet = playersByDraftPosition.get_worksheet_by_name("Pick " + str(draftPos))
		
		#add name
		worksheet.write(currentRow[draftPos-1],0,playerName)

		#add rookie year
		worksheet.write(currentRow[draftPos-1],1,year)


		#add param for rookie year
		cumulativePercentileValue,numSeasons = getPlayerMetricCareer(playerName, "percentile", year)
		if(numSeasons == 0):
			print("NO SEASONS FOUND FOR PERCENTILE STAT: " + playerName)
			numSeasons = 1
		percentileValue = cumulativePercentileValue / numSeasons
		print(playerName + " %val: " + str(percentileValue))

		#add metrics to the same row
		worksheet.write(currentRow[draftPos-1],2, percentileValue)

		
		#increment the count. zero-indexed array so the first pick is the zero'th array, etc. 
		currentRow[draftPos-1] = currentRow[draftPos-1] + 1

	playersByDraftPosition.close()


#start main code

#initial run
playerSet = addPlayers()
playerDraftPosnSet = set()
playerRookieYearSet = set()
createWorkbookAndAddPercentile(playerSet)
#save playerset, draftPosn and rookieYear to csv


#subsequent runs
#import sets as a df
#playerSet = col1
#draftPosnSet = col2
#rookieYear = col3 

playerNameAndDraftPosnDict = dict(zip(playerSet,playerDraftPosnSet))

for i in range(1,62):
	print(getAverageFromCol(i,"percentile"))


