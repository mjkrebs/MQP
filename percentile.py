# What do we want to include in the percentile stat
# TS%, rebs/opporitunities, a/TO, opponent fg% guarded vs average
# PER and PIE and RAPM
# PPG, Assists, Blocks, Rebounds, Steals

import xlrd
import pandas as pd
import xlsxwriter


#Merge Sort
def merge(a, b, i, val):
    c = []
    while len(a) != 0 and len(b) != 0:
        result = 0
        if val == 1:
            if a[0][i].value == " " or a[0][i].value == "" :
                a[0][i].value = 0
            if b[0][i].value == " " or b[0][i].value == "" :
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


def calculate_percentile(year, headers, name):
    master = pd.read_excel("Resources/" + year + "/Master_" + year + ".xlsx")
    output_df = pd.DataFrame()
    headers_rank = []
    first = 1
    for col_header in headers:
        # Here is where I am applying a cutoff of 10 minutes minimum played
        sorted_df = master.loc[master["MP"] > 10].get(["PID", "Player", col_header]).sort_values(col_header, ascending = False)
        sorted_df.set_index(["PID","Player"])
        sorted_df.reset_index(inplace=True)
        sorted_df[col_header+"_rank"] = sorted_df.index
        headers_rank.append(col_header+"_rank")
        if first == 1:
            output_df = sorted_df
            first = 2
        else:
            output_df = output_df.merge(sorted_df, on=["PID", "Player"])

    output_df["Overall_Rank"] = (output_df[headers_rank].sum(axis=1).divide(len(headers)))
    output_df = output_df.sort_values("Overall_Rank", ascending = True)
    output_df.reset_index(inplace=True)
    output_df.__delitem__("index_x")
    output_df.__delitem__("index_y")
    output_df.__delitem__("index")
    output_df.__delitem__("level_0")
    output_df.to_excel("Resources/" + year + "/" + name + "_Percentile_" + year + ".xlsx")


def multiple_percentiles(start, end, headers, name):
    for i in range(start, end+1):
        calculate_percentile(str(i),headers, name)

BasHeaders = ["PS/G", "AST", "TRB", "STL", "BLK"]
bas = "Basic"
AdvHeaders = ["PER", "TS%", "USG%", "WS/48", "VORP"]
adv = "Advanced"
multiple_percentiles(2018,2018, BasHeaders, bas)
multiple_percentiles(2018,2018, AdvHeaders, adv)
