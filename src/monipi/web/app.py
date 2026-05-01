

from csv import DictReader
from json import JSONDecodeError, load

from flask import Flask, render_template

from monipi.process.data_manager import DataManager

app = Flask(__name__)
dm = DataManager()


def read_json_file(path):
    if not path.exists():
        return None

    try:
        with open(path, "r") as file:
            return load(file)
    except JSONDecodeError:
        return None


def read_csv_rows(path, limit=10):
    if not path.exists():
        return []

    with open(path, "r", newline="") as file:
        rows = list(DictReader(file))

    return rows[-limit:]


@app.route("/")
def status():
    session_path = dm.data_dir / "current_session_details.json"
    averages_path = dm.csvpath_sample_averages_scd30

    session = read_json_file(session_path)
    latest_averages = read_csv_rows(averages_path, limit=1)
    latest_average = latest_averages[0] if latest_averages else None

    return render_template(
        "status.html",
        session=session,
        latest_average=latest_average,
    )


@app.route("/data")
def data():
    scd30_rows = read_csv_rows(dm.csvpath_sample_averages_scd30, limit=10)
    pms5003_rows = read_csv_rows(dm.csvpath_sample_averages_pms5003, limit=10)

    return render_template(
        "data.html",
        scd30_rows=scd30_rows,
        pms5003_rows=pms5003_rows,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)