import xlrd
import xlsxwriter

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
                            print(col)
                            worksheet.write(r_index,c_index, col)
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
    workbook = xlsxwriter.Workbook("Resources/"+year+'/Master_' + year + '.xlsx')
    worksheet = workbook.add_worksheet()
    PG = xlrd.open_workbook("Resources/"+year+"/PG_"+year+".xlsx")
    PG_sheet = PG.sheet_by_index(0)

    Adv = xlrd.open_workbook("Resources/"+year+"/Advanced_"+year+".xlsx")
    Adv_sheet = Adv.sheet_by_index(0)

    SPA = xlrd.open_workbook("Resources/"+year+"/Single_Player_Awards_"+year+".xlsx")
    SPA_sheet = SPA.sheet_by_index(0)

    AllNBA = xlrd.open_workbook("Resources/ALL_NBA_Teams.xlsx")
    AllNBA_sheet = AllNBA.sheet_by_index(0)

    AllDef = xlrd.open_workbook("Resources/ALL_Defensive.xlsx")
    AllDef_sheet = AllDef.sheet_by_index(0)

    AllRK = xlrd.open_workbook("Resources/ALL_Rookie.xlsx")
    AllRK_sheet = AllRK.sheet_by_index(0)
    column_length = 0
    
    for i in range(PG_sheet.nrows):
        for j in range(PG_sheet.ncols):
            value = PG_sheet.cell(i,j).value
            if value == "\xa0" or value == "":
                worksheet.write(i, j, 0.0)
            else:
                worksheet.write(i, j, value)
    column_length = PG_sheet.ncols
    
    for i in range(Adv_sheet.nrows):
        for j in range(6,Adv_sheet.ncols):
            value = Adv_sheet.cell(i, j).value
            if value == "\xa0" or value == "":
                worksheet.write(i, j, 0.0)
            else:
                worksheet.write(i,j+column_length-6, value)
    column_length = column_length+Adv_sheet.ncols - 7
    
    for i in range(1, SPA_sheet.nrows):
        for j in range(PG_sheet.nrows):
            worksheet.write(0, i+column_length, SPA_sheet.cell(i, 0).value)
            if PG_sheet.cell(j, 0).value == SPA_sheet.cell(i, 1).value:
                worksheet.write(j, i+column_length,1)
            else:
                worksheet.write(j, i+column_length, 0)
    column_length = column_length + SPA_sheet.nrows
    
    index = -1
    for i in range(AllNBA_sheet.nrows):
        currYear = AllNBA_sheet.cell(i,0).value
        if currYear[0:2] == year[0:2] and currYear[len(currYear)-2:] == year[2:]:
            # Found the year
            index = i
            break
    for i in range(1,4):
        worksheet.write(0, column_length+i-1, AllNBA_sheet.cell(index+i-1, 2).value + "NBA")
        players = []
        for j in range(3, AllNBA_sheet.ncols):
            players.append(AllNBA_sheet.cell(i, j).value[:-2])
        for x in range(1,PG_sheet.nrows):
                if PG_sheet.cell(x, 0).value in players:
                    worksheet.write(x, column_length+i - 1, 1)
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
            players.append(AllDef_sheet.cell(i, j).value)
        for x in range(1, PG_sheet.nrows):
            if PG_sheet.cell(x, 0).value in players:
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
            players.append(AllRK_sheet.cell(i, j).value)
        for x in range(1, PG_sheet.nrows):
            if PG_sheet.cell(x, 0).value in players:
                worksheet.write(x, column_length + i - 1, 1)
            else:
                worksheet.write(x, column_length + i - 1, 0)
    column_length = column_length + 2

    workbook.close()

def multiple_masters(start, end):
    for i in range(start, end+1):
        make_master(str(i))
# make_master("2018")