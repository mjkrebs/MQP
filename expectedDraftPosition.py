import time
import xlrd
import xlsxwriter
import numpy as np
import pandas as pd


# function which can get any metric based on the parameter, calls the appropriate function.
# currently only supports percentile
# NOTE: RETURNS CUMULATIVE VALUE & NUMSEASONS (seasonsplayed)
def getPlayerCumulativeMetricCareer(name, metric, year):
    if (metric == "percentile"):
        cumValue, numSeasons = getPercentileMetricCareer(name, year)
        if (numSeasons == 0):
            return cumValue, 1
    else:
        print("This is not a valid metric.")
    return cumValue, numSeasons


# go through all percentile files, if found, add the value to a cumulative and increment a count.
# return a pair [cumulative percentile, numSeasons]. TO
def getPercentileMetricCareer(pid, rookieYear):
    cumulative = 0
    numSeasons = 0
    start = time.time()
    for year in range(rookieYear, 2018):
        master = pd.read_excel("Resources/" + str(year) + "/Percentile_" + str(year) + ".xlsx")
        try:
            player = master.loc[master['PID'] == pid]
            numSeasons = numSeasons + 1
            cumulative = cumulative + int(player['Overall_Rank'])
        except Exception as e:
            continue
    end = time.time()
    print(pid + " took " + str(end-start) + " to finish")
    return cumulative, numSeasons


# creates a set of all players. currently bottlenecks
def addPlayers():
    players = set()
    x = 1
    for year in range(1990, 2019):
        master = xlrd.open_workbook("Resources/" + str(year) + "/Master_" + str(year) + ".xlsx")
        m_sheet = master.sheet_by_index(0)
        for i in range(1, m_sheet.nrows):
            result = m_sheet.cell(i, 1).value
            if (result not in players):
                players.add(result)
                x = x + 1
    return players


# look up name in draft workbook. 61 == undrafted (rookie year == 1990)
def getPlayerDraftPosn(playerID):
    for year in range(1990, 2019):
        master = xlrd.open_workbook("Resources/" + str(year) + "/Draft_" + str(year) + ".xlsx")
        m_sheet = master.sheet_by_index(0)
        for i in range(1, m_sheet.nrows):
            result = m_sheet.cell(i, 2).value
            if (result == playerID):
                draftPos = m_sheet.cell(i, 0).value
                return int(draftPos), year
    return 61, 1990


# given a draft position and name of a metric, will go into that workbook and return the average value.
def getAverageMetric(df, draftPosition, metric):
    df = df.loc[df['draftPosition'] == draftPosition]
    OGsum = 0
    count = 0
    for row in df.itertuples(index=True, name='Pandas'):
        count = count + 1
        OGsum = OGsum + row[metric]
    return OGsum / count


# creates the master workbook
def addMetricToDataframe(playerInfoDataframe, metric):
    metricColumn = list()
    print("Beginning to add metric " + metric + " to dataframe")
    start = time.time()
    progress = 0
    for row in playerInfoDataframe.itertuples(index=True, name='Pandas'):

        if progress == len(playerInfoDataframe)*.10:
            print("10%")
            print("Took " + str(time.time()-start) + "seconds")
        if progress == len(playerInfoDataframe)*.20:
            print("20%")
            print("Took " + str(time.time() - start) + "seconds")
        draftPos = getattr(row, "draftPosition")
        playerID = getattr(row, "playerID")
        rookieYear = getattr(row, "rookieYear")
        cumulativeMetric, numSeasons = getPlayerCumulativeMetricCareer(playerID, metric, rookieYear)
        metricValue = cumulativeMetric / numSeasons
        metricColumn.append(metricValue)
        # print(playerName + " %val: " + str(metricValue))
        progress = progress + 1
    end = time.time()
    print("Finished adding metric to df: Took " + str(end-start) + " to complete.")
    playerInfoDataframe[metric] = metricColumn
    playerInfoDataframe.to_excel("Tester_percentile_playerInfo.xlsx")
    return playerInfoDataframe



def optimized_getPlayerDraftPosn(playerSet):
    playerIDs = list()
    playerPosn = list()
    playerRKYear = list()
    for year in range(1990, 2019):
        master = xlrd.open_workbook("Resources/" + str(year) + "/Draft_" + str(year) + ".xlsx")
        m_sheet = master.sheet_by_index(0)
        for i in range(1, m_sheet.nrows):
            result = m_sheet.cell(i, 2).value
            if (result in playerSet):
                draftPos = m_sheet.cell(i, 0).value
                playerIDs.append(result)
                playerPosn.append(draftPos)
                playerRKYear.append(year)
                # print(result + " was drafted " + str(draftPos)+ " in " + str(year))
    return playerIDs, playerPosn, playerRKYear


def createOGDataframe():
    print("Creating player set")
    playerSet = addPlayers()
    # print(playerSet)
    # playerDraftPosnSet = list()
    # playerRookieYearSet = list()
    print("Obtaining draft position and rookie year")
    start = time.time()
    pid, draftpos, year = optimized_getPlayerDraftPosn(playerSet)

    # print(pid)

    for playerID in playerSet:
        if playerID in pid:
            continue
        else:
            pid.append(playerID)
            draftpos.append(61)
            year.append(1990)

    end = time.time()
    print("finished creating playerset:\n\tTook " + str(end-start) + "time to complete/n saving to dataframe")
    OGDataFrame = pd.DataFrame({'playerID': pid,
                                'draftPosition': draftpos, 'rookieYear': year})
    OGDataFrame.to_csv('OGDataFrame.csv')
    print("Saved")
    return OGDataFrame


# start main code


# print(str(getPercentileMetricCareer("jamesle01",2003)))

dfWithMetric = addMetricToDataframe(createOGDataframe(), "percentile")
#
# # save playerset, draftPosn and rookieYear to csv
#
#
for i in range(1, 62):
    print(getAverageMetric(dfWithMetric, i, "percentile"))