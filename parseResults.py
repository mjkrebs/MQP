import re
import numpy as np
import pandas as pd
# e.g. made, fresh

def frequenciesOfPlayersByScope(type, scope):
    cumulativeTxt = ""
    for i in {"madeNBA", "wasDrafted", "firstRound", "lotteryPick"}:
        f = open("Plot/Results/" + i + "_" + type + "_" + scope + ".txt", "r")
        cumulativeTxt = cumulativeTxt + f.read()
        f.close()
    allnames = re.findall(r"\[\'(\w+ \w+|\w+ \w+-\w+)", cumulativeTxt)
    # print(names)
    noDupNames= list(dict.fromkeys(allnames))
    output = []
    for name in noDupNames:
        output.append((allnames.count(name), name))
    output.sort(reverse=True)
    output = np.array(output)
    out = open("Plot/Results/Frequency/" + scope + "_" + type + ".txt", "w+")
    for row in output:
        out.write("Player:" + row[1] + " Count: " + row[0]+"\n")
    out.close()


def frequenciesOfPlayersByTarget(type, target):
    cumulativeTxt = ""
    for i in {"all", "fresh", "last"}:
        f = open("Plot/Results/" + target + "_" + type + "_" + i + ".txt", "r")
        cumulativeTxt = cumulativeTxt + f.read()
        f.close()
    allnames = re.findall(r"\[\'(\w+ \w+|\w+ \w+-\w+)", cumulativeTxt)
    # print(names)
    noDupNames= list(dict.fromkeys(allnames))
    output = []
    for name in noDupNames:
        output.append((allnames.count(name), name))
    output.sort(reverse=True)
    output = np.array(output)
    out = open("Plot/Results/Frequency/" + target+ "_" + type + ".txt", "w+")
    for row in output:
        out.write("Player:" + row[1] + " Count: " + row[0]+"\n")
    out.close()



def resultsToTables(type, target):
    cumulativeTxt = ""
    for i in {"all", "fresh", "last"}:
        f = open("Plot/Results/" + target + "_" + type + "_" + i + ".txt", "r")
        for line in f:
            line = line + "[" + i + "]"
            print(line)
            cumulativeTxt = cumulativeTxt + line
        f.close()
    # print(cumulativeTxt)
    all = re.findall(r"\[\'(\w+ \w+|\w\.\w\. \w+|\w+ \w+-\w+|\w+ \w+ \w+)\'\]\: \[(0\.\d+) (0.\d+)\] Year: \[\'(\d+-\d+)\'\] \w+: (\d) \w+: (\d)\n\[(\w+)", cumulativeTxt)
    names = []
    probM = []
    probN = []
    year = []
    pred = []
    actual = []
    scope = []
    counter = 0
    for player in all:
        for row in player:
            if(counter%7==0):
                names.append(row)
            elif (counter % 7 == 1):
                probN.append(row)
            elif (counter % 7 == 2):
                probM.append(row)
            elif (counter % 7 == 3):
                year.append(row)
            elif (counter % 7 == 4):
                pred.append(row)
            elif (counter % 7 == 5):
                actual.append(row)
            else:
                scope.append(row)
            counter +=1
    typeDF = [str(type)]*len(actual)
    targetDF = [str(target)]*len(actual)

    df = pd.DataFrame({"Scope":scope, "Type":typeDF, "Target":targetDF, "Name": names, "Probability Made": probM, "Probability Not": probN, "Year": year, "Predicted":pred, "Actual":actual})
    df.to_excel(type + "_" + target + ".xlsx")


def combineTables():
    masterdf = pd.DataFrame()
    for type in {"made", "not"}:
        for target in {"madeNBA", "wasDrafted", "lotteryPick", "firstRound", "secondRound"}:
            if(len(masterdf)==0):
                masterdf = pd.read_excel(type + "_" + target + ".xlsx")
            else:
                masterdf = masterdf.append(pd.read_excel(type + "_" + target + ".xlsx"))
    masterdf.to_excel("all_misses.xlsx")


for type in {"made", "not"}:
    # for scope in {"all", "fresh", "last"}:
    #     frequenciesOfPlayersByScope(type, scope)
    for target in {"madeNBA", "wasDrafted", "lotteryPick", "firstRound", "secondRound"}:
        # frequenciesOfPlayersByTarget(type, target)
        resultsToTables(type, target)

combineTables()


