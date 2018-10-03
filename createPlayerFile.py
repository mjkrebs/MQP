import pandas as pd
import time


def all_players():
    all_pid = []
    all_names = []
    for year in range(1990,2019):
        master = pd.read_excel("Resources/" + str(year) + "/Master_" + str(year) + ".xlsx")
        players = master.get(["PID", "Player"]).values
        for player in players:
            if player[0] not in all_pid:
                all_pid.append(player[0])
                all_names.append((player[1]))
    return all_pid,all_names


def binary_search(arr, l, r, x):
    # Check base case
    if r >= l:
        mid = int(l + (r - l) / 2)
        # If element is present at the middle itself
        if arr[mid] == x:
            return arr[mid]
            # If element is smaller than mid, then it
        # can only be present in left subarray
        elif arr[mid] > x:
            return binary_search(arr, l, mid - 1, x)
            # Else the element can only be present
        # in right subarray
        else:
            return binary_search(arr, mid + 1, r, x)
    else:
        return -1

def find_player(pid, binary):
    if binary == 1:
        pids = pd.read_excel("Master_Players.xlsx")["PID"].values
        return binary_search(pids, 0, len(pid)-1, pid)
    else:
        df = pd.read_excel("Master_Players.xlsx")
        df = df.loc[df['PID'] == pid]
        return df.values


