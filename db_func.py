import random
import pymysql
import re
import time
import math

# Debugging
print_debug = False

# Check if I have connection to the DataBase
use_database = True
try:
    if print_debug: print("Im trying to connect...")
    db = pymysql.connect("localhost", "root", "weisi9527sj", "P5BA")
    use_database = True
except:
    use_database = False
#use_database = False
print("use_database:",use_database)

# Global variables
if use_database: cursor = db.cursor()
questions_id=[]
sessionQues=[]


# Prepare the questions to send to index.html (from txt file)
def db_get_input_csv():
    session_id = str(math.floor(time.time()))
    with open("static/questions.txt", "r") as myfile:
        data=myfile.read().splitlines()
        sample_questions = random.sample(data, 3)
    return session_id,sample_questions


# Prepare the questions to send to index.html
def db_get_input():
    sample_questions=[]
    session_id="0"

    # Get last sessionQues_id
    if use_database:
        sql_getSessionQuesID = "select * from Session_question order by sessionQuesID desc limit 1"
        cursor.execute(sql_getSessionQuesID)
        results = cursor.fetchall()[0]
        sessionQues_id = results[0]
    else:
        sessionQues_id = 0

    global sessionQues
    sessionQues = [str(int(sessionQues_id) + 1), str(int(sessionQues_id) + 2), str(int(sessionQues_id) + 3)]
    if print_debug: print("<<<<<<<<<<<<<<<<")
    if print_debug: print(sessionQues)

    if use_database:
        try:
            # Ask for Session ID
            sql = "select * from Session order by sessionID desc limit 1"
            cursor.execute(sql)
            results = cursor.fetchall()[0]
            session_id = str(results[0]+1)

            # Get timestamp
            sessionTimestamp =str(int(time.time()*1000))

            # Store the new session
            sql_sess = "INSERT INTO Session(sessionID, sessionTimestamp) VALUES ("+session_id+","+sessionTimestamp+")"
            if print_debug: print("p---------------------")
            if print_debug: print(sql_sess)
            cursor.execute(sql_sess)

            # Select 3 questions
            sql_question = "select * from Question"
            cursor.execute(sql_question)
            questions_table = cursor.fetchall()
            questions_no = len(questions_table)
            questions_id = random.sample(range(questions_no),3)

            # Store the questions for the session
            for seq in range(3):
                question = str(questions_id[seq])
                sequen = str(seq + 1)
                sql_prediction = "insert into Session_question(sessionQuesID,sessionID,questionID,sequence) values(" + sessionQues[seq] + "," + session_id + "," + question + "," + sequen + ")"
                if print_debug: print(sql_prediction)
                cursor.execute(sql_prediction)

            # Save the questions String
            for q_id in questions_id:
                question = questions_table[q_id][1]
                sample_questions = sample_questions + [question]

            # Save the questions ID
            for i in range(3):
                questions_id[i]=str(questions_id[i]+1)
                if print_debug: print(questions_id)

            # Commit
            db.commit()
        except:
            # if fail, roll back
            db.rollback()
            if print_debug: print("sad_ques")
            db.close()
        return session_id,sample_questions
    else:
        return db_get_input_csv()

# Process the results from index.html
def db_store_results(session_id,log_affdex,log_xlabs,log_events):
    # =========== Write Table LogEvent ===========
    log_events = log_events[:len(log_events)-1]
    stamps = []
    for eachEvent in log_events:
        # Get values
        eventTimestamp = eachEvent.split(',')[0].split(':')[1]
        event = eachEvent.split(',')[1].split(':')[1].strip('}"')
        if event.find("question")!=-1:
            stamps = stamps + [eventTimestamp]

        if use_database:
            try:
                sql_logEvent = "INSERT INTO LogEvent(sessionID,eventTimestamp,logEvent) VALUES ("+session_id+","+eventTimestamp+","+"\""+event+"\")"
                if print_debug: print(sql_logEvent)
                if print_debug: print("Events running well!!")
                cursor.execute(sql_logEvent)
            except:
                db.rollback()
                if print_debug: print("event..................")
    # =========== Write Table LogEvent ok ===========

    # =========== Write Table Expression =============
    columns_Expression = "sessionQuesID,expTimestamp,gender,glasses,age,ethnicity,joy,sadness,disgust,contempt,anger,fear,surprise,valence,engagement,smile,innerBrowRaise,browRaise,browFurrow,noseWrinkle,upperLipRaise,lipCornerDepressor,chinRaise,lipPucker,lipPress,lipSuck,mouthOpen,smirk,eyeClosure,attention,lidTighten,jawDrop,dimpler,eyeWiden,cheekRaise,lipStretch"

    c = 0
    res_affdex = []
    res_affdex.append("#" + ',' + columns_Expression)

    log_affdex = log_affdex[:len(log_affdex) - 1]
    for eachExpression in log_affdex:
        inside = re.findall('\{(.*)\}', eachExpression)[0]
        split = re.findall('\{(.*?)\}', inside)
        eachExpression_data = []

        expTime = split[1]
        expTimestamp = expTime.split(':')[1]

        # remove records before question1 starts and after question3 ends
        if expTimestamp < stamps[0] or expTimestamp > stamps[5]:
            continue

        if expTimestamp >= stamps[0] and expTimestamp < stamps[1]:
            sessionQues_id = sessionQues[0]
        if expTimestamp >= stamps[2] and expTimestamp < stamps[3]:
            sessionQues_id = sessionQues[1]
        if expTimestamp >= stamps[4] and expTimestamp <= stamps[5]:
            sessionQues_id = sessionQues[2]

        eachExpression_data = eachExpression_data + [sessionQues_id]
        eachExpression_data = eachExpression_data + [expTimestamp]

        appearance = split[2]
        appearance_var = appearance.split(',')
        for appearanceVar in appearance_var:
            eachExpression_data = eachExpression_data + [appearanceVar.split(':')[1].strip('\"')]

        emotions = split[3]
        emotions_var = emotions.split(',')
        for emotionsVar in emotions_var:
            eachExpression_data = eachExpression_data + [emotionsVar.split(':')[1]]

        expressions = split[4]
        expressions_var = expressions.split(',')
        for expressionsVar in expressions_var:
            eachExpression_data = eachExpression_data + [expressionsVar.split(':')[1]]

        if print_debug: print(eachExpression_data)
        if print_debug: print("Expression running well!!")

        # write TABLE Expression
        values_Expression = ""
        for k in range(len(eachExpression_data)):
            eachExpression_data[k] = str(eachExpression_data[k])
            if (k == 0):
                values_Expression = eachExpression_data[k]
            elif (k >= 2 and k <= 5):
                values_Expression = values_Expression + ",\"" + eachExpression_data[k] + "\""
            else:
                values_Expression = values_Expression + "," + eachExpression_data[k]

        # For the results
        c += 1
        res_affdex.append(str(c) + ',' + values_Expression)

        if use_database:
            try:
                sql_Expression = "INSERT INTO Expression(" + columns_Expression + ") VALUES (" + values_Expression + ")"
                if print_debug: print("*********")
                if print_debug: print(sql_Expression)
                cursor.execute(sql_Expression)
            except:
                db.rollback()
                if print_debug: print("expression..................")

    # =========== Write Table Expression ok =============

    # =========== Write Table Gaze =============
    columns_Gaze = "sessionQuesID,gazeTimestamp,x,y,confidence"

    log_xlabs = log_xlabs[:len(log_xlabs)-1]
    for eachGaze in log_xlabs:
        eachGaze_data = eachGaze.split(',')
        gazeTimestamp = eachGaze_data[0]
        if gazeTimestamp<stamps[0] or gazeTimestamp>stamps[5]:
            continue
        if gazeTimestamp>=stamps[0] and gazeTimestamp<stamps[1]:
            sessionQues_id = sessionQues[0]
        if gazeTimestamp>=stamps[2] and gazeTimestamp<stamps[3]:
            sessionQues_id = sessionQues[1]
        if gazeTimestamp>=stamps[4] and gazeTimestamp<=stamps[5]:
            sessionQues_id = sessionQues[2]
        eachGaze_data.insert(0,sessionQues_id)

        if print_debug: print(eachGaze_data)
        if print_debug: print("Gaze running well!!")

        # write TABLE Gaze
        values_Gaze = ""
        for j in range(len(eachGaze_data)):
            eachGaze_data[j] = str(eachGaze_data[j])
            if (j==0 ):
                values_Gaze = eachGaze_data[j]
            elif (j==1 | j==2):
                values_Gaze = values_Gaze+","+eachGaze_data[j]
            else:
                values_Gaze = values_Gaze+",\""+eachGaze_data[j]+"\""

        if use_database:
            try:
                sql_Gaze = "INSERT INTO Gaze(" + columns_Gaze + ") VALUES ("+ values_Gaze +")"
                cursor.execute(sql_Gaze)
            except:
                db.rollback()
                if print_debug: print("gaze..................")
    # =========== Write Table Gaze ok =============

    if use_database:
        try:
            db.commit()
        except:
            db.rollback()
            if print_debug: print("So sad..................")

    return use_database, res_affdex


# Store the prediction
def db_store_prediction(session_id,prediction):
    #print("The prediction for session_id " + session_id + " is: " + prediction)
    if use_database:
        for seq in range(3):
            if prediction == seq + 1:
                prediction_bin = "1"
            else:
                prediction_bin = "0"
            try:
                sql_prediction = "update Session_question set pLabel="+prediction_bin+" where sessionQuesID="+sessionQues[seq]
                if print_debug: print(sql_prediction)
                cursor.execute(sql_prediction)
                db.commit()
            except:
                db.rollback()
                if print_debug: print("session_predict.........")
    return use_database


# Store the truth
def db_store_truth(session_id,correct_res):
    #print("The truth for session_id " + session_id + " is: " + correct_res)
    if use_database:
        for seq in range(3):
            if correct_res == str(seq + 1):
                correct_res_bin = "1"
            else:
                correct_res_bin = "0"
            try:
                sql_correct_res = "update Session_question set tLabel="+correct_res_bin+" where sessionQuesID="+sessionQues[seq]
                if print_debug: print(sql_correct_res)
                cursor.execute(sql_correct_res)
                db.commit()
            except:
                db.rollback()
                if print_debug: print("session_label.........")
    return use_database
