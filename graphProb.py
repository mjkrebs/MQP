import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
def makeMadeGraph(fname, title, xlabel, cutoff):
    df = pd.read_excel("Plot/Results/" + fname)
    df = df.sort_values("MadePercent")
    df["Truth Values"] = df["actual"]-df["predicted"]*2
    df = df.reset_index()
    percentLower = []
    for i in range(1, len(df)+1):
        percentLower.append(i/(len(df)+1))
    print(percentLower[2500])
    df["percentLower"] = percentLower
    df = df.drop(df[df.MadePercent<cutoff].index)
    sns.set_style("whitegrid")

    prediction = {-2: "False Positive", -1:"True Positive", 0:"True Negative", 1: "False Negative"}
    labels = df["Truth Values"].map(prediction)
    flatui = ["#34FFdb", "#FF3956", "#FFaa71", "#37FF6c"]
    sns.scatterplot(x="MadePercent", y="percentLower", hue=labels, palette=sns.color_palette(flatui, 4), alpha=0.5, legend="brief", s=700, data=df)
    plt.legend(loc="best", markerscale=5, fontsize=45)
    plt.xlim(xmin=0, xmax=1)
    plt.ylim(ymin=.9, ymax=1)
    plt.xticks([.01,.05,.1,.15,.20,.25,.3,.35,.4,.45,.5,.55,.6,.65,.7,.75,.8,.85,.9,.95,1], size=20)
    plt.yticks(size=20)
    plt.xlabel(xlabel, fontsize = 40)
    plt.ylabel("Cumulative Percent of NCAA Players", fontsize = 40)
    plt.title(title, size=50)
    plt.axvline(.5, 0, 1, color="black", linewidth=2)
    plt.show()


# makeMadeGraph("madeNBA_all.xlsx", "NCAA DI Players Probability of Making the NBA", "Chance of Making the NBA", .01)
# makeMadeGraph("wasDrafted_all.xlsx", "NCAA DI Players Probability of being Drafted", "Chance of being drafted", .01)
# makeMadeGraph("firstRound_all.xlsx", "NCAA DI Players Probability of being Drafted in the First Round", "Chance of being drafted in First Round", .01)
# Need to make pallete size = 3 on line 20 because there was no true positives lol
# makeMadeGraph("secondRound_all.xlsx", "NCAA DI Players Probability of being Drafted in the Second Round", "Chance of being drafted in Second Round", .01)
# makeMadeGraph("lotteryPick_all.xlsx", "NCAA DI Players Probability of being a Lottery Pick", "Chance of being a Lottery Pick", .01)


# makeMadeGraph("madeNBA_fresh.xlsx", "NCAA DI Freshmen Probability of Making the NBA", "Chance of Making the NBA", .01)
# makeMadeGraph("wasDrafted_fresh.xlsx", "NCAA DI Freshmen Probability of being Drafted", "Chance of being drafted", .01)
# makeMadeGraph("firstRound_fresh.xlsx", "NCAA DI Freshmen Probability of being Drafted in the First Round", "Chance of being drafted in First Round", .01)
# Need to make pallete size = 1 on line 20 because there was only true negatives... no freshmen outside of first round
# makeMadeGraph("secondRound_fresh.xlsx", "NCAA DI Freshmen Probability of being Drafted in the Second Round", "Chance of being drafted in Second Round", .0)
# makeMadeGraph("lotteryPick_fresh.xlsx", "NCAA DI Freshmen Probability of being a Lottery Pick", "Chance of being a Lottery Pick", .01)


makeMadeGraph("madeNBA_last.xlsx", "NCAA DI Player's Last Year Probability of Making the NBA", "Chance of Making the NBA", .01)
makeMadeGraph("wasDrafted_last.xlsx", "NCAA DI Player's Last Year Probability of being Drafted", "Chance of being drafted", .01)
makeMadeGraph("firstRound_last.xlsx", "NCAA DI Player's Last Year Probability of being Drafted in the First Round", "Chance of being drafted in First Round", .01)
# Need to make pallete size = 1 on line 20 because there was only true negatives... no lastmen outside of first round
makeMadeGraph("secondRound_last.xlsx", "NCAA DI Player's Last Year Probability of being Drafted in the Second Round", "Chance of being drafted in Second Round", .01)
makeMadeGraph("lotteryPick_last.xlsx", "NCAA DI Player's Last Year Probability of being a Lottery Pick", "Chance of being a Lottery Pick", .01)
