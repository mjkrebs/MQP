import pandas as pd
import matplotlib.pyplot as plt
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


def get_average_tick(cluster_ends):
    r = []
    index = 0
    for i in cluster_ends:
        if len(r) < 1:
            r.append((i+1)/2)
        else:
            r.append((cluster_ends[index-1]+1 + i)/2)
        index = index + 1
    return r

def graph_X_Y(x_axis , y_axis, cluster, cluster_ends, cluster_labels, start_year, end_year):
    x_cluster = get_average_tick(cluster_ends)
    y_cluster = [0]*len(cluster_labels)
    for year in range(start_year, end_year+1):
        draft = pd.read_excel("Resources/" + str(year) + "/Draft_" + str(year) + ".xlsx")
        y_index = 0
        if cluster:# Cluster the draft picks into grades
            # x_cluster.append(str(start_of_cluster) + "-" + str(cluster_ends[cluster_indexes]))
            temp_y = 0.0
            count = 0.0
            start_of_cluster = 1
            cluster_indexes = 0
            for pick in range(0, len(draft)):
                if draft.get(y_axis)[pick] > 0:
                    temp_y = temp_y + (draft.get(y_axis)[pick] / ((draft.get("G")[pick])*(end_year-start_year)))
                count = count + 1
                if pick == cluster_ends[cluster_indexes]-1:
                    y_cluster[y_index] =  y_cluster[y_index] + (temp_y/count)
                    y_index = y_index + 1
                    temp_y = 0.0
                    count = 0.0
                    start_of_cluster = pick + 2
                    cluster_indexes = cluster_indexes + 1
    draft = pd.DataFrame( {x_axis:x_cluster, y_axis:y_cluster})
    draft.plot(x=x_axis, y=y_axis)
    plt.savefig("Resources/Graphs/" + str(start_year) + "-" + str(end_year) + "_" + y_axis + "perGame_over_" + x_axis + "_.png")
    plt.show()


cluster_labels = ["1-3", "4-7", "8-12", "13-20", "21-30", "31-44", "45-60"]
cluster_ends = [3, 7, 12, 21, 30, 44, 60]
graph_X_Y("Pk","PTS" , 1, cluster_ends, cluster_labels, 2008, 2018)