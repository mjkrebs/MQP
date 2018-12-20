import numpy as np 
import pandas as pd
import sys
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

df_list = list()

# for x in range(2015,2019):
# 	df = pd.read_excel("all_NCAA_players_"+str(x) + ".xlsx")
# 	drop Pos as already added dummies in Excel
	# df = df.drop(columns = ['Pos'])
	# Drop the irrelevant ID variables
	# df = df.drop(columns = ['Player','Year'])
	# Concatenate the dataframe without the team variable with the dataframe which has the dummy variables for the team
	# df = pd.concat([df.drop('Team',axis=1), pd.get_dummies(df['Team'])],axis=1)
	# df_list.append(df)



result = pd.read_excel("all_NCAA_2015_2018.xlsx")
# result = pd.read_excel("Forwards_2015_2018.xlsx")

# result = pd.concat(df_list)
result = result.drop(['Player','Year', 'DraftPos'], axis=1)
result = pd.get_dummies(result, columns = ["Team", "Pos"] )

# sys.stdout = open('outputs.txt', 'w')
test = ""
for i in range(0,1):
    if i==0:
        test = "NBA"
        curr = result.drop(['Drafted', 'FirstRound', 'SecondRound', 'Lottery', 'FreeAgent'], axis=1)
    elif i==1:
        test="Drafted"
        curr = result.drop(['NBA', 'FirstRound', 'SecondRound', 'Lottery', 'FreeAgent'], axis=1)
    elif i==2:
        test="FirstRound"
        curr = result.drop(['Drafted', 'NBA', 'SecondRound', 'Lottery', 'FreeAgent'], axis=1)
    elif i==3:
        test="SecondRound"
        curr = result.drop(['Drafted', 'FirstRound', 'NBA', 'Lottery', 'FreeAgent'], axis=1)
    elif i==4:
        test="Lottery"
        curr = result.drop(['Drafted', 'FirstRound', 'SecondRound', 'NBA', 'FreeAgent'], axis=1)
    elif i==5:
        test = "FreeAgent"
        curr = result.drop(['Drafted', 'FirstRound', 'SecondRound', 'Lottery', 'NBA'], axis=1)
    print("\n\n" + test)
    y = curr.pop(test).values
    X = curr.values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30)

    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    logreg = LogisticRegression().fit(X_train, y_train)
    logreg_predictions = logreg.predict(X_test)


    dtree = DecisionTreeClassifier().fit(X_train,y_train)
    dtree_predictions = dtree.predict(X_test)

    rfor = RandomForestClassifier(n_estimators=100).fit(X_train,y_train)
    rfor_predictions = rfor.predict(X_test)

    cnn = MLPClassifier().fit(X_train,y_train)
    cnn_predictions = cnn.predict(X_test)


    if i==0:
        t_names = ['No NBA', 'Made NBA']
    elif i==1:
        t_names = ['Not Drafted', 'Drafted']
    elif i==2:
        t_names = ['Not FirstRound', 'Made FirstRound']
    elif i==3:
        t_names = ['Not SecondRound', 'Made SecondRound']
    elif i==4:
        t_names = ['Not Lottery', 'Lottery']
    elif i==5:
        t_names = ['Not Free Agent', 'Free Agent']
    print("Logistic Regression")
    print(classification_report(y_test, logreg_predictions, target_names =t_names))
    # print("Decision Tree")
    # print(classification_report(y_test, dtree_predictions, target_names =t_names))
    # print("Random Forest")
    # print(classification_report(y_test, rfor_predictions, target_names =t_names))
    print("Multilayer Perceptron")
    print(classification_report(y_test, cnn_predictions, target_names =t_names))

    # print(logreg.coef_)
    print("====================================================================\n====================================================================")






