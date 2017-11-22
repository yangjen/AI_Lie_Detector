# Prepare the questions to send to index.html
def get_input():
    session_id = 1

    with open("static/questions.txt", "r") as myfile:
        data=myfile.read().splitlines()
        sample_questions = random.sample(data, 3)

    return session_id,sample_questions

# Process the results from index.html
def process_logs(session_id,log_affdex,log_xlabs,log_events):
    return
