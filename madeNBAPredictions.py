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

df_list = list()

for x in range(2015,2019):
	df = pd.read_excel("all_NCAA_players_"+str(x) + ".xlsx")
	#drop Pos as already added dummies in Excel
	df = df.drop(columns = ['Pos'])
	#Drop the irrelevant ID variables
	df = df.drop(columns = ['Player','Year'])
	#Concatenate the dataframe without the team variable with the dataframe which has the dummy variables for the team
	df = pd.concat([df.drop('Team',axis=1), pd.get_dummies(df['Team'])],axis=1)
	df_list.append(df)

result = pd.concat(df_list)
y = result.pop('NBA').values
X = result.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)

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

print("Logistic Regression")
print(classification_report(y_test, logreg_predictions, target_names =['No NBA', 'Made NBA']))
print("Decision Tree")
print(classification_report(y_test, dtree_predictions, target_names =['No NBA', 'Made NBA']))
print("Random Forest")
print(classification_report(y_test, rfor_predictions, target_names =['No NBA', 'Made NBA']))
print("Multilayer Perceptron")
print(classification_report(y_test, cnn_predictions, target_names =['No NBA', 'Made NBA']))








