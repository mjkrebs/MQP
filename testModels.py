import random
import re

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn import preprocessing


def runModels(seed):
    df = pd.read_excel("NCAA/NCAA_Freshmen_2012_Forward.xlsx")
    # df = pd.read_excel("lastYearOnly.xlsx")
    df.reset_index()

    #this little code snippet removes all seasons for players that aren't their last. It makes sense that we're trying to predict whether or not
    #a 'season' will make the NBA and the player going back for another year of school adds unnecessary noise into the data.

    '''
    lastGrade = 0
    lastrow = None
    lastarr = []
    
    for row in df.itertuples(name='Pandas',index=True):
        currGrade = getattr(row, 'Grade')
        if(lastGrade >= currGrade):
                lastarr.append(lastrow)
        lastGrade = currGrade
        lastrow = row
    lastarr.append(lastrow)
    lastdf = pd.DataFrame(lastarr)
    lastdf.to_excel("lastYearOnly.xlsx")
    exit(1)
    '''

    #FRESHMEN ONLY
    # df = df.loc[df['Grade'] == 1]


    masterframe = df


    df = df.drop(['Year','Pos','FreeAgent'], axis=1)
    df = pd.concat([df.drop('Team',axis=1), pd.get_dummies(df['Team'])],axis=1)


    madeNBA = df.pop('NBA').values
    wasDrafted = df.pop('Drafted').values
    draftPosition = df.pop('Pk').values
    firstRound = df.pop('FirstRound').values
    secondRound = df.pop('SecondRound').values
    lotteryPick = df.pop('Lottery').values
    playerNames = df.pop('Player').values
    # ids = df.pop('ID').values


    colnames = df.columns.values

    result = df

    # ---HERE, CHOOSE WHAT YOU WANT TO PREDICT ---
    # ---OPTIONS ARE: madeNBA, wasDrafted, firstRound, secondRound, lotteryPick
    target = madeNBA
    targetString = ""

    if np.array_equal(target,madeNBA):
        targetString = "madeNBA"
    elif np.array_equal(target,wasDrafted):
        targetString = "wasDrafted"
    elif np.array_equal(target,firstRound):
        targetString = "firstRound"
    elif np.array_equal(target,secondRound):
        targetString = "secondRound"
    elif np.array_equal(target,lotteryPick):
        targetString = "lotteryPick"

    y = target
    X = result.values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, stratify=y, random_state = seed)

    X_test_normal = X_test

    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    logreg = LogisticRegression().fit(X_train, y_train)
    logreg_predictions = logreg.predict(X_test)
    logreg_proba = logreg.predict_proba(X_test)

    dtree = DecisionTreeClassifier().fit(X_train,y_train)
    dtree_predictions = dtree.predict(X_test)
     
    rfor = RandomForestClassifier(n_estimators=100).fit(X_train,y_train)
    rfor_predictions = rfor.predict(X_test)

    # cnn = MLPClassifier(learning_rate='adaptive',batch_size=400,activation='relu',hidden_layer_sizes =[1000,800,600,400,200,100,80,60,40,20,2],max_iter=1000)
    # cnn.fit(X_train,y_train)
    # cnn_predictions = cnn.predict(X_test)

    lr = classification_report(y_test, logreg_predictions, target_names=['No NBA', 'Made NBA'])
    dt = classification_report(y_test, dtree_predictions, target_names =['No NBA', 'Made NBA'])
    rf = classification_report(y_test, rfor_predictions, target_names =['No NBA', 'Made NBA'])
    # mp = classification_report(y_test, cnn_predictions, target_names=['No NBA', 'Made NBA'])
    mp = "Made NBA 0.1 0.1 0.1"
    lr_R = re.findall(r'Made NBA +(0.\d+) +(0.\d+) +(0.\d+)', lr)
    dt_R = re.findall(r'Made NBA +(0.\d+) +(0.\d+) +(0.\d+)', dt)
    rf_R = re.findall(r'Made NBA +(0.\d+) +(0.\d+) +(0.\d+)', rf)
    mp_R = re.findall(r'Made NBA +(0.\d+) +(0.\d+) +(0.\d+)', mp)
    
    return (lr_R, dt_R, rf_R,mp_R)
    
    
def testModels():
    fout = open("testModels.txt", "w+")
    lrA = 0
    dtA = 0
    rfA = 0
    mpA = 0

    lrM = 0
    dtM = 0
    rfM = 0
    mpM = 0
    num = 0
    for i in range(0,6):
        currResult = runModels(random.randint(1,50))
        lr = currResult[0]
        dt = currResult[1]
        rf = currResult[2]
        mp = currResult[3]
        
        if(float(float(lr[0][2])) > lrM):
            lrM = float(lr[0][2])
        if (float(dt[0][2]) > dtM):
            dtM = float(dt[0][2])
        if (float(rf[0][2]) > rfM):
            rfM = float(rf[0][2])
        if (float(mp[0][2]) > mpM):
            mpM = float(mp[0][2])

        lrA = lrA + float(lr[0][2])
        dtA = dtA + float(dt[0][2])
        rfA = rfA + float(rf[0][2])
        mpA = mpA + float(mp[0][2])
        num += 1
        print("Next Trial")
    lrA = lrA/num
    dtA = dtA/num
    rfA = rfA/num
    mpA = mpA/num
    fout.write("Average F1 Scores:\n")
    fout.write("LogReg: " + str(lrA))
    fout.write("\nDecision Tree: " + str(dtA))
    fout.write("\nRandom Forest: " + str(rfA))
    fout.write("\nMultilayer Perceptron: " + str(mpA))

    fout.write("\nMax F1 Scores:\n")
    fout.write("\nLogReg: " + str(lrM))
    fout.write("\nDecision Tree: " + str(dtM))
    fout.write("\nRandom Forest: " + str(rfM))
    fout.write("\nMultilayer Perceptron: " + str(mpM))


# testModels()




        
        