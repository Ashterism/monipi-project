import csv
from monipi.process.data_manager import DataManager


dm = DataManager()
storage = dm.storage


def _clean_time(value):
    return value.split("+")[0]


def _format_number(value, decimal_places=2):
    try:
        return f"{float(value):.{decimal_places}f}"
    except (TypeError, ValueError):
        return value


def _format_scd30_row(row):
    if not row or len(row) < 4:
        return None

    clean_time = _clean_time(row[0])
    date_part, time_part = clean_time.split(" ")

    return {
        "date": date_part,
        "time": time_part,
        "timestamp": clean_time,
        "co2": _format_number(row[1]),
        "temp": _format_number(row[2]),
        "hum": _format_number(row[3]),
    }


def _format_pms5003_row(row):
    if not row or len(row) < 6:
        return None

    clean_time = _clean_time(row[0])
    date_part, time_part = clean_time.split(" ")

    return {
        "date": date_part,
        "time": time_part,
        "timestamp": clean_time,
        "pm1": _format_number(row[1]),
        "pm25": _format_number(row[2]),
        "pm10": _format_number(row[3]),
        "pc03": _format_number(row[4], decimal_places=0),
        "pc25": _format_number(row[5], decimal_places=0),
    }


def _format_scd30_average_row(row):
    if not row or len(row) < 5:
        return None

    clean_time = _clean_time(row[0])
    date_part, time_part = clean_time.split(" ")

    return {
        "date": date_part,
        "time": time_part,
        "timestamp": clean_time,
        "co2": _format_number(row[1]),
        "temp": _format_number(row[2]),
        "hum": _format_number(row[3]),
        "utc_time": _clean_time(row[4]),
    }


def _format_pms5003_average_row(row):
    if not row or len(row) < 7:
        return None

    clean_time = _clean_time(row[0])
    date_part, time_part = clean_time.split(" ")

    return {
        "date": date_part,
        "time": time_part,
        "timestamp": clean_time,
        "pm1": _format_number(row[1]),
        "pm25": _format_number(row[2]),
        "pm10": _format_number(row[3]),
        "pc03": _format_number(row[4], decimal_places=0),
        "pc25": _format_number(row[5], decimal_places=0),
        "utc_time": _clean_time(row[6]),
    }


def get_status_data():
    session_path = storage.data_dir / "current_session_details.json"

    session = storage.read_json(session_path)

    scd30_rows = storage.read_last_n_rows(dm.csvpath_samples_scd30, 5)
    pms_rows = storage.read_last_n_rows(dm.csvpath_samples_pms5003, 5)

    latest_scd30_list = [_format_scd30_row(r) for r in scd30_rows if r]
    latest_pms5003_list = [_format_pms5003_row(r) for r in pms_rows if r]

    latest_scd30 = latest_scd30_list[-1] if latest_scd30_list else None
    latest_pms5003 = latest_pms5003_list[-1] if latest_pms5003_list else None

    return {
        "session": session,
        "latest_scd30": latest_scd30,
        "latest_pms5003": latest_pms5003,
        "latest_scd30_list": latest_scd30_list,
        "latest_pms5003_list": latest_pms5003_list,
    }


def get_recent_data(limit=10):
    scd30_rows = storage.read_last_n_rows(dm.csvpath_sample_averages_scd30, limit)
    pms5003_rows = storage.read_last_n_rows(dm.csvpath_sample_averages_pms5003, limit)

    scd30_average_rows = [_format_scd30_average_row(r) for r in scd30_rows if r]
    pms5003_average_rows = [_format_pms5003_average_row(r) for r in pms5003_rows if r]

    return {
        "scd30_average_rows": scd30_average_rows,
        "pms5003_average_rows": pms5003_average_rows,
    }
