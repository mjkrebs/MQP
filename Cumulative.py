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

    # points = minPoints + MVP*360 + ROY*60 + DPOY*360 + MIP * 360 + SM * 360 + NBA3*24 + NBA2*24 + NBA1*24 + Def1*36 + Def2*36 + RK1*6 + RK2*6
    # points = minPoints + 3 * float(starts) + NBA3 * 24 + NBA2 * 24 + NBA1 * 24 + Def1 * 36 + Def2 * 36 + RK1 * 6 + RK2 * 6

    return (name,points)


for x in range(1990,2019):
    calculate_cumulative(str(x))
