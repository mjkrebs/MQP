import pandas as pd


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

def find_player(pid):
    df = pd.read_excel("Master_Players.xlsx")
    df = df.loc[df['PID'] == pid]
    return df.values

