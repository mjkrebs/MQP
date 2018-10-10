import xlrd
import xlsxwriter
import numpy as np
import pandas as pd

#function which can get any metric based on the parameter, calls the appropriate function.
#currently only supports percentile
#NOTE: RETURNS CUMULATIVE VALUE & NUMSEASONS (seasonsplayed)
def getPlayerCumulativeMetricCareer(name,metric, year):
	if(metric == "percentile"):
		cumValue, numSeasons = getPercentileMetricCareer(name, year)
		if(numSeasons == 0):
			return cumValue, 1
	else:
		print("This is not a valid metric.")
	return 0,0

#go through all percentile files, if found, add the value to a cumulative and increment a count. 
#return a pair [cumulative percentile, numSeasons]. TO
def getPercentileMetricCareer(name, rookieYear):
	cumulative = 0
	numSeasons = 0
	if(rookieYear == 1989):
		rookieYear+=1
	for year in range(rookieYear,2018):
		master = xlrd.open_workbook("Resources/" + str(year) + "/Percentile_" + str(year) + ".xlsx")
		m_sheet = master.sheet_by_index(0)
		for i in range(1,m_sheet.nrows):
			if(name == m_sheet.cell(i,0).value):
				cumulative = cumulative + m_sheet.cell(i,1).value
				numSeasons += 1
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
			result = m_sheet.cell(i,1).value
			if(result not in players):
				players.add(result)       
				x = x+1
	return players

#look up name in draft workbook. 61 == undrafted (rookie year == 1989)
def getPlayerDraftPosn(playerName):
	for year in range(1990,2019):
		master = xlrd.open_workbook("Resources/" + str(year) + "/Draft_" + str(year) + ".xlsx")
		m_sheet = master.sheet_by_index(0)
		for i in range(1,m_sheet.nrows):
			result = m_sheet.cell(i,2).value
			if(result == playerName):
				draftPos = m_sheet.cell(i,0).value
				return int(draftPos), year
	return 61, 1989

#given a draft position and name of a metric, will go into that workbook and return the average value.
def getAverageMetric(df, draftPosition, metric):
	df = df.loc[df['draftPosition'] == draftPosition]
	OGsum = 0
	count = 0
	for row in df.itertuples(index=True, name='Pandas'):
		count = count + 1
		OGsum = OGsum + row[metric]
	return OGsum / count




#creates the master workbook
def addMetricToDataframe(playerInfoDataframe,metric):
	metricColumn = list()
	for row in playerInfoDataframe.itertuples(index=True, name='Pandas'):
		draftPos = getattr(row,"draftPosition")
		playerID = getattr(row,"playerID")
		rookieYear = getattr(row,"rookieYear")
		cumulativeMetric, numSeasons = getPlayerCumulativeMetricCareer(playerID, metric, rookieYear)
		metricValue = cumulativeMetric / numSeasons
		metricColumn.append(metricValue)
		print(playerName + " %val: " + str(metricValue))
	playerInfoDataframe[metric] = metricColumn
	return playerInfoDataframe
		

 

def createOGDataframe():
	playerSet = addPlayers()
	playerDraftPosnSet = list()
	playerRookieYearSet = list()
	for playerID in playerSet:
		draftPos, year = getPlayerDraftPosn(playerID)
		playerDraftPosnSet.append(draftPos)
		playerRookieYearSet.append(year)
		print("PlayerID: " + str(playerID) + "Draft Position: " + str(draftPos) + "Rook Yr: " + str(year))
	OGDataFrame = pd.DataFrame({'playerID' : list(playerSet), 
		'draftPosition' : playerDraftPosnSet, 'rookieYear': playerRookieYearSet})
	OGDataFrame.to_csv('OGDataFrame.csv')
	return OGDataFrame



#start main code




dfWithMetric = addMetricToDataframe(createOGDataframe(), "percentile")

#save playerset, draftPosn and rookieYear to csv




for i in range(1,62):
	print(getAverageMetric(dfWithMetric,i,"percentile"))


