import random
import pymysql
import re
import time

# Prepare the questions to send to index.html
def db_get_input_csv():
    session_id = 22

    with open("static/questions.txt", "r") as myfile:
        data=myfile.read().splitlines()
        sample_questions = random.sample(data, 3)

    return session_id,sample_questions

db = pymysql.connect("localhost", "root", "weisi9527sj", "P5BA")
cursor = db.cursor()

questions_id=[]
sessionQues=[]

def db_get_input():
    sample_questions=[]
    session_id="0"

    try:
        sql = "select * from Session order by sessionID desc limit 1"
        cursor.execute(sql)
        results = cursor.fetchall()[0]
        session_id = str(results[0]+1)

        sessionTimestamp =str(int(time.time()*1000))
        print("p---------------------")
        sql_sess = "INSERT INTO Session(sessionID, sessionTimestamp) VALUES ("+session_id+","+sessionTimestamp+")"

        
        print(sql_sess)
        cursor.execute(sql_sess)

        global questions_id
        sql_question = "select * from Question"
        cursor.execute(sql_question)
        questions_table = cursor.fetchall()
        questions_no = len(questions_table)
        questions_id = random.sample(range(questions_no),3)
        
        
        for q_id in questions_id:
            question = questions_table[q_id][1]
            sample_questions = sample_questions + [question]
        
        for i in range(3):
            questions_id[i]=str(questions_id[i]+1)
        print(questions_id)
        
        
        db.commit()

    except:
        # if fail, roll back
        db.rollback()
        print("sad_ques")
        db.close()
    return session_id,sample_questions

# Process the results from index.html
def db_store_results(session_id,log_affdex,log_xlabs,log_events):
    try:
        sessionid = str(session_id)

        # get sessionQues_id
        sql_getSessionQuesID = "select * from Session_question order by sessionQuesID desc limit 1"
        cursor.execute(sql_getSessionQuesID)
        results = cursor.fetchall()[0]
        sessionQues_id = results[0]

        global sessionQues
        sessionQues = [str(int(sessionQues_id)+1),str(int(sessionQues_id)+2),str(int(sessionQues_id)+3)]
        print("<<<<<<<<<<<<<<<<")
        print(sessionQues)
        # =========== Write Table LogEvent ===========
        try:
            log_events = log_events[:len(log_events)-1]
            stamps = []
            for eachEvent in log_events:
                # Get values
                eventTimestamp = eachEvent.split(',')[0].split(':')[1]
                event = eachEvent.split(',')[1].split(':')[1].strip('}"')
                if event.find("question")!=-1:
                    stamps = stamps + [eventTimestamp]
                sql_logEvent = "INSERT INTO LogEvent(sessionID,eventTimestamp,logEvent) VALUES ("+session_id+","+eventTimestamp+","+"\""+event+"\")"
                print(sql_logEvent)
                print("Events running well!!")
                cursor.execute(sql_logEvent)
            db.commit()
        except:
            db.rollback()
            print("event..................")

        # =========== Write Table LogEvent ok ===========

        # =========== Write Table Expression =============
        # columns = "expTimestamp,sessionQuesID,gender,glasses,age,ethnicity,joy,sadness,disgust,contempt,anger,fear,surprise,valence,engagement,smile,innerBrowRaise,browRaise,browFurrow,noseWrinkle,upperLipRaise,lipCornerDepressor,chinRaise,lipPucker,lipPress,lipSuck,mouthOpen,smirk,eyeClosure,attention,lidTighten,jawDrop,dimpler,eyeWiden,cheekRaise,lipStretch"
        columns = "sessionQuesID,expTimestamp,gender,glasses,age,ethnicity,joy,sadness,disgust,contempt,anger,fear,surprise,valence,engagement,smile,innerBrowRaise,browRaise,browFurrow,noseWrinkle,upperLipRaise,lipCornerDepressor,chinRaise,lipPucker,lipPress,lipSuck,mouthOpen,smirk,eyeClosure,attention,lidTighten,jawDrop,dimpler,eyeWiden,cheekRaise,lipStretch"

        c = 0
        res_affdex = []
        res_affdex.append("#" + ',' + columns)

        log_affdex = log_affdex[:len(log_affdex)-1]
        for eachExpression in log_affdex:
            inside = re.findall('\{(.*)\}',eachExpression)[0]
            split = re.findall('\{(.*?)\}',inside)
            eachExpression_data = []
            
            expTime = split[1]
            expTimestamp = expTime.split(':')[1]
            # remove records before question1 starts and after question3 ends
            if expTimestamp<stamps[0] or expTimestamp>stamps[5]:
                continue
            #eachExpression_data = eachExpression_data + [expTimestamp]

            if expTimestamp>=stamps[0] and expTimestamp<stamps[1]:
                sessionQues_id = sessionQues[0]
            if expTimestamp>=stamps[2] and expTimestamp<stamps[3]:
                sessionQues_id = sessionQues[1]
            if expTimestamp>=stamps[4] and expTimestamp<=stamps[5]:
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
            print(eachExpression_data)
            print("Expression running well!!")
            
            # write TABLE Expression
            values_Expression = ""
            for k in range(len(eachExpression_data)):
                eachExpression_data[k] = str(eachExpression_data[k])
                if (k==0):
                    values_Expression=eachExpression_data[k]
                elif (k>=2 and k<=5):
                    values_Expression=values_Expression+",\""+eachExpression_data[k]+"\""
                else:
                    values_Expression=values_Expression+","+eachExpression_data[k]
            try:
                # For the results
                c += 1
                res_affdex.append(str(c) + ',' + values_Expression)


                sql_Expression = "INSERT INTO Expression(" + columns + ") VALUES ("+ values_Expression +")"
                print("*********")
                print(sql_Expression)
                cursor.execute(sql_Expression)
            except:
                db.rollback()
                print("expression..................")

        # =========== Write Table Expression ok=============

        # =========== Write Table Gaze =============
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
            print(eachGaze_data)
            print("Gaze running well!!")

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
            try:
                sql_Gaze = "INSERT INTO Gaze(sessionQuesID,gazeTimestamp,x,y,confidence) VALUES ("+ values_Gaze +")"
                cursor.execute(sql_Gaze)
            except:
                db.rollback()
                print("gaze..................")
        db.commit()

    except:
        db.rollback()
        print("So sad..................")
        #print("I received data from the session_id=",session_id)

    return res_affdex

# Store the prediction
def db_store_prediction(session_id,prediction):
    # =========== Write Table Session_question ===========
    for seq in range(3):
        if prediction == seq + 1:
            prediction_bin = "1"
        else:
            prediction_bin = "0"
        try:
            question=str(questions_id[seq])
            sequen=str(seq+1)
            
            sql_prediction = "insert into Session_question(sessionQuesID,sessionID,questionID,sequence,pLabel) values("+sessionQues[seq]+","+session_id+","+question+","+sequen+","+prediction_bin+")"
            
            print(sql_prediction)
            cursor.execute(sql_prediction)
            db.commit()
        except:
            db.rollback()
            print("session_predict.........")
    
    #print("The prediction for session_id " + session_id + " is: " + prediction)
    return

def db_store_truth(session_id,correct_res):
    # =========== Update Table Session_question ===========
    for seq in range(3):
        if correct_res == str(seq + 1):
            correct_res_bin = "1"
        else:
            correct_res_bin = "0"
        try:
            
            sql_correct_res = "update Session_question set tLabel="+correct_res_bin+" where sessionQuesID="+sessionQues[seq]
            print(correct_res)
            print(sql_correct_res)
            cursor.execute(sql_correct_res)
            db.commit()
        except:
            db.rollback()
            print("session_label.........")
    
    #print("The prediction for session_id " + session_id + " is: " + prediction)
    return
