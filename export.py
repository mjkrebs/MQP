import difflib

import xlrd
import xlsxwriter
import pandas as pd
import createPlayerFile
import numpy as np
import re

#Merge Sort
def merge(a, b, i, type):
    c = []
    while len(a) != 0 and len(b) != 0:
        result = 0
        if type == "num":
            if a[0][i].value == " ":
                a[0][i].value = 0
            if b[0][i].value == " ":
                b[0][i].value = 0
            if float(a[0][i].value) > float(b[0][i].value):
                result = 1
        else:
            if a[0][i] < b[0][i]:
                result = 1
        if result == 1:
            c.append(a[0])
            a.remove(a[0])
        else:
            c.append(b[0])
            b.remove(b[0])
    if len(a) == 0:
        c += b
    else:
        c += a
    return c


# Code for merge sort
def MergeSort(x, col, val):
    if len(x) == 0 or len(x) == 1:
        return x
    else:
        middle = int(len(x)/2)
        a = MergeSort(x[:middle], col, val)
        b = MergeSort(x[middle:], col, val)
        return merge(a, b, col, val)


def sort_by_column(table, col, val):
    return MergeSort(table, col, val)


def export(table,name, y):
    workbook = xlsxwriter.Workbook(name+'.xlsx')
    worksheet = workbook.add_worksheet()
    r_index = 0
    name = ""
    duplicate = False
    if y == True:
        for t in table:
            for row in t:
                c_index = 0
                if duplicate == True:
                    if row[0] == name:
                        continue
                    else:
                        duplicate = False
                        name = ""
                if (len(row) > 0):
                    for col in row:
                        if col == "TOT":
                            name = row[0]
                            duplicate = True
                        if col == "RK" and r_index != 0:
                            r_index  = r_index-2
                            break
                        if len(col) > 0:
                            if col == " ":
                                col = 0
                            worksheet.write(r_index, c_index, col)
                            c_index = c_index + 1
                    r_index = r_index + 1
    else:
          for row in table:
            c_index = 0
            if duplicate == True:
                if row[0] == name:
                    continue
                else:
                    duplicate = False
                    name = ""
            if (len(row) > 0):
                for col in row:
                    if col == "TOT":
                        name = row[0]
                        duplicate = True
                    if len(col) > 0:
                        if col == " ":
                            col = 0
                        worksheet.write(r_index, c_index, col)
                        c_index = c_index + 1
            r_index = r_index + 1
    workbook.close()


def make_master(year):
    # make_awards_file(year)

    pg = pd.read_excel("Resources/"+str(year)+"/PG_"+str(year)+".xlsx")
    pg['Player'] = pg['Player'].map(lambda x: x.rstrip('*'))
    Adv = pd.read_excel("Resources/"+str(year)+"/Advanced_"+str(year)+".xlsx")
    Adv.__delitem__("PID")
    Adv.__delitem__("Player")
    Adv.__delitem__("Age")
    Adv.__delitem__("Pos")
    Adv.__delitem__("G")
    Adv.__delitem__("Tm")

    tot = pd.read_excel("Resources/" + str(year) + "/Totals_" + str(year) + ".xlsx")
    tot.__delitem__("PID")
    tot.__delitem__("Player")
    tot.__delitem__("Age")
    tot.__delitem__("Pos")
    tot.__delitem__("G")
    tot.__delitem__("Tm")

    awards = pd.read_excel("Resources/" + str(year) + "/Binary_Awards_" + str(year) + ".xlsx")

    result = pd.concat([pg, Adv, awards], axis=1)
    result.to_excel("Resources/"+str(year)+"/Master_"+str(year)+".xlsx")


def make_awards_file(year):
    workbook = xlsxwriter.Workbook("Resources/" + year + '/Binary_Awards_' + year + '.xlsx')
    worksheet = workbook.add_worksheet()
    PG = xlrd.open_workbook("Resources/" + year + "/PG_" + year + ".xlsx")
    PG_sheet = PG.sheet_by_index(0)

    SPA = xlrd.open_workbook("Resources/" + year + "/Single_Player_Awards_" + year + ".xlsx")
    SPA_sheet = SPA.sheet_by_index(0)

    AllNBA = xlrd.open_workbook("Resources/ALL_NBA_Teams.xlsx")
    AllNBA_sheet = AllNBA.sheet_by_index(0)

    AllDef = xlrd.open_workbook("Resources/ALL_Defensive.xlsx")
    AllDef_sheet = AllDef.sheet_by_index(0)

    AllRK = xlrd.open_workbook("Resources/ALL_Rookie.xlsx")
    AllRK_sheet = AllRK.sheet_by_index(0)

    column_length = 0
    for i in range(1, SPA_sheet.nrows):
        for j in range(PG_sheet.nrows):
            worksheet.write(0, i-1, SPA_sheet.cell(i, 0).value)
            if PG_sheet.cell(j, 1).value.replace("*","") == SPA_sheet.cell(i, 1).value:
                worksheet.write(j, i-1, 1)
            else:
                worksheet.write(j, i-1, 0)
    column_length = column_length + SPA_sheet.nrows-1
    index = -1
    for i in range(AllNBA_sheet.nrows):
        currYear = AllNBA_sheet.cell(i, 0).value
        if currYear[0:2] == year[0:2] and currYear[len(currYear) - 2:] == year[2:]:
            # Found the year
            index = i
            break
    for i in range(1, 4):
        worksheet.write(0, column_length + i - 1, AllNBA_sheet.cell(index + i - 1, 2).value + "NBA")
        players = []
        for j in range(3, AllNBA_sheet.ncols):
            players.append(AllNBA_sheet.cell(i-1 + index, j).value[:-2])
        for x in range(1, PG_sheet.nrows):
            name = PG_sheet.cell(x,1).value
            if PG_sheet.cell(x, 1).value.replace("*","") in players:
                worksheet.write(x, column_length + i - 1, 1)
            else:
                worksheet.write(x, column_length + i - 1, 0)
    column_length = column_length + 3


    index = -1
    for i in range(AllDef_sheet.nrows):
        currYear = AllDef_sheet.cell(i, 0).value
        if currYear[0:2] == year[0:2] and currYear[len(currYear) - 2:] == year[2:]:
            # Found the year
            index = i
            break
    for i in range(1, 3):
        worksheet.write(0, column_length + i - 1, AllDef_sheet.cell(index + i - 1, 2).value + "DEF")
        players = []
        for j in range(3, AllDef_sheet.ncols):
            players.append(AllDef_sheet.cell(i-1 + index, j).value)
        for x in range(1, PG_sheet.nrows):
            if PG_sheet.cell(x, 1).value.replace("*","") in players:
                worksheet.write(x, column_length + i - 1, 1)
            else:
                worksheet.write(x, column_length + i - 1, 0)
    column_length = column_length + 2

    index = -1
    for i in range(AllRK_sheet.nrows):
        currYear = AllRK_sheet.cell(i, 0).value
        if currYear[0:2] == year[0:2] and currYear[len(currYear) - 2:] == year[2:]:
            # Found the year
            index = i
            break
    for i in range(1, 3):
        worksheet.write(0, column_length + i - 1, AllRK_sheet.cell(index + i - 1, 2).value + "RK")
        players = []
        for j in range(3, AllRK_sheet.ncols):
            players.append(AllRK_sheet.cell(i-1 + index, j).value)
        for x in range(1, PG_sheet.nrows):
            if PG_sheet.cell(x, 1).value.replace("*","") in players:
                worksheet.write(x, column_length + i - 1, 1)
            else:
                worksheet.write(x, column_length + i - 1, 0)


def multiple_masters(start, end):
    for i in range(start, end+1):
        make_master(str(i))


def salary_cleanup(start_year, end_year):
    f = open("Resources/nba_salaries_1990_to_2018.csv","r")
    all_file = f.read()
    for i in range(start_year, end_year+1):
        s_year = str(i)
        players = re.findall('(.+),(\d+),(' + s_year + '),(\d+),(\w+),(\w+ \w+)', all_file)
        correct_players = []
        for player in players:
            firstname = ""
            lastname = ""
            player_names = re.findall('(\w+)', player[0])
            for names in range(len(player_names)):
                if names == len(player_names)-1:
                    lastname = player_names[names]
                else:
                    firstname = firstname + player_names[names]
            fixed_player = []
            for col in range(len(player)):
                if col == 0:
                    fixed_player.append(lastname + " " + firstname)
                else:
                    fixed_player.append(player[col])
            correct_players.append(fixed_player)
        sorted_players = export.sort_by_column(correct_players, 0,"str")
        tempout = open("Resources/" + s_year + "/Salary_" + s_year + ".csv", "w+")
        for player in sorted_players:
            for col in range(len(player)):
                tempout.write(player[col])
                if col == len(player)-1:
                    tempout.write("\n")
                else:
                    tempout.write(",")
    f.close()


def make_master_player():
    master_draft = pd.read_excel("Master_Draft.xlsx")
    master_draft.set_index(['PID'])

    for year in range(1990, 1991):
        #TODO
        # What we need to do here is add all of the players who are in the master list and also not in the master draft and add them in
        print("")


# Note that players from early drafts who don't have stats at all in basketball reference do not have a PID, so we should ignore them.
def make_master_draft():
    master_draft = pd.DataFrame
    first = 1
    for year in range(1976, 2019):
        draft = pd.read_excel("Resources/" + str(year) + "/Draft_" + str(year) + ".xlsx")
        draft = draft[["PID", "Player", "Pk","Tm","College"]]
        draft["RkYear"] = year
        draft.columns = ['PID', "Player", "Pk", "DraftTeam", "College", "RkYear"]
        if first == 1:
            master_draft = draft
            first = 2
        else:
            master_draft = pd.concat([draft, master_draft])
    pids, names = createPlayerFile.all_players()
    drafted_pids = master_draft["PID"].values
    undrafted_pids = []
    undrafted_names = []
    for i in range(len(pids)):
        if " " in pids[i] or pids[i] in drafted_pids:
            continue
        else:
            undrafted_pids.append(pids[i])
            undrafted_names.append(names[i])
    master_draft_removed = master_draft.values


    master_draft.to_excel("Master_Draft.xlsx")
    undrafted_players = pd.DataFrame({"PID":undrafted_pids, "Player":undrafted_names,"Pk":61, "DraftTeam":0, "College":0, "RkYear":1990})
    print(undrafted_players)
    master_players = master_draft.append(undrafted_players)
    master_players = master_players.set_index("PID")
    master_players = master_players.sort_index()
    master_players.to_excel("Master_Players.xlsx")

    return master_draft


def percentile_to_master(start, end):
    for year in range(start, end+1):
        pdf = pd.read_excel("Resources/" + str(year) + "/Basic_Percentile_" + str(year) + ".xlsx").get(["PID","Overall_Rank"])
        adf = pd.read_excel("Resources/" + str(year) + "/Advanced_Percentile_" + str(year) + ".xlsx").get(["PID","Overall_Rank"])
        master = pd.read_excel("Resources/" + str(year) + "/Master_" + str(year) + ".xlsx")

        pdf.set_index(["PID"])
        adf.set_index(["PID"])
        master.set_index(["PID"])

        pdf.columns = ["PID", "BPercentile"]
        adf.columns = ["PID", "APercentile"]

        master = master.merge(pdf, on=["PID"])
        master = master.merge(adf, on=["PID"])
        master.to_excel("Resources/" + str(year) + "/Master_" + str(year) + ".xlsx")
        print(str(year))


def salary_master(start, end):
    salary = pd.read_excel("NBA_Salary_History.xlsx")
    salary = salary.get(["Player", "Salary", "YearEnd", "Team"])
    salary.columns = ["Player", "Salary", "Year", "Tm"]
    salary.set_index(["Player"])
    if start == 1990:
        start +=1
    for year in range(start, end+1):
        temp = salary.loc[salary["Year"] == year].get(["Player", "Salary"])
        print(len(temp))
        master = pd.read_excel("Resources/" + str(year) + "/Master_" + str(year) + ".xlsx")
        master.set_index(["Player"])
        try:
            master.__delitem__("Salary")
        except Exception as e:
            print(e)
        master = master.merge(temp, on=(["Player"]), how="outer")

        # This line below is where we fill in the values where there is no
        master.Salary.fillna(value=0, inplace=True)
        # This two lines remove the people at the bottom, who are the people in the salary sheet but not in master sheet.
        # Basically these are people who were under contract but never played in that season
        # E.g. Shawn Bradley in 2007
        master['PID'].replace('', pd.np.nan, inplace=True)
        master.dropna(subset=['PID'], inplace=True)

        sal = master['Salary']
        master.__delitem__("Salary")
        master.insert(5,"Salary", sal)
        master.to_excel("Resources/" + str(year) + "/Master_" + str(year) + ".xlsx")


# Points*1 + RBS*1.2 + 3&stl + 3*blk + 1.5*ast - TO*1
def fantasy_master(start, end):
    for year in range(start, end+1):
        master = pd.read_excel("Resources/" + str(year) + "/Master_" + str(year) + ".xlsx")
        master.set_index(["Player"])
        try:
            master.__delitem__("Fantasy")
        except Exception as e:
            print(e)

        master["PS/G"].fillna(value=(master["3P"] *3 + master["2P"]*2 + master["FT"]), inplace=True)
        master["Fantasy"] = master["G"]*(master['PS/G']*1 + master['AST']*1.5 + master["TRB"]*1.2 + master["STL"]*3 + master["BLK"]*3 - master["TOV"])
        master.to_excel("Resources/" + str(year) + "/Master_" + str(year) + ".xlsx")


def master_ncaa_teams(start,end):
    result = pd.DataFrame
    for year in range(start, end+1):
        s_year = str(year)
        curr = pd.read_excel("NCAA/" + s_year + "/School_Stats" + s_year + ".xlsx").get(["ID", "School"])
        curr.set_index(["ID", "School"])
        curr["School"] = curr["School"].apply(lambda x: x.rstrip("NCAA"))
        if result.empty:
            result = curr
        else:
            result = result.merge(curr, on=(["ID", "School"]), how='outer')
    result = result.drop_duplicates("ID")
    result = result.sort_values("ID")
    result.to_excel("NCAA/master_teams.xlsx")


def fill_nba_players(start, end):
    # We need to do two things, read the Teams nba roster and then go to the setting
    master_teams = pd.read_excel("NCAA/master_teams.xlsx")
    for year in range(start, end+1):
        s_year = str(year)
        print("\n\n\n\n" + s_year)
        curr_master = pd.read_excel("NCAA/" + s_year + "/" + s_year + "_master_roster.xlsx")

        # We need to fix the naming on all master sheets, we mad two 2PA
        curr_master.columns = ["Team", "Player", "NBA", "G", "GS", "MP", "FG", "FGA", "FG%", "2P", "2PA", "2P%", "3P", "3PA", "3P%", "FT",
                        "FTA","FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]
        curr_ids = pd.read_excel("NCAA/master_teams_urls.xlsx")["URLS"]
        x = 0
        for id in curr_ids:
            if id == "None":
                continue
            teams_nba_players = pd.read_excel("NCAA/Teams/" + id + "/NBA_Players_" + id + ".xlsx")
            teams_nba_players = teams_nba_players.loc[teams_nba_players['Year'] == year]
            for name in teams_nba_players["Player"]:
                # player names are not consistent
                curr_player_row = curr_master.loc[curr_master['Player'] == name]
                if curr_player_row.empty:
                    print(name)
                    continue
                index = curr_player_row.index[curr_player_row['Player'] == name]
                index = index[0]
                if index == -1:
                    print("rip")
                else:
                    curr_player_row = curr_player_row.set_value(index, "NBA", 1)
                    curr_player_row.set_index(["Team"])
                    curr_master.set_index(["Team"])
                    curr_master = curr_player_row.merge(curr_master, on=["Team", "Player", "G", "GS", "MP", "FG", "FGA", "FG%", "2P", "2PA", "2P%", "3P", "3PA", "3P%", "FT",
                                "FTA","FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"], how = "outer")
                    curr_master["NBA_x"] = curr_master["NBA_x"].replace(r'\s+', np.nan, regex=True)
                    curr_master["NBA_x"] = curr_master["NBA_x"].fillna(0)
                    curr_master = curr_master.sort_values("Team")
                    curr_master.insert(2, "NBA", curr_master["NBA_x"] + curr_master["NBA_y"])
                    curr_master.__delitem__("NBA_x")
                    curr_master.__delitem__("NBA_y")
        curr_master.to_excel("NCAA/" + s_year + "/" + s_year + "_master_roster.xlsx")


def get_nba_players(start, end):
    for year in range(start, end + 1):
        s_year = str(year)
        curr_year = pd.read_excel("NCAA/" + s_year + "/" + s_year + "_master_roster.xlsx")
        nba_players = curr_year[curr_year.NBA == 1]
        nba_players.to_excel("NCAA/" + s_year + "/" + s_year + "_nba_players_stats.xlsx")


def make_NCAA_master_roster(start, end):
    result = pd.DataFrame
    for year in range(start, end+1):
        s_year = str(year)
        curr_year = pd.read_excel("NCAA/" + s_year + "/" + s_year + "_master_roster.xlsx")
        if result.empty:
            result = curr_year
        else:
            result = result.append(curr_year)
    result.to_excel("test.xlsx")
    result.to_csv("test.csv")


start = 2000
end = 2018

# # First make the master sheets
# multiple_masters(start, end)
#
# # Then make the percentile sheets from the master sheets
# BasHeaders = ["PS/G", "AST", "TRB", "STL", "BLK"]
# bas = "Basic"
# AdvHeaders = ["TS%", "AST%", "TRB%", "STL%", "BLK%"]
# adv = "Advanced"
# percentile.multiple_percentiles(start,end, BasHeaders, bas)
# percentile.multiple_percentiles(start,end, AdvHeaders, adv)
#
# # Add the percentile metrics to master
# percentile_to_master(start, end)
#
# # Add the salary to the master sheet
# salary_master(start, end)
#
# # Add the fantasy points to master
# fantasy_master(start, end)

# master_ncaa_teams(start, end)

# fill_nba_players(start, end)

# get_nba_players(start, end)
make_NCAA_master_roster(start, end)