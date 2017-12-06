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

def db_get_input():
    sample_questions=[]
    session_id="0"
    db = pymysql.connect("localhost", "root", "weisi9527sj", "P4BA")
    cursor = db.cursor()
    
    try:
        sql = "select * from Session order by sessionID desc limit 1"
        cursor.execute(sql)
        results = cursor.fetchall()[0]
        session_id = str(results[0]+1)
        
        sql_n = "INSERT INTO Session(sessionID) VALUES ("+session_id+")"
        cursor.execute(sql_n)
        
        
        sql_question = "select * from Question"
        cursor.execute(sql_question)
        questions_table = cursor.fetchall()
        questions_no = len(questions_table)
        questions_id = random.sample(range(questions_no),3)
        print(questions_id)
        
        for q_id in questions_id:
            question = questions_table[q_id][1]
            sample_questions = sample_questions + [question]
            q_id_real =str(q_id+1)
            
            sql_sq =  "INSERT INTO Session_question(sessionID,questionID) VALUES ("+session_id+","+q_id_real+")"
            cursor.execute(sql_sq)
            db.commit()

    except:
        # 如果发生错误则回滚
        db.rollback()
        print("sad.......")
        db.close()
    return session_id,sample_questions

# Process the results from index.html
def db_store_results(session_id,log_affdex,log_xlabs,log_events):
    #print("I received data from the session_id=",session_id)
    return

# Store the prediction
def db_store_prediction(session_id,prediction):
    #print("The prediction for session_id " + session_id + " is: " + prediction)
    return

# Store the truth
def db_store_truth(session_id,correct_res):
    #print("The correct answer for session_id " + session_id + " was: " + correct_res)
    return
