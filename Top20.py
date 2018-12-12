import pandas as pd 

df = pd.read_excel("Top20.xlsx")
playerList = list()
scoreList = list()
for row in df.itertuples(index = True, name = 'Pandas'):

	playersAtRank = list()
	playersAtRank.append(row[2])
	playersAtRank.append(row[3])
	playersAtRank.append(row[4])
	playersAtRank.append(row[5])
	playersAtRank.append(row[6])
	playersAtRank.append(row[7])

	for player in playersAtRank:
		score = row[1]
		if player not in playerList:
			playerList.append(player)
			scoreList.append(0)
		scoreList[playerList.index(player)] += score
zipped = zip(playerList,scoreList)
zipped = sorted(zipped, key=lambda x: x[1], reverse=True)
for item in zipped:
	print(item)

