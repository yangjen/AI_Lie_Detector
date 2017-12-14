import os
import pandas as pd
import numpy as np
import pickle


def clean_x(x_data):
    x_df1 = x_data.iloc[:, 7:]
    x_df1['sessionQuesID'] = x_data.iloc[:, 1]
    No_quest = len(x_df1['sessionQuesID'].unique())
    features = x_df1.shape[1] - 1
    x_clean = []
    n = 10
    for i in range(No_quest):
        x1 = x_df1[x_df1['sessionQuesID'] == i + 1]
        x1 = x1.drop(['sessionQuesID'], axis=1)
        No_data = int(x1.shape[0] / n)
        a = 0
        for j in range(n):
            x_clean.extend(np.mean(x1.iloc[a:a + No_data, :], axis=0).values.tolist())
            a = a + No_data
    x_clean = np.reshape(x_clean, (No_quest, n * features))
    return x_clean


def clean_y(y_data):
    y_clean = y_data.iloc[1:, 4].values.tolist()
    return y_clean


# # LIE DETECTOR
def training():
    print("Training the Lie Detector")
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score
    from sklearn.datasets import load_digits
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import KFold
    from sklearn.svm import SVC
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.linear_model import LogisticRegression

    Event = pd.read_csv('model/EventTable.csv')
    Expression = pd.read_csv('model/ExpressionTable.csv')
    Gaze = pd.read_csv('model/GazeTable.csv')
    session_question = pd.read_csv('model/sessionQuestion.csv')
    session = pd.read_csv('model/sessionTable.csv')

    X = clean_x(Expression)
    Y = np.array(clean_y(session_question))

    train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size=0.3)

    # # MODEL 1 - Adaboost, Random Forest Classifier

    print("MODEL 1 - Adaboost, Random Forest Classifier")

    clf_forest = RandomForestClassifier()
    clf_AdaForest = AdaBoostClassifier(n_estimators=50, base_estimator=clf_forest,learning_rate=0.5)
    clf_AdaForest.fit(train_x, train_y)
    prediction1 = np.array(clf_AdaForest.predict(test_x))
    error_model_1 = np.array(1-accuracy_score(test_y, prediction1))

    # # MODEL 2 - Adaboost, DecisionTreeClassifier

    print("MODEL 2 - Adaboost, DecisionTreeClassifier")

    clf_tree = DecisionTreeClassifier(max_depth = 1, random_state = 1)
    clf_AdaTree = AdaBoostClassifier(n_estimators=50, base_estimator=clf_tree,learning_rate=0.5)
    clf_AdaTree.fit(train_x, train_y)
    prediction2 = clf_AdaTree.predict(test_x)
    error_model_2 = np.array(1-accuracy_score(test_y, prediction2))

    # # MODEL 3 - Logistic Regression
    
    print("MODEL 3 - Logistic Regression")

    clf_log = LogisticRegression()
    clf_AdaLog = AdaBoostClassifier(n_estimators=50, base_estimator=clf_log,learning_rate=0.5)
    clf_AdaLog.fit(train_x, train_y)
    prediction3 = clf_AdaLog.predict(test_x)
    error_model_3 = np.array(1-accuracy_score(test_y, prediction3))

    # # MODEL 4 - SVM classifiers

    print("MODEL 4 - SVM classifiers")

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

    for i in range(num_costs):
        for j in range(num_gammas):
            error_test_count = 0
            svm = SVC(C=cost_range[i],kernel='rbf',gamma=gamma_range[j])
            for train_indice, test_indice in kf.split(X):
                X_train, X_test = X[train_indice],X[test_indice]
                Y_train, Y_test = Y[train_indice],Y[test_indice]

                svm.fit(X_train,Y_train)
                predicted_Y_test = svm.predict(X_test)
                error_test = Y_test!= predicted_Y_test
                error_test_count += sum(error_test)

            cv_error[i,j] = error_test_count/K

    a = cv_error
    row,column = a.shape
    _position = np.argmin(a)
    m,n = divmod(_position,column)
    cost = cost_range[m]
    gamma = gamma_range[n]

    svm = SVC(C=cost, kernel='rbf', gamma=gamma, probability=True)
    svm.fit(train_x,train_y)
    prediction4 = svm.predict(test_x)
    error_model_4 = np.array(1 - accuracy_score(test_y, prediction4))

    # # Choose the best model

    print("Choosing the model...")

    dic = {0:clf_AdaForest, 1:clf_AdaTree, 2:clf_AdaLog, 3:svm}
    errors = (error_model_1, error_model_2, error_model_3, error_model_4)
    error_min =min(errors)
    index_min=errors.index(error_min)

    print("Saving the model...")

    pickle_out = open("model/model.pickle",'wb')
    pickle.dump(dic[index_min], pickle_out)
    pickle_out.close()

    print("Done!")


# # RESULTS
def predict_lie(x_user):
    variable = open('model/x_user.csv',"w")
    for row in x_user: variable.write(row + "\n")
    variable.close()
    x_user2 = pd.read_csv('model/x_user.csv')
    os.remove('model/x_user.csv')

    X_TEST = clean_x(x_user2)

    pickle_in = open("model/model.pickle",'rb')
    clf_pred = pickle.load(pickle_in)
    pickle_in.close()

    predictors = tuple(clf_pred.predict_proba(X_TEST)[:,1])

    return predictors.index(max(predictors))+1
