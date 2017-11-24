import random

# Prepare the questions to send to index.html
def get_input():
    session_id = 22

    with open("static/questions.txt", "r") as myfile:
        data=myfile.read().splitlines()
        sample_questions = random.sample(data, 3)

    print(sample_questions)

    return session_id,sample_questions

# Process the results from index.html
def process_logs(session_id,log_affdex,log_xlabs,log_events):
    print("I received data from the session_id=",session_id)
    return
