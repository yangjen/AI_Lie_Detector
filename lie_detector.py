
# # LIE DETECTOR
def training():
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

	Event = pd.read_csv('model/EventTable.csv')
	Expression = pd.read_csv('model/ExpressionTable.csv')
	Gaze = pd.read_csv('model/GazeTable.csv')
	session_question = pd.read_csv('model/sessionQuestion.csv')
	session = pd.read_csv('model/sessionTable.csv')


	def clean_x(x_data):
		x_df1=x_data.iloc[:,7:]
		x_df1['sessionQuesID']=x_data.iloc[:,1]
		No_quest= len(x_df1['sessionQuesID'].unique())
		features = x_df1.shape[1]-1
		x_clean =[]
		n = 10
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

	# # MODEL 1 - Adaboost, Random Forest Classifier

	train_x, test_x, train_y, test_y = train_test_split(X, Y,test_size=0.3)

	clf_forest = RandomForestClassifier()
	clf_AdaForest = AdaBoostClassifier(n_estimators=50, base_estimator=clf_forest,learning_rate=0.5)
	clf_AdaForest.fit(train_x, train_y)
	prediction1 = np.array(clf_AdaForest.predict(test_x))
	error_model_1 = np.array(1-accuracy_score(test_y, prediction1))


	# # MODEL 2 - Adaboost, DecisionTreeClassifier

	clf_tree = DecisionTreeClassifier(max_depth = 1, random_state = 1)
	clf_AdaTree = AdaBoostClassifier(n_estimators=50, base_estimator=clf_tree,learning_rate=0.5)
	clf_AdaTree.fit(train_x, train_y)
	prediction2 = clf_AdaTree.predict(test_x)
	error_model_2 = np.array(1-accuracy_score(test_y, prediction2))

	# # MODEL 3 - Logistic Regression
	
	clf_log = LogisticRegression()
	clf_AdaLog = AdaBoostClassifier(n_estimators=50, base_estimator=clf_log,learning_rate=0.5)
	clf_AdaLog.fit(train_x, train_y)
	prediction3 = clf_AdaLog.predict(test_x)
	error_model_3 = np.array(1-accuracy_score(test_y, prediction3))

	# # MODEL 4 - SVM classifiers

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

	a = cv_error
	row,column = a.shape
	_position = np.argmin(a)
	m,n = divmod(_position,column)
	cost = cost_range[m]
	gamma = gamma_range[n]

	svm = SVC(C=cost, kernel='rbf', gamma=gamma, probability=True)
	svm.fit(X_train,Y_train)

	dic = {0:clf_AdaForest, 1:clf_AdaTree, 2:clf_AdaLog, 3:svm}
	errors = (error_model_1, error_model_2, error_model_3, error_model_4)
	error_min =min(errors)
	index_min=errors.index(error_min)
	s = pickle.dumps(dic[index_min])


# # RESULTS

def predict_lie(x_user):
	import pickle
	import pandas as pd

	variable = open('x_user.csv',"w")
	for row in x_user: variable.write(row + "\n")
	variable.close()
	x_user2 = pd.read_csv('x_user.csv')
	X_TEST = training.clean_x(x_user2)	
	clf_pred = pickle.loads(s)
	predictors = tuple(clf_pred.predict_proba(X_TEST)[:,1])

	return predictors.index(max(predictors))+1




