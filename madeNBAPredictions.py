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

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, stratify=y, random_state = 42)

X_test_normal = X_test

scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

logreg = LogisticRegression().fit(X_train, y_train)
logreg_predictions = logreg.predict(X_test)
logreg_proba = logreg.predict_proba(X_test)

# dtree = DecisionTreeClassifier().fit(X_train,y_train)
# dtree_predictions = dtree.predict(X_test)

# rfor = RandomForestClassifier(n_estimators=100).fit(X_train,y_train)
# rfor_predictions = rfor.predict(X_test)


# cnn = MLPClassifier(learning_rate='adaptive',batch_size=400,activation='relu',hidden_layer_sizes =[1000,800,600,400,200,100,80,60,40,20,2],max_iter=1000)
# cnn.fit(X_train,y_train)
# cnn_predictions = cnn.predict(X_test)


print("Metrics for: " + targetString)
print("Logistic Regression")
print(classification_report(y_test, logreg_predictions, target_names =['No NBA', 'Made NBA']))
# print("Decision Tree")
# print(classification_report(y_test, dtree_predictions, target_names =['No NBA', 'Made NBA']))
# print("Random Forest")
# print(classification_report(y_test, rfor_predictions, target_names =['No NBA', 'Made NBA']))
# print("Multilayer Perceptron")
# print(classification_report(y_test, cnn_predictions, target_names =['No NBA', 'Made NBA']))

'''
print("Metrics for: " + targetString)
print("Logistic Regression")
if np.array_equal(target,madeNBA):
	print(classification_report(y_test, logreg_predictions, target_names=['No NBA', 'Made NBA']))
elif np.array_equal(target,wasDrafted):
	print(classification_report(y_test, logreg_predictions, target_names=['Not Drafted', 'Drafted']))
elif np.array_equal(target,firstRound):
	print(classification_report(y_test, logreg_predictions, target_names=['Not First Round', 'First Round']))
elif np.array_equal(target,secondRound):
	print(classification_report(y_test, logreg_predictions, target_names=['Not Second Round', 'Second Round']))
elif np.array_equal(target,lotteryPick):
	print(classification_report(y_test, logreg_predictions, target_names=['Not Lottery', 'Lottery']))
'''
#code to display coefficients
"""
coefs = logreg.coef_[0]
indices = np.argsort(coefs)
coefs.sort()


for i in range(0,len(indices)):
	print(colnames[indices[i]])
	print(coefs[i])
"""

'''
probs = logreg_proba[y_test != logreg_predictions]
prediction = logreg_predictions[y_test != logreg_predictions]
actuals = y_test[y_test != logreg_predictions]
array = X_test_normal[y_test != logreg_predictions]
frame = pd.DataFrame(columns = colnames, data=array)

made = open("Plot/Results/" + targetString + "_made_last.txt", "w+")
no = open("Plot/Results/" + targetString + "_not_last.txt", "w+")
columnName = ""

if np.array_equal(target,madeNBA):
	columnName = "NBA"
elif np.array_equal(target,wasDrafted):
	columnName = "Drafted"
elif np.array_equal(target,firstRound):
	columnName = "FirstRound"
elif np.array_equal(target,secondRound):
	columnName = "SecondRound"
elif np.array_equal(target,lotteryPick):
	columnName = "Lottery"
for index, row in frame.iterrows():
	# print(index)
	height = getattr(row, 'Height')
	pts = getattr(row,'PTS')
	fga = getattr(row,'FGA')
	pprod = getattr(row,'PProd')
	player = masterframe.loc[masterframe['Height'] == height]
	player = player.loc[player['PTS'] == pts]
	player = player.loc[player['FGA'] == fga]
	player = player.loc[player['PProd'] == pprod]
	if(player[columnName].values[0]==0):
		no.write(str(player['Player'].values) + ": " + str(probs[index]) + " Year: " + str(player['Year'].values) + " Predicted: " +
				 str(prediction[index]) + " Actual: " + str(actuals[index]) + "\n")
	else:
		made.write(str(player['Player'].values) + ": " + str(probs[index]) + " Year: " + str(
			player['Year'].values) + " Predicted: " + str(prediction[index]) + " Actual: " + str(actuals[index]) + "\n")

allprobs = pd.DataFrame(logreg_proba)
allprobs.columns = ["MissedPercent", "MadePercent"]
allprobs["actual"] = y_test
allprobs["predicted"] = logreg_predictions
allprobs.to_excel("Plot/Results/" + targetString + "_last.xlsx")


# print(player['Player'].values + ": " + str(probs[index]) + " Pos: " + player['Pos'].values +  " Height: " + str(player['Height'].values) + " School: " + player['Team'].values + " Year: " + player['Year'].values + " Predicted: " + str(prediction[index]) + " Actual: " + str(actuals[index]))
'''
