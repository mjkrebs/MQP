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


df = pd.read_excel("NCAA/NCAA_Freshmen_2012_Forward.xlsx")


#this little code snippet removes all seasons for players that aren't their last. It makes sense that we're trying to predict whether or not
#a 'season' will make the NBA and the player going back for another year of school adds unnecessary noise into the data. 
"""
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
"""

#FRESHMEN ONLY
df = df.loc[df['Grade'] == 1]


masterframe = df
df = df.drop(columns = ['Year','Pos','FreeAgent'])
df = pd.concat([df.drop('Team',axis=1), pd.get_dummies(df['Team'])],axis=1)


madeNBA = df.pop('NBA').values
wasDrafted = df.pop('Drafted').values
draftPosition = df.pop('Pk').values
firstRound = df.pop('FirstRound').values
secondRound = df.pop('SecondRound').values
lotteryPick = df.pop('Lottery').values
playerNames = df.pop('Player').values
ids = df.pop('ID').values


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

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, stratify=y, random_state = 42)

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


cnn = MLPClassifier(learning_rate='adaptive',batch_size=400,activation='relu',hidden_layer_sizes =[1000,800,600,400,200,100,80,60,40,20,2],max_iter=1000)
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

#code to display coefficients
"""
coefs = logreg.coef_[0]
indices = np.argsort(coefs)
coefs.sort()


for i in range(0,len(indices)):
	print(colnames[indices[i]])
	print(coefs[i])
"""

#for each misclassified row, find the corresponding name in the master dataframe
#print(misclassified_samples)
#for row in misclassified_samples:
probs = logreg_proba[y_test != logreg_predictions]
prediction = logreg_predictions[y_test != logreg_predictions]
actuals = y_test[y_test != logreg_predictions]
array = X_test_normal[y_test != logreg_predictions]
frame = pd.DataFrame(columns = colnames, data=array)

for index, row in frame.iterrows():
	print(index)
	height = getattr(row, 'Height')
	pts = getattr(row,'PTS')
	fga = getattr(row,'FGA')
	pprod = getattr(row,'PProd')
	player = masterframe.loc[masterframe['Height'] == height]
	player = player.loc[player['PTS'] == pts]
	player = player.loc[player['FGA'] == fga]
	player = player.loc[player['PProd'] == pprod]
	print(player['Player'].values + ": " + str(probs[index]) + " Pos: " + player['Pos'].values +  " Height: " + str(player['Height'].values) + " School: " + player['Team'].values + " Year: " + player['Year'].values + " Predicted: " + str(prediction[index]) + " Actual: " + str(actuals[index]))
	
