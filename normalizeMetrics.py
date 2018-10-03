#code to normalize all metrics from single season master sheets. 

#one metric normalize:
#loop through all the files
#find the maximum value of the metric
#loop through all the files
#set each value to value / maximum * 100


import pandas as pd 

#returns a metric value as a proportion of the maximum value, max = 100
def normalizeFunction(value,maxValue):
	return (value / maxValue) * 100

#finds the maximum value of the given metric, then normalizes all values and saves in the master season sheets.
def	normalizeMetric(metric):
	maxVal = 0
	for year in range(1990,2019):
		df = pd.read_excel("Resources/" + str(year) + "/Master_" + str(year) + ".xlsx")
		for row in df.itertuples():
			metricValue = getattr(row,metric)
			if(metricValue > maxVal):
				maxVal = metricValue

	for year in range(1990,2019):
		df = pd.read_excel("Resources/" + str(year) + "/Master_" + str(year) + ".xlsx")
		df['normalized_' + metric] = df.apply(lambda row: normalizeFunction(row['PER'], maxVal), axis=1)
		df.to_excel("Resources/" + str(year) + "/Master_" + str(year) + ".xlsx")



#normalizeMetric("PER")

#this dataframe not up to date, has too many undrafted players. using for testing purposes, change later. 
masterFrame = pd.read_excel("Master_Players.xlsx")


#given a playerID and rookie year, return a pair of values: one the cumulative value of the metric over the career, the other the number of seasons played.
def getPlayerMetricCareer(playerID, rookieYear,metric):
	cumulativeValue = 0
	numSeasons = 0
	if(rookieYear < 1989):
		rookieYear = 1990
	for year in range(rookieYear,2019):
		df = pd.read_excel("Resources/" + str(year) + "/Master_" + str(year) + ".xlsx")
		df = df.loc[df['PID'] == playerID]
		for row in df.itertuples():
			seasonValue = getattr(row,metric)
			numSeasons += 1
			cumulativeValue += seasonValue
			break
	print (cumulativeValue, numSeasons)
	return cumulativeValue, numSeasons


#this calculates the total metric for the draft position then divides by numSeasons. 
#An alternative would be to calculate the mean value for each player first, then take the average of averages.

def getAverageMetricForDraftPosition(df, draftPosition, metric):
	df = df.loc[df['Pk'] == draftPosition]
	OGsum = 0
	numPlayers = 0
	totalSeasonsForPick = 0
	for row in df.itertuples(index=True, name='Pandas'):

		numPlayers += 1
		playerID = getattr(row,'PID')
		print(playerID)
		rookieYear = getattr(row, 'RkYear')
		playerValue, playerSeasons = getPlayerMetricCareer(playerID, rookieYear,metric)
		OGsum += playerValue
		totalSeasonsForPick += playerSeasons


	return OGsum / totalSeasonsForPick

normalized_PER_list = list()

for x in range (1,61):
	value = getAverageMetricForDraftPosition(masterFrame,x,"normalized_PER")
	normalized_PER_list.append(value)
	print("Computed normalized_PER for draftPosition: " + str(x) + str(value))
