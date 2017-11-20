from flask import Flask, request, jsonify, render_template, make_response

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1


@app.route("/", methods=["GET"])
def form():
    quests = ["Q1", "Q2", "Q3"]
    return render_template('index.html', questions=quests)


if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')

