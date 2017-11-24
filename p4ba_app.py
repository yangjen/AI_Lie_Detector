from flask import Flask, request, jsonify, render_template, make_response, session

import db_func
import local_func

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.config['SECRET_KEY'] = 'WeXiLeDiJo'


@app.route("/", methods=["GET"])
def html_index():
    session['session_id'],session['questions'] = db_func.get_input()
    return render_template('index.html', questions=session['questions'])


@app.route("/index_post", methods = ["POST"])
def get_logs():
    log_affdex = []
    log_xlabs = []
    log_events = []

    if "log_affdex" in request.form: log_affdex = request.form.get("log_affdex", None)
    if "log_xlabs" in request.form: log_xlabs = request.form.get("log_xlabs", None)
    if "log_events" in request.form: log_events = request.form.get("log_events", None)

    log_affdex = log_affdex.split('\r\n')
    log_xlabs = log_xlabs.split('\r\n')
    log_events = log_events.split('\r\n')

    db_func.process_logs(session['session_id'],log_affdex,log_xlabs,log_events)

    local_func.local_save(session['questions'],log_affdex,log_xlabs,log_events)

    return make_response(jsonify("do nothing for now")), 204


if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')

