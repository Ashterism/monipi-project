from flask import Flask, render_template

from monipi.web.dashboard import get_status_data, get_recent_data

app = Flask(__name__)


@app.route("/")
def status():
    return render_template("status.html", **get_status_data())


@app.route("/data")
def data():
    return render_template("data.html", **get_recent_data(limit=10))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)