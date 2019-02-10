import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
def makeViz():
    df = pd.read_excel("tester.xlsx")
    df = df.sort_values("MadePercent")
    df["Truth Values"] = df["actual"]-df["predicted"]*2
    df = df.reset_index()
    percentLower = []
    for i in range(1, len(df)+1):
        percentLower.append(i/(len(df)+1))
    print(percentLower[2500])
    df["percentLower"] = percentLower
    df = df.drop(df[df.MadePercent<.01].index)
    sns.set_style("whitegrid")

    prediction = {-2: "False Positive", -1:"True Positive", 0:"True Negative", 1: "False Negative"}
    labels = df["Truth Values"].map(prediction)
    flatui = ["#34FFdb", "#FF3956", "#FFaa71", "#37FF6c"]
    sns.scatterplot(x="MadePercent", y="percentLower", hue=labels, palette=sns.color_palette(flatui, 4), alpha=0.75, legend="brief", s=700, data=df)
    plt.legend(loc="best", markerscale=5, fontsize=45)
    plt.xlim(xmin=0, xmax=1)
    plt.ylim(ymin=.975, ymax=1)
    plt.xticks([.05,.1,.15,.20,.25,.3,.35,.4,.45,.5,.55,.6,.65,.7,.75,.8,.85,.9,.95,1], size=20)
    plt.yticks(size=20)
    plt.xlabel("Chance of Making the NBA", fontsize = 40)
    plt.ylabel("Cumulative Percent of NCAA Players", fontsize = 40)
    plt.title("NCAA Players Predicted Probabilities of Making the NBA", size=50)
    plt.axvline(.5, 0, 1, color="black", linewidth=2)
    plt.show()
makeViz()
