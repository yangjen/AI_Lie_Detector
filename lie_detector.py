
# # LIE DETECTOR

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.datasets import load_digits
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import KFold
from sklearn.svm import SVC
import pickle

Event = pd.read_csv('D:/programmin for business/group project/DataTablesCSV/DataTablesCSV/EventTable.csv')
Expression = pd.read_csv('D:/programmin for business/group project/DataTablesCSV/DataTablesCSV/ExpressionTable.csv')
Gaze = pd.read_csv('D:/programmin for business/group project/DataTablesCSV/DataTablesCSV/GazeTable.csv')
session_question = pd.read_csv('D:/programmin for business/group project/DataTablesCSV/DataTablesCSV/sessionQuestion.csv')
session = pd.read_csv('D:/programmin for business/group project/DataTablesCSV/DataTablesCSV/sessionTable.csv')


def clean_x(x_data):
    x_df1=x_data.iloc[:,7:]
    x_df1['sessionQuesID']=x_data.iloc[:,1]
    No_quest = np.max(x_df1['sessionQuesID'])
    features = x_df1.shape[1]-1
    x_clean =[]
    n = 5

    for i in range(No_quest):
        x1 = x_df1[x_df1['sessionQuesID']==i+1]
        x1 = x1.drop(['sessionQuesID'], axis=1)
        No_data = int(x1.shape[0]/n)
        a=0
        for j in range(n):     
            x_clean.extend(np.mean(x1.iloc[a:a+No_data,:], axis=0).values.tolist())
            a=a+No_data
    x_clean=np.reshape(x_clean, (No_quest,n*features))
    return x_clean

def clean_y(y_data):
    y_clean = y_data.iloc[1:,4].values.tolist()
    return y_clean

X= clean_x(Expression)
Y= np.array(clean_y(session_question))


print(X.shape)
print(Y)

# # MODEL 1 - Random Forest Classifier

train_x, test_x, train_y, test_y = train_test_split(X, Y,test_size=0.3)

clf_forest = RandomForestClassifier()
clf_forest.fit(train_x, train_y)
predictions = clf_forest.predict(test_x)
#predictions2 = clf.predict(train_x)
#prediction1 = np.array(clf_forest.predict_proba(X_TEST_clean))[:,1]
error_model_1 = np.array(1-accuracy_score(test_y, predictions))
#print ("Train Accuracy :: ", accuracy_score(train_y, predictions2))
print (error_model_1)
#print(prediction1)

#visualize_classifier(clf,train_x, train_y)


# # MODEL 2 - ADABOOST 


def get_error_rate(pred, Y):
    return sum(pred != Y) / float(len(Y))

def print_error_rate(err):
    print('Error rate: Training: %.4f - Test: %.4f' % err)

def generic_clf(Y_train, X_train, Y_test, X_test, clf):
    clf.fit(X_train,Y_train)
    pred_train = clf.predict(X_train)
    pred_test = clf.predict(X_test)
    return get_error_rate(pred_train, Y_train),            get_error_rate(pred_test, Y_test)
    
def adaboost_clf(Y_train, X_train, Y_test, X_test, M, clf):
    n_train, n_test = len(X_train), len(X_test)
    # Initialize weights
    w = np.ones(n_train) / n_train
    pred_train, pred_test = [np.zeros(n_train), np.zeros(n_test)]
    
    for i in range(M):
        # Fit a classifier with the specific weights
        clf.fit(X_train, Y_train, sample_weight = w)
        pred_train_i = clf.predict(X_train)
        pred_test_i = clf.predict(X_test)
        # Indicator function
        miss = [int(x) for x in (pred_train_i != Y_train)]
        # Equivalent with 1/-1 to update weights
        miss2 = [x if x==1 else -1 for x in miss]
        # Error
        err_m = np.dot(w,miss) / sum(w)
        # Alpha
        alpha_m = 0.5 * np.log( (1 - err_m) / float(err_m))
        # New weights
        w = np.multiply(w, np.exp([float(x) * alpha_m for x in miss2]))
        # Add to prediction
        pred_train = [sum(x) for x in zip(pred_train, [x * alpha_m for x in pred_train_i])]
        pred_test = [sum(x) for x in zip(pred_test, [x * alpha_m for x in pred_test_i])]

    
    pred_train, pred_test = np.sign(pred_train), np.sign(pred_test)
    # Return error rate in train and test set
    return get_error_rate(pred_test, Y_test)

def adaboost_clf2(Y_train, X_train, X_test, M, clf):
    n_train, n_test = len(X_train), len(X_test)
    # Initialize weights
    w = np.ones(n_train) / n_train
    pred_train, pred_test = [np.zeros(n_train), np.zeros(n_test)]
    
    for i in range(M):
        # Fit a classifier with the specific weights
        clf.fit(X_train, Y_train, sample_weight = w)
        pred_train_i = clf.predict(X_train)
        pred_test_i = clf.predict_proba(X_test)
        #print(pred_test_i)
        # Indicator function
        miss = [int(x) for x in (pred_train_i != Y_train)]
        # Equivalent with 1/-1 to update weights
        miss2 = [x if x==1 else -1 for x in miss]
        # Error
        err_m = np.dot(w,miss) / sum(w)
        # Alpha
        alpha_m = 0.5 * np.log( (1 - err_m) / float(err_m))
        # New weights
        w = np.multiply(w, np.exp([float(x) * alpha_m for x in miss2]))
        # Add to prediction
        pred_test = [sum(x) for x in zip(pred_test, [x * alpha_m for x in pred_test_i])]
    #pred_test = np.sign(pred_test)
    return pred_test
#.clip(min=0)
df = pd.DataFrame(X)
df['Y'] = Y
train, test = train_test_split(df, test_size = 0.3)
X_train, Y_train = train.iloc[:,:-1], train.iloc[:,-1]
X_test, Y_test = test.iloc[:,:-1], test.iloc[:,-1]
clf_tree = DecisionTreeClassifier(max_depth = 1, random_state = 1)
er_tree = generic_clf(Y_train, X_train, Y_test, X_test, clf_tree)   
er_train, er_test = [er_tree[0]], [er_tree[1]]
#x_range = range(10, 410, 10)
# i in x_range:
error_model_2 = np.array(adaboost_clf(Y_train, X_train, Y_test, X_test, 50, clf_tree))
# Compare error rate vs number of iterations
print(error_model_2)
#prediction2 = np.array(adaboost_clf2(Y_train, X_train, X_TEST_clean, 1, clf_tree))[:,1]
#print(prediction2)


# # MODEL 3 - Convolutional and LSTM neuronal networks


# #SVM classifiers

# # MODEL 4 - SVM

def logsample(start, end, num):
    return np.logspace(np.log10(start), np.log10(end), num, base=10.0)

num_gammas = 20   
num_costs = 20
gamma_range = logsample(1e-1, 1e3, num_gammas)
cost_range = logsample(1e-1, 1e3, num_costs)

# Training the model with previous data saved in database
K = 6  # number of folds for cross validation
kf = KFold(n_splits=K)
cv_error = np.zeros((num_gammas, num_costs))  # error matrix
error_train_array = []
error_test_array = []

error_model_4 = []


for i in range(num_costs):
    for j in range(num_gammas):
        error_train = 0
        error_test = 0
        error_train_count = 0
        error_test_count = 0
        svm = SVC(C=cost_range[i],kernel='rbf',gamma=gamma_range[j])
        for train_indice, test_indice in kf.split(X):
            X_train, X_test = X[train_indice],X[test_indice]
            Y_train, Y_test = Y[train_indice],Y[test_indice]
            
            svm.fit(X_train,Y_train)
            
            predicted_Y_train = svm.predict(X_train)
            error_train = (Y_train!= predicted_Y_train)
            error_train_count += sum(error_train)
            error_train_array.append(error_train)
            
            predicted_Y_test = svm.predict(X_test)
            error_test = Y_test!= predicted_Y_test
            error_test_count += sum(error_test)
            error_test_array.append(error_test)
            
            error_train_rate = np.mean(error_train_array)
            error_model_4 = np.mean(error_test_array)
            
        cv_error[i,j] = error_train_count/10

#print("error_train =", error_train_rate*100)
print(error_model_4)


# Find the best parameter combinatio with minimzing the error
a = cv_error
row,column = a.shape
_position = np.argmin(a)
m,n = divmod(_position,column)
cost = cost_range[m]
gamma = gamma_range[n]

# Train the SVM classifier using these parameters
svm = SVC(C=cost, kernel='rbf', gamma=gamma, probability=True)
svm.fit(X_train,Y_train)

# Making guess for the real session 

#prediction4 = svm.predict_proba(X_TEST_clean)[:,1]
#print(prediction4)

dic = {0: clf_forest, 1:clf_tree, 2:svm}
errors = (error_model_1, error_model_2, error_model_4)
error_min =min(errors)
index_min=errors.index(error_min)
s = pickle.dumps(dic[index_min])


# # RESULTS

def predict_lie(x_user):
	import pickle
	import pandas as pd
	import csv
    #X_TEST = pd.read_csv('D:/programmin for business/group project/DataTablesCSV/DataTablesCSV/Expression_test.csv')
	print(type(x_user[1]))
	print(len(x_user))
	with open("x_user.csv", "w") as f:  # open("output.csv","wb") for Python 2
		cw = csv.writer(f)
		cw.writerows(x_user)
	#x_data = pd.DataFrame([x_user[1].split(","),x_user[2].split(","),x_user[3].split(",")],columns=(x_user[0].split(",")))
	x_user2 = pd.read_csv('x_user.csv')
	x_data = pd.DataFrame(x_user2)
	x_df1=x_data.iloc[:,7:]
	x_df1['sessionQuesID']=x_data.iloc[:,1]
	No_quest = int(np.max(x_df1['sessionQuesID']))
	features = x_df1.shape[1]-1
	X_TEST =[]
	n = 5
	for i in range(No_quest):
		x1 = x_df1[x_df1['sessionQuesID']==i+1]
		x1 = x1.drop(['sessionQuesID'], axis=1)
		No_data = int(x1.shape[0]/n)
		a=0
		for j in range(n):
			X_TEST.extend(np.mean(x1.iloc[a:a+No_data,:], axis=0).values.tolist())
			a=a+No_data
	X_TEST=np.reshape(X_TEST, (No_quest,n*features))
	clf_pred = pickle.loads(s)
	predictors = tuple(clf_pred.predict_proba(X_TEST)[:,1])

#predictors = (prediction1, prediction2, prediction4)
#pred = tuple(predictors[index_min])

#print("I am "+str(int(100-(error_min*100)))+"% sure that", choices[pred])
	return predictors.index(max(predictors))+1




