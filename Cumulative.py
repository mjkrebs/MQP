import xlrd

# Read the excel file
import xlsxwriter


def calculate_cumulative(year):
    master = xlrd.open_workbook("Resources/" + year + "/Master_" + year + ".xlsx")
    m_sheet = master.sheet_by_index(0)

    workbook = xlsxwriter.Workbook("Resources/" + year + '/Cumulative_games_solo' + year + '.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0,0,"Player")
    worksheet.write(0,1,"Points")
    for i in range(1,m_sheet.nrows):

        result = calculate_row(m_sheet.row(i))
        worksheet.write(i,0,result[0])
        worksheet.write(i, 1, result[1])
    workbook.close()

def calculate_row(r):
    name = r[0].value
    points = 0
    games = r[4].value
    starts = r[5].value
    minutes = r[6].value
    MVP = r[49].value
    ROY = r[50].value
    DPOY = r[51].value
    MIP = r[52].value
    SM = r[53].value
    NBA3 = r[54].value
    NBA2 = r[55].value
    NBA1 = r[56].value
    Def2 = r[57].value
    Def1 = r[58].value
    RK1 = r[59].value
    RK2 = r[60].value

    minsPlayed = float(minutes) *  float(games)
    startsAndPlayedOnly = float(games) + float(starts)*2.4
    minPoints = (48/5)*(float(minutes)/48.0) * float(games)

    points = minsPlayed * 0.24 + MVP*450 + ROY*60 + DPOY*450 + MIP * 450 + SM * 210 + NBA3*90 + NBA2*90 + NBA1*90 + Def1*90 + Def2*90 + RK1*12 + RK2*12
    # number of players on a roster: 15
    # active players for a game (GP) 12/15 --> 1
    # starting a game (GS) 5/12 --> 2.4
    # playing a minute (MP) 10 players on court / 24 --> 2.4
    # MVP 1 player / 30 teams * 15 players each --> 450
    # ROY 1 player / 60 rookies --> 60
    # DPOY 1 player / 450 players --> 450
    # MIP --> 450
    # 6th Man (SM) --> 1 player / 30 teams * 7 non-starters --> 210
    # NBA 3rd/2nd/1st / All defense team --> 450 points / 5 players on the team --> 90
    # NBA All rookie 2nd/1st --> 60 points / 5 players on the team --> 12 points
    # points = minPoints + 3 * float(starts) + NBA3 * 24 + NBA2 * 24 + NBA1 * 24 + Def1 * 36 + Def2 * 36 + RK1 * 6 + RK2 * 6

    return (name,points)


for x in range(1990,2019):
    calculate_cumulative(str(x))
