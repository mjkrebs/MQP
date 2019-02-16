import re
import numpy as np
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


for type in {"made", "not"}:
    for scope in {"all", "fresh", "last"}:
        frequenciesOfPlayersByScope(type, scope)
    for target in {"madeNBA", "wasDrafted", "lotteryPick", "firstRound"}:
        frequenciesOfPlayersByTarget(type, target)

