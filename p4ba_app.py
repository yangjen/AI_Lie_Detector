import random
from flask import Flask, request, jsonify, render_template, make_response

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1


# Prepare the questions to send to index.html
def get_questions():
    with open("static/questions.txt", "r") as myfile:
        data=myfile.read().splitlines()
        sample_questions = random.sample(data, 3)
    return sample_questions

# Process the results from index.html
def process_logs(log_affdex,log_xlabs,log_events):
    return


@app.route("/", methods=["GET"])
def html_index():
    return render_template('index.html', questions=get_questions())


@app.route("/index_post", methods = ["POST"])
def get_logs():
    log_affdex = []
    log_xlabs = []
    log_events = []

    if "log_affdex" in request.form: log_affdex = request.form.get("log_affdex", None)
    if "log_xlabs" in request.form: log_xlabs = request.form.get("log_xlabs", None)
    if "log_events" in request.form: log_events = request.form.get("log_events", None)

    process_logs(log_affdex,log_xlabs,log_events)

    return make_response(jsonify("do nothing for now")), 204


if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')

