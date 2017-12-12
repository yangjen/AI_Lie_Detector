import pymysql
import re
import time
import os


# Import local results in txt files into database
path = "./txt_log_data"
def import_results(path):

    db = pymysql.connect("localhost", "root", "weisi9527sj", "P5BA")
    cursor = db.cursor()

    try:

        # get session_id
        sql_getSessionID = "select * from Session order by sessionID desc limit 1"
        cursor.execute(sql_getSessionID)
        results = cursor.fetchall()[0]
        session_id = results[0]
        # get sessionQues_id
        sql_getSessionQuesID = "select * from Session_question order by sessionQuesID desc limit 1"
        cursor.execute(sql_getSessionQuesID)
        results = cursor.fetchall()[0]
        sessionQues_id_last = results[0]

        files = os.listdir(path)
        sessions_count = int(len(files)/4)
        files.sort()
        order = [2,1,0,3]
        
        for iter in range(sessions_count):
            session_id = str(int(session_id)+1)
            sessionQues = [str(int(sessionQues_id_last)+1+iter*3),str(int(sessionQues_id_last)+2+iter*3),str(int(sessionQues_id_last)+3+iter*3)]
            '''
            try:
                sql_sess = "INSERT INTO Session(sessionID) VALUES ("+session_id+")"
                cursor.execute(sql_sess)
                #db.commit()
            except:
                    db.rollback()
                    print("session..................")
            '''
            
            # process log_questions txt file
            f_questions = open(path+"/"+files[order[0]+iter*4])
            sequence = 0
            i = -1
            while 1:
                i = i+1
                line = f_questions.readline()
                if not line:
                    break
                question_id = line[0:2]
                sessionQues_id = sessionQues[i]
                label = line[-2]
                sequence = str(int(sequence)+1)
                #print(sessionQues_id,session_id,question_id,sequence,label)
                #print("Questions running well!!")
            
                # write TABLE Session_question                
                # values_sessQues = "sessionQues_id"+","+"session_id"+","+"question_id"+","+"sequence"+","+"label"
                try:
                    sql_sessQues = "insert into Session_question(sessionQuesID,sessionID,questionID,sequence,plabel,tlabel) values ("+sessionQues_id+","+session_id+","+question_id+","+sequence+","+label+","+label+")"
                    cursor.execute(sql_sessQues)
                    #db.commit()
                except:
                    db.rollback()
                    print("session_question..................")
                
            

            # process log_events txt file
            f_events = open(path+"/"+files[order[1]+iter*4])
            stamps = []
            n = -1
            stamps_index = [1,2,3,4,5,6]
            session_flag = 0

            while 1:
                line = f_events.readline()
                n = n+1
                if line=="\n":
                    break
                if not line:
                    break
                eventTimestamp = line.split(',')[0].split(':')[1]
                if n in stamps_index:
                    stamps = stamps + [eventTimestamp]
                event = line.split(',')[1].strip('}\n').split(':')[1]
                #print(eventTimestamp,event)
                #print("Events running well!!")
            
                # write TABLE LogEvent
                try:
                    # insert event
                    sql_logEvent = "INSERT INTO LogEvent(sessionID,eventTimestamp,logEvent) VALUES ("+session_id+","+eventTimestamp+","+event+")"
                    cursor.execute(sql_logEvent)
                        #db.commit()

                    # insert session
                    if(session_flag==0):
                        sql_sess = "INSERT INTO Session(sessionID, sessionTimestamp) VALUES ("+session_id+","+eventTimestamp+")"
                        cursor.execute(sql_sess)
                        session_flag=1

                except:
                    db.rollback()
                    print("event/session..................")


            # process log_affdex txt file
            f_affdex = open(path+"/"+files[order[2]+iter*4])
            m=-1
            while 1:
                line = f_affdex.readline()
                m = m+1
                if line=="\n":
                    break
                if not line:
                    break
                line = line.strip('\n')
                inside = re.findall('\{(.*)\}',line)[0]
                split = re.findall('\{(.*?)\}',inside)
                        
                eachExpression_data = []
                        
                expTime = split[1]
                expTimestamp = expTime.split(':')[1]
                if expTimestamp<stamps[0] or expTimestamp>stamps[5]:
                    continue
                #print("data is in line"+str(m))
                eachExpression_data = eachExpression_data + [expTimestamp]
                if expTimestamp>=stamps[0] and expTimestamp<stamps[1]:
                    sessionQues_id = sessionQues[0]
                if expTimestamp>=stamps[2] and expTimestamp<stamps[3]:
                    sessionQues_id = sessionQues[1]
                if expTimestamp>=stamps[4] and expTimestamp<=stamps[5]:
                    sessionQues_id = sessionQues[2]
                eachExpression_data = eachExpression_data + [sessionQues_id]
                
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
                #print(eachExpression_data)
                #print("Expression running well!!")
                
                
                
                # write TABLE Expression
                values_Expression = "" #应该是sessionQuesid呀，下同
                
                for k in range(len(eachExpression_data)):
                    eachExpression_data[k] = str(eachExpression_data[k])
                    if (k==0):
                        values_Expression=eachExpression_data[k]
                    elif (k>=2 and k<=5):
                        values_Expression=values_Expression+",\""+eachExpression_data[k]+"\""
                    else:
                        values_Expression=values_Expression+","+eachExpression_data[k]
                try:
                    sql_Expression = "INSERT INTO Expression(expTimestamp,sessionQuesID,gender,glasses,age,ethnicity,joy,sadness,disgust,contempt,anger,fear,surprise,valence,engagement,smile,innerBrowRaise,browRaise,browFurrow,noseWrinkle,upperLipRaise,lipCornerDepressor,chinRaise,lipPucker,lipPress,lipSuck,mouthOpen,smirk,eyeClosure,attention,lidTighten,jawDrop,dimpler,eyeWiden,cheekRaise,lipStretch) VALUES ("+ values_Expression +")"
                    #print("*********")
                    #print(sql_Expression)
                    cursor.execute(sql_Expression)
                except:
                    db.rollback()
                    print("expression..................")
                
            
            # process log_xlabs txt file
            f_xlabs = open(path+"/"+files[order[3]+iter*4])
            while 1:
                line = f_xlabs.readline()
                if line=="\n":
                    break
                if not line:
                    break
                line = line.strip('\n')
                eachGaze_data = line.split(',')
                
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
                #print(eachGaze_data)
                #print("Gaze running well!!")
                
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

    db.close()
    return

import_results(path)
