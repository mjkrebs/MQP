# What do we want to include in the percentile stat
# TS%, rebs/opporitunities, a/TO, opponent fg% guarded vs average
# PER and PIE and RAPM
# PPG, Assists, Blocks, Rebounds, Steals

import xlrd

import xlsxwriter


#Merge Sort
def merge(a, b, i, val):
    c = []
    while len(a) != 0 and len(b) != 0:
        result = 0
        if val == 1:
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


def calculate_percentile(name, year, headers, cols):
    master = xlrd.open_workbook("Resources/" + year + "/Master_" + year + ".xlsx")
    m_sheet = master.sheet_by_index(0)

    workbook = xlsxwriter.Workbook("Resources/" + year + '/Percentile_' + name + "_" + year + '.xlsx')
    worksheet = workbook.add_worksheet()
    for i in range(len(headers)):
        worksheet.write(0, i, headers[i])

    currTable = []
    finalTable = []
    for i in range(1, m_sheet.nrows):
        currTable.append(m_sheet.row_slice(i, 0, m_sheet.ncols))
    # PPG 28, RB 22, 23 Ass, 24 Stl, 25 blk
    for player in range(1, m_sheet.nrows):
        name = currTable[player-1][0].value
        ranks = []
        if float(currTable[player-1][4].value) < 10:
            continue
        for i in range(len(cols)):
            tempTable = sort_by_column(currTable, cols[i], 1)
            tempRank = get_rank(tempTable, name)
            ranks.append(tempRank)
        overall = 0
        for j in range(len(ranks)):
            overall = overall + ranks[j]
        overall = overall/len(ranks)
        ranks.insert(0,name)
        ranks.insert(1,overall)
        finalTable.append(ranks)
    finalTable = sort_by_column(finalTable, 1, -1)
    for i in range(1, len(finalTable)):
        worksheet.write(i, 0, finalTable[i-1][0])
        worksheet.write(i, 1, finalTable[i-1][1])
        worksheet.write(i, 2, finalTable[i-1][2])
        worksheet.write(i, 3, finalTable[i-1][3])
        worksheet.write(i, 4, finalTable[i-1][4])
        worksheet.write(i, 5, finalTable[i-1][5])
        worksheet.write(i, 6, finalTable[i-1][6])


def get_rank(table, name):
    for i in range(len(table)):
        if table[i][0].value == name:
            return i


def multiple_percentiles(name, start, end, headers, cols):
    for i in range(start, end):
        calculate_percentile(name, str(i),headers,cols)



# year = "2018"
# headers = ["Name", "Overall", "Points", "Assists", "Rebounds", "Steals", "Blocks"]
# cols = [28, 23, 22, 24, 25]
# calculate_percentile(year, headers, cols)

