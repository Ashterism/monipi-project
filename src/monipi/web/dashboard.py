import csv
from datetime import datetime, timedelta, timezone
from monipi.process.data_manager import DataManager
from ..config import reporting_period_in_mins

dm = DataManager()
storage = dm.storage


def _clean_time(value):
    # drops of timezone (i.e. +04:00)
    return value.split("+")[0]


def _utc_to_local_parts(utc_string):
    try:
        dt_utc = datetime.strptime(_clean_time(utc_string), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        dt_local = dt_utc.astimezone()
        return dt_local.strftime("%Y-%m-%d"), dt_local.strftime("%H:%M:%S"), dt_local.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        clean = _clean_time(utc_string)
        if " " in clean:
            d, t = clean.split(" ")
            return d, t, clean
        return clean, "", clean


def _format_number(value, decimal_places=2):
    try:
        return f"{float(value):.{decimal_places}f}"
    except (TypeError, ValueError):
        return value


def _format_scd30_row(row):
    if not row or len(row) < 4:
        return None

    date_part, time_part, clean_time = _utc_to_local_parts(row[0])

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

    date_part, time_part, clean_time = _utc_to_local_parts(row[0])

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

    date_part, time_part, clean_time = _utc_to_local_parts(row[0])

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

    date_part, time_part, clean_time = _utc_to_local_parts(row[0])

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

    # convert session timestamps (UTC) to local for display
    if session:
        for key in ["start", "expected end time"]:
            if key in session and session[key]:
                try:
                    _, _, local_ts = _utc_to_local_parts(session[key])
                    session[key] = local_ts
                except Exception:
                    pass

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


def get_recent_data(timeframe_hours=1):
    timeframe_mins = timeframe_hours * 60
    limit = int(timeframe_mins / reporting_period_in_mins) + 10
    current_time = datetime.now(timezone.utc)
    target_start = current_time - timedelta(minutes=timeframe_mins)

    scd30_rows = storage.read_last_n_rows(dm.csvpath_sample_averages_scd30, limit)
    pms5003_rows = storage.read_last_n_rows(dm.csvpath_sample_averages_pms5003, limit)
    
    filtered_scd30_rows = []
    for row in scd30_rows:
        # get time from row, strip tz, convert to datetime object
        row_time = datetime.strptime(_clean_time(row[0]), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        # if row since target start add to list, else discard
        if row_time >= target_start:
            filtered_scd30_rows.append(row)
    
    filtered_pms5003_rows = []
    for row in pms5003_rows:
        # get time from row, strip tz, convert to datetime object
        row_time = datetime.strptime(_clean_time(row[0]), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        # if row since target start add to list, else discard
        if row_time >= target_start:
            filtered_pms5003_rows.append(row)

    scd30_average_rows = [_format_scd30_average_row(r) for r in filtered_scd30_rows if r]
    pms5003_average_rows = [_format_pms5003_average_row(r) for r in filtered_pms5003_rows if r]
    


    return {
        "scd30_average_rows": scd30_average_rows,
        "pms5003_average_rows": pms5003_average_rows,
    }