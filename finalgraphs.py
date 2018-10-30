import pandas as pd 
import math

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

masterFrame = pd.read_excel("Master_Players.xlsx")

draftPositions = list()
for x in range(1,62):
	draftPositions.append(x)


PER_list = list()
WS_list = list()
VORP_list = list()
BPercentile_list = list()
APercentile_list = list()
Fantasy_list = list()
numPlayersAtPick_list = list()

for x in range(1,62):
	PER_value, numPlayersAtPick = getCumulativeMetricForDraftPosition(masterFrame,x,"PER")
	VORP_value, numPlayersAtPick = getCumulativeMetricForDraftPosition(masterFrame,x,"VORP")
	WS_value, numPlayersAtPick = getCumulativeMetricForDraftPosition(masterFrame,x,"WS")
	BPercentile_value, numPlayersAtPick = getCumulativeMetricForDraftPosition(masterFrame,x,"BPercentile")
	APercentile_value, numPlayersAtPick = getCumulativeMetricForDraftPosition(masterFrame,x,"APercentile")
	Fantasy_value, numPlayersAtPick = getCumulativeMetricForDraftPosition(masterFrame,x,"Fantasy")


	PER_list.append(PER_value)
	WS_list.append(WS_value)
	VORP_list.append(VORP_value)
	BPercentile_list.append(BPercentile_value)
	APercentile_list.append(APercentile_value)
	Fantasy_list.append(Fantasy_value)
	numPlayersAtPick_list.append(numPlayersAtPick)


stats = [('Draft Position', draftPositions),
		('Number of players computed for', numPlayersAtPick_list),
		('Cumulative Normalized PER', PER_list), 
		('Cumulative Normalized WS', WS_list),
		 ('Cumulative Normalized VORP', VORP_list),
		 ('Cumulative Normalized Basic Percentile', BPercentile_list),
		 ('Cumulative Normalized Advanced Percentile', APercentile_list),
		 ('Cumulative Normalized Fantasy Points', Fantasy_list)]
stats_df = pd.DataFrame.from_items(stats)
writer = pd.ExcelWriter('Final_Draft_Position_Graphs.xlsx')
stats_df.to_excel(writer, 'Sheet1')
writer.save()