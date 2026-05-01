from monipi.process.data_manager import DataManager


dm = DataManager()
storage = dm.storage


def get_status_data():
    session_path = storage.data_dir / "current_session_details.json"
    averages_path = dm.csvpath_sample_averages_scd30

    session = storage.read_json(session_path)
    latest_averages = storage.read_csv_rows(averages_path, limit=1)
    latest_average = latest_averages[0] if latest_averages else None

    return {
        "session": session,
        "latest_average": latest_average,
    }


def get_recent_data(limit=10):
    scd30_rows = storage.read_csv_rows(
        dm.csvpath_sample_averages_scd30,
        limit=limit,
    )
    pms5003_rows = storage.read_csv_rows(
        dm.csvpath_sample_averages_pms5003,
        limit=limit,
    )

    return {
        "scd30_rows": scd30_rows,
        "pms5003_rows": pms5003_rows,
    }
