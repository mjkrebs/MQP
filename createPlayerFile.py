import xlrd

# Read the excel file
import xlsxwriter


def add_players():
    workbook = xlsxwriter.Workbook("Resources/Players.xlsx")
    worksheet = workbook.add_worksheet()
    worksheet.write(0,0,"Name")
    players = set()
    x = 1
    for year in range(1990,2019):
        master = xlrd.open_workbook("Resources/" + str(year) + "/Master_" + str(year) + ".xlsx")
        m_sheet = master.sheet_by_index(0)
        for i in range(1,m_sheet.nrows):
            result = m_sheet.cell(i,0).value
            if(result not in players):
                players.add(result)
                worksheet.write(x,0,result)
                x = x+1
    workbook.close()

add_players()