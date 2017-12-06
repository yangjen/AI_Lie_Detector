import random

# Prepare the questions to send to index.html
def db_get_input_csv():
    session_id = 22

    with open("static/questions.txt", "r") as myfile:
        data=myfile.read().splitlines()
        sample_questions = random.sample(data, 3)

    return session_id,sample_questions

def db_get_input():
    session_id = 22
    sample_questions = ["q1","q2","q3"]
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