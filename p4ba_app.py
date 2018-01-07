from flask import Flask, request, jsonify, render_template, make_response, session
from random import randint
import sys
import os

import db_func
import local_func
import lie_detector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'WeXiLeDiJo'
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1


@app.route("/test", methods=["GET"])
def html_test():
    #return render_template('test.html')
    session['session_id'], session['questions'] = db_func.db_get_input()
    prediction = randint(1,3)
    return render_template('results.html', questions=session['questions'], prediction=prediction, testing=True)


@app.route("/", methods=["GET"])
def html_index():
    session['session_id'],session['questions'] = db_func.db_get_input()
    return render_template('index.html', questions=session['questions'])


@app.route("/results", methods = ["POST"])
def html_index_post():
    # Send logs
    log_affdex = []
    log_xlabs = []
    log_events = []

    if "log_affdex" in request.form: log_affdex = request.form.get("log_affdex", None)
    if "log_xlabs" in request.form: log_xlabs = request.form.get("log_xlabs", None)
    if "log_events" in request.form: log_events = request.form.get("log_events", None)

    log_affdex = log_affdex.split('\r\n')
    log_xlabs = log_xlabs.split('\r\n')
    log_events = log_events.split('\r\n')

    # Store results into the DB
    # If didn't connect to DB, then save the files locally to manually add them afterwards
    use_database, res_affdex = db_func.db_store_results(session['session_id'],log_affdex,log_xlabs,log_events)
    if not use_database: local_func.local_save(session['session_id'],log_affdex,log_xlabs,log_events,session['questions'])

    # Get the predicted value from the model
    prediction = randint(1, 3)
    try:
        prediction = lie_detector.predict_lie(res_affdex)
    except:
        print("lie_detector.predict_lie()...")

    # Store the prediction
    db_func.db_store_prediction(session['session_id'],prediction)

    # Show the results page
    #return make_response(jsonify("do nothing for now")), 204
    return render_template('results.html', questions=session['questions'], prediction=prediction, testing=False)


@app.route("/results_post", methods = ["POST"])
def html_results():
    # Get ground truth from the user
    ground_truth = request.form.get("log_res", None)

    # Store ground truth in the db
    use_database = db_func.db_store_truth(session['session_id'],ground_truth)
    if not use_database: local_func.local_save_truth(session['session_id'],ground_truth)

    # Do nothing else
    return make_response(jsonify("do nothing for now")), 204


if __name__ == "__main__":
    try:
        # Because of how different versions of python work on different systems, is not possible to
        # use pickle to save the trained model in one system and load it in another system.
        # Because of this, for now we are not saving into github the pickle model.
        # Therefore, if you just downloaded our code you will need to train the model.
        # And since we have a small amount of training data, the training of the model should be fast.
        # After that, there will be no need to train it again in this same system.
        if not os.path.isfile(os.path.join("model", "model.pickle")):
            lie_detector.training()
    except:
        print("lie_detector.training()...")

    # To use SSL (https):
    #   1. pip3 install pyopenssl
    #   2. run this file with "ssl" as argument:
    #      python3 p4ba_app.py ssl
    try:
        if (sys.argv[1].lower() != "ssl"): raise Exception("I don't want to use SSL")
        import OpenSSL
        app.run(port=5000, host='0.0.0.0', ssl_context='adhoc')
    except:
        app.run(port=5000, host='0.0.0.0')
