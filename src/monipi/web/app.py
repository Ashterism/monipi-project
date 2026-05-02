from flask import Flask, render_template, request

from monipi.web.dashboard import get_status_data, get_recent_data

app = Flask(__name__)


@app.route("/")
def status():
    return render_template("status.html", **get_status_data())


@app.route("/data")
def data():
    timeframe = request.args.get("timeframe", default=1, type=int)
    return render_template("data.html", **get_recent_data(timeframe_hours=timeframe))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)