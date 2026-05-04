from flask import Flask, render_template, request

from monipi.web.ui_data import get_status_data, get_recent_data, get_reading_detail_data

app = Flask(__name__)


@app.route("/")
def status():
    return render_template("status.html", **get_status_data())


# Dashboard route
@app.route("/dashboard")
def dashboard():
    dashboard_context = get_status_data()
    recent_context = get_recent_data(timeframe_hours=1, page=1)
    dashboard_context.update(recent_context)
    return render_template("dashboard.html", **dashboard_context)


# Reading detail route
@app.route("/dashboard/<reading_key>")
def reading_detail(reading_key):
    timeframe = request.args.get("timeframe", default=1, type=int)
    page = request.args.get("page", default=1, type=int)
    detail_context = get_reading_detail_data(
        reading_key,
        timeframe_hours=timeframe,
        page=page,
    )
    return render_template("reading_detail.html", **detail_context)


@app.route("/data")
def data():
    timeframe = request.args.get("timeframe", default=1, type=int)
    page = request.args.get("page", default=1, type=int)
    data_context = get_recent_data(timeframe_hours=timeframe, page=page)
    data_context["timeframe_hours"] = timeframe
    data_context["page"] = page
    return render_template("data.html", **data_context)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)