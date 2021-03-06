#code to normalize all metrics from single season master sheets. 

#one metric normalize:
#loop through all the files
#find the maximum value of the metric
#loop through all the files
#set each value to value / maximum * 100


import pandas as pd 
import math
#returns a metric value as a proportion of the maximum value, max = 100
def normalizeFunction(value,maxValue):
	return (value / maxValue) * 100


#finds the maximum value of the given metric, then normalizes all values and saves in the master season sheets.
def	normalizeMetric(metric):
	maxVal = -100
	for year in range(1990,2019):
		df = master_season_dfs[year-1990]
		for row in df.itertuples():
			metricValue = getattr(row,metric)
			if(metricValue > maxVal):
				maxVal = metricValue
	print('Max Value: ' + str(maxVal))
	for year in range(1990,2019):
		df = master_season_dfs[year-1990]
		df['normalized_' + metric] = df.apply(lambda row: normalizeFunction(row[metric], maxVal), axis=1)
		df.to_excel("Resources/" + str(year) + "/Master_" + str(year) + ".xlsx")







#given a playerID and rookie year, return a pair of values: one the cumulative value of the metric over the career, the other the number of seasons played.
def getPlayerMetricCareer(playerID, rookieYear,metric):
	cumulativeValue = 0
	numSeasons = 1
	stoppedFinding = 0
	if(rookieYear <= 1989):
		rookieYear = 1990
	for year in range(rookieYear,2019):
		if(year == 1990 and metric == "Salary"):
			continue
		df = master_season_dfs[year - 1990]
		df = df.loc[df['PID'] == playerID]
		for row in df.itertuples():
			seasonValue = getattr(row,metric)
			if(math.isnan(seasonValue)):
				continue
			numSeasons += 1
			stoppedFinding = 0
			cumulativeValue += seasonValue
			break
		stoppedFinding += 1
		if(stoppedFinding == 3):
			break
	if(numSeasons > 1):
		numSeasons -= 1
	return cumulativeValue, numSeasons


#this calculates the total metric for the draft position then divides by numSeasons. 
#An alternative would be to calculate the mean value for each player first, then take the average of averages.

def getAverageMetricForDraftPosition(df, draftPosition, metric):
	df = df.loc[df['Pk'] == draftPosition]
	numPlayersAtPick = 0
	OGsum = 0
	numPlayers = 0
	totalSeasonsForPick = 0
	for row in df.itertuples(index=True, name='Pandas'):
		numPlayersAtPick += 1
		numPlayers += 1
		playerID = getattr(row,'PID')
		print(playerID)
		rookieYear = getattr(row, 'RkYear')
		playerValue, playerSeasons = getPlayerMetricCareer(playerID, rookieYear,metric)
		OGsum += playerValue
		totalSeasonsForPick += playerSeasons


	return OGsum / totalSeasonsForPick, numPlayersAtPick

def getCumulativeMetricForDraftPosition(df, draftPosition, metric):
	df = df.loc[df['Pk'] == draftPosition]
	numPlayersAtPick = 0
	OGsum = 0
	for row in df.itertuples(index=True, name='Pandas'):
		numPlayersAtPick += 1
		playerID = getattr(row,'PID')
		print(playerID)
		rookieYear = getattr(row, 'RkYear')
		playerValue, playerSeasons = getPlayerMetricCareer(playerID, rookieYear,metric)
		OGsum += playerValue


	return OGsum, numPlayersAtPick




master_season_dfs = list()
for year in range (1990,2019):
	master_season_dfs.append(pd.read_excel("Resources/" + str(year) + "/Master_" + str(year) + ".xlsx"))
"""
normalizeMetric("PER")
normalizeMetric("WS")
normalizeMetric("VORP")

"""
masterFrame = pd.read_excel("Master_Players.xlsx")

draftPositions = list()
for x in range(1,61):
	draftPositions.append(x)



# START NORMALIZED PER, WS AND VORP

normalized_PER_list = list()
normalized_WS_list = list()
normalized_VORP_list = list()
numPlayersAtPick_list = list()
"""
for x in range (1,61):
	
	PER_value, numPlayersAtPick = getAverageMetricForDraftPosition(masterFrame,x,"normalized_PER")
	VORP_value, numPlayersAtPick = getAverageMetricForDraftPosition(masterFrame,x,"normalized_VORP")
	WS_value, numPlayersAtPick = getAverageMetricForDraftPosition(masterFrame,x,"normalized_WS")
	"""

#START CUMULATIVE CODE

"""
	PER_value, numPlayersAtPick = getCumulativeMetricForDraftPosition(masterFrame,x,"normalized_PER")
	VORP_value, numPlayersAtPick = getCumulativeMetricForDraftPosition(masterFrame,x,"normalized_VORP")
	WS_value, numPlayersAtPick = getCumulativeMetricForDraftPosition(masterFrame,x,"normalized_WS")

	normalized_PER_list.append(PER_value)
	normalized_WS_list.append(WS_value)
	normalized_VORP_list.append(VORP_value)
	numPlayersAtPick_list.append(numPlayersAtPick)

	print("Computed normalized_PER for draftPosition " + str(x) + ": " + str(PER_value))
	print("Computed normalized_WS for draftPosition " + str(x) + ": " + str(WS_value))
	print("Computed normalized_VORP for draftPosition " + str(x) + ": " + str(VORP_value))



stats = [('Draft Position', draftPositions),
		('Number of players computed for', numPlayersAtPick_list),
		('Cumulative Normalized PER', normalized_PER_list), 
		('Cumulative Normalized WS', normalized_WS_list),
		 ('Cumulative Normalized VORP', normalized_VORP_list)]
stats_df = pd.DataFrame.from_items(stats)
writer = pd.ExcelWriter('Cumulative_Normalized_Stats_by_DraftPos.xlsx')
stats_df.to_excel(writer, 'Sheet1')
writer.save()

"""

#Add a list here
playerID_list = list()
metric1_list = list()
metric2_list = list()
metric3_list = list()
metric4_list = list()
metric5_list = list()
metric6_list = list()


for row in masterFrame.itertuples(index = True, name='Pandas'):
	playerID = getattr(row, 'PID')
	print(playerID + " " + str(getattr(row,'RkYear')))
	#Add a getPlayerMetric here output = (cumulative value, num of seasons)
	metric1Value, a = getPlayerMetricCareer(playerID, getattr(row,'RkYear'), "WS")
	metric2Value, b = getPlayerMetricCareer(playerID, getattr(row,'RkYear'), "PER")
	metric3Value, c = getPlayerMetricCareer(playerID, getattr(row,'RkYear'), "VORP")
	metric4Value, d = getPlayerMetricCareer(playerID, getattr(row,'RkYear'), "BPercentile")
	metric5Value, e = getPlayerMetricCareer(playerID, getattr(row,'RkYear'), "APercentile")
	metric6value, f = getPlayerMetricCareer(playerID, getattr(row,'RkYear'), "Salary")
	
	#Append to the list here
	playerID_list.append(playerID)
	metric1_list.append(metric1Value/a)
	metric2_list.append(metric2Value/b)
	metric3_list.append(metric3Value/c)
	metric4_list.append(metric4Value/d)
	metric5_list.append(metric5Value/e)
	metric6_list.append(metric6value/f)

#add (header title, list) 
stats = [('Player ID', playerID_list),
		 ('WS', metric1_list),
		 ('PER', metric2_list),
		 ('VORP',metric3_list),
		 ('BPercentile',metric4_list),
		 ('APercentile',metric5_list),
		 ('Salary', metric6_list)]
stats_df = pd.DataFrame.from_items(stats)
writer = pd.ExcelWriter('AllMetrics1.xlsx')
stats_df.to_excel(writer, 'Sheet1')
writer.save()
