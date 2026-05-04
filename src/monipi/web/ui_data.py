from datetime import datetime, timedelta, timezone
from monipi.process.data_manager import DataManager
from monipi.process.air_quality import get_gauge_config
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


def _as_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


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

    # row[0] is already local time → do NOT convert
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

    # row[0] is already local time → do NOT convert
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


def _build_dashboard_readings(latest_scd30, latest_pms5003):
    co2_value = _as_float(latest_scd30.get("co2")) if latest_scd30 else None
    temp_value = _as_float(latest_scd30.get("temp")) if latest_scd30 else None
    humidity_value = _as_float(latest_scd30.get("hum")) if latest_scd30 else None

    pm1_value = _as_float(latest_pms5003.get("pm1")) if latest_pms5003 else None
    pm25_value = _as_float(latest_pms5003.get("pm25")) if latest_pms5003 else None
    pm10_value = _as_float(latest_pms5003.get("pm10")) if latest_pms5003 else None

    return {
        "co2": get_gauge_config("co2", co2_value),
        "temperature": get_gauge_config("temperature", temp_value),
        "humidity": get_gauge_config("humidity", humidity_value),
        "pm1": get_gauge_config("pm1", pm1_value),
        "pm25": get_gauge_config("pm25", pm25_value),
        "pm10": get_gauge_config("pm10", pm10_value),
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
    dashboard_readings = _build_dashboard_readings(latest_scd30, latest_pms5003)

    return {
        "session": session,
        "latest_scd30": latest_scd30,
        "latest_pms5003": latest_pms5003,
        "latest_scd30_list": latest_scd30_list,
        "latest_pms5003_list": latest_pms5003_list,
        "dashboard_readings": dashboard_readings,
        "co2_ppm": dashboard_readings["co2"]["value"],
        "temperature_c": dashboard_readings["temperature"]["value"],
        "humidity_percent": dashboard_readings["humidity"]["value"],
        "pm1_0": dashboard_readings["pm1"]["value"],
        "pm2_5": dashboard_readings["pm25"]["value"],
        "pm10": dashboard_readings["pm10"]["value"],
    }


def get_recent_data(timeframe_hours=1, page=1, page_size=10):
    timeframe_mins = timeframe_hours * 60
    limit = int(timeframe_mins / reporting_period_in_mins) + 10
    current_time = datetime.now(timezone.utc)
    target_start = current_time - timedelta(minutes=timeframe_mins)

    scd30_rows = storage.read_last_n_rows(dm.csvpath_sample_averages_scd30, limit)
    pms5003_rows = storage.read_last_n_rows(dm.csvpath_sample_averages_pms5003, limit)
    
    filtered_scd30_rows = []
    for row in scd30_rows:
        # SCD30: UTC is at index 4
        if len(row) > 4:
            row_time = datetime.strptime(_clean_time(row[4]), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        else:
            continue
        # if row since target start add to list, else discard
        if row_time >= target_start:
            filtered_scd30_rows.append(row)

    filtered_pms5003_rows = []
    for row in pms5003_rows:
        # PMS5003: UTC is at index 6
        if len(row) > 6:
            row_time = datetime.strptime(_clean_time(row[6]), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        else:
            continue
        # if row since target start add to list, else discard
        if row_time >= target_start:
            filtered_pms5003_rows.append(row)

    scd30_average_rows_full = [_format_scd30_average_row(r) for r in filtered_scd30_rows if r]
    pms5003_average_rows_full = [_format_pms5003_average_row(r) for r in filtered_pms5003_rows if r]

    # chart data stays chronological: oldest → newest
    scd30_chart_rows = scd30_average_rows_full[:]
    pms5003_chart_rows = pms5003_average_rows_full[:]


    # pagination for table only
    start = (page - 1) * page_size
    end = start + page_size

    scd30_average_rows = scd30_average_rows_full[start:end]
    pms5003_average_rows = pms5003_average_rows_full[start:end]


    return {
        "scd30_average_rows": scd30_average_rows,
        "pms5003_average_rows": pms5003_average_rows,
        "scd30_chart_rows": scd30_chart_rows,
        "pms5003_chart_rows": pms5003_chart_rows,
    }


# New function: get_reading_detail_data
def get_reading_detail_data(reading_key, timeframe_hours=1, page=1):
    supported_readings = {
        "co2": {
            "title": "CO₂",
            "unit": "ppm",
            "source": "SCD30",
            "row_key": "co2",
            "table_heading": "CO₂ ppm",
            "chart_rows_key": "scd30_chart_rows",
            "table_rows_key": "scd30_average_rows",
        },
        "temperature": {
            "title": "Temperature",
            "unit": "°C",
            "source": "SCD30",
            "row_key": "temp",
            "table_heading": "Temp °C",
            "chart_rows_key": "scd30_chart_rows",
            "table_rows_key": "scd30_average_rows",
        },
    }

    if reading_key not in supported_readings:
        reading_key = "co2"

    reading = supported_readings[reading_key]
    recent_data = get_recent_data(timeframe_hours=timeframe_hours, page=page)

    chart_rows = recent_data[reading["chart_rows_key"]]
    table_rows_source = recent_data[reading["table_rows_key"]]
    row_key = reading["row_key"]

    chart_labels = [row["time"] for row in chart_rows]
    chart_values = [row[row_key] for row in chart_rows]

    table_rows = [
        {
            "time": row["time"],
            "value": row[row_key],
            "utc_time": row["utc_time"],
        }
        for row in table_rows_source
    ]

    return {
        "reading_key": reading_key,
        "title": reading["title"],
        "unit": reading["unit"],
        "source": reading["source"],
        "table_heading": reading["table_heading"],
        "chart_labels": chart_labels,
        "chart_values": chart_values,
        "table_rows": table_rows,
        "timeframe_hours": timeframe_hours,
        "page": page,
    }