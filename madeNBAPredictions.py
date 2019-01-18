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


df = pd.read_excel("Forwards_2015_2018.xlsx")

#this little code snippet removes all seasons for players that aren't their last. It makes sense that we're trying to predict whether or not
#a 'season' will make the NBA and the player going back for another year of school adds unnecessary noise into the data. 
i = 0
print (len(df.index))
for row in df.itertuples(name='Pandas',index=True):
	if(i+1 == len(df.index)):
		break
	nextrow = df.iloc[i+1]
	rowname = getattr(row,'Player')
	nextrowname = getattr(nextrow,'Player')
	rowindex = row[0]
	i += 1
	if(rowname == nextrowname):
		df = df.drop(rowindex,axis='index')
print(len(df.index))		

df = df.drop(columns = ['Player','Year'])
df = pd.concat([df.drop('Team',axis=1), pd.get_dummies(df['Team'])],axis=1)
df = pd.concat([df.drop('Pos',axis = 1), pd.get_dummies(df['Pos'])],axis =1)

madeNBA = df.pop('NBA').values
wasDrafted = df.pop('Drafted').values
draftPosition = df.pop('DraftPos').values
firstRound = df.pop('FirstRound').values
secondRound = df.pop('SecondRound').values
lotteryPick = df.pop('Lottery').values

#Need to normalize the data!!!
min_max_scaler = preprocessing.MinMaxScaler()
np_scaled = min_max_scaler.fit_transform(df)
df = pd.DataFrame(np_scaled)

result = df

# ---HERE, CHOOSE WHAT YOU WANT TO PREDICT ---
# ---OPTIONS ARE: madeNBA, wasDrafted, firstRound, secondRound, lotteryPick
# ---draftPosition will need a regression & not classification!!!---
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

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, stratify=y, random_state=42)

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


cnn = MLPClassifier(learning_rate='adaptive',batch_size=400,activation='relu',hidden_layer_sizes=[100,80,60,40,20,2],max_iter=10)
cnn.fit(X_train,y_train)
cnn_predictions = cnn.predict(X_test)

print("Metrics for: " + targetString)
print("Logistic Regression")
print(classification_report(y_test, logreg_predictions, target_names =['No NBA', 'Made NBA']))
print("Decision Tree")
print(classification_report(y_test, dtree_predictions, target_names =['No NBA', 'Made NBA']))
print("Random Forest")
print(classification_report(y_test, rfor_predictions, target_names =['No NBA', 'Made NBA']))
print("Multilayer Perceptron")
print(classification_report(y_test, cnn_predictions, target_names =['No NBA', 'Made NBA']))



master_df = pd.read_excel("all_NCAA_2015_2018.xlsx")

misclassified_samples = X_test[y_test != logreg_predictions]

#for each misclassified row, find the corresponding name in the master dataframe
print(misclassified_samples)
#for row in misclassified_samples:



