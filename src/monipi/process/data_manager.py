from datetime import datetime, timedelta
from .storage import Storage

""" 
    this is a utility class to manage the data 
    read / write operations to csv
"""


class DataManager:
    def __init__(self):
        self.storage = Storage()

        self.csvpath_samples_scd30 = self.storage.data_dir / "current_samples_scd30.csv"
        self.csvpath_sample_averages_scd30 = self.storage.data_dir / "current_sample_averages_scd30.csv"
        
        self.csvpath_samples_pms5003 = self.storage.data_dir / "current_samples_pms5003.csv"
        self.csvpath_sample_averages_pms5003 = self.storage.data_dir / "current_sample_averages_pms5003.csv"

    #==== SCD30 ====#

    def write_readings_scd30(self, t_utc, c, t, h):
        self.storage.append_csv_row(self.csvpath_samples_scd30, [t_utc, c, t, h])

    def write_averages_scd30(self, t_lcl, c, t, h, t_utc):
        self.storage.append_csv_row(self.csvpath_sample_averages_scd30, [t_lcl, c, t, h, t_utc])

    #==== PMS5003 ====#

    def write_readings_pms5003(self, t_utc, pm1, pm25, pm10, pc03, pc25):
        self.storage.append_csv_row(self.csvpath_samples_pms5003, [t_utc, pm1, pm25, pm10, pc03, pc25])

    def write_averages_pms5003(self, t_lcl, pm1, pm25, pm10, pc03, pc25, t_utc):
        self.storage.append_csv_row(self.csvpath_sample_averages_pms5003, [t_lcl, pm1, pm25, pm10, pc03, pc25, t_utc])

    #==== Backup management ====#
 
    def backup_dailies(self):
        date_for_file = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        # ---- SCD30 ----
        scd_src = self.storage.data_dir / "current_session_details_scd30.json"
        scd_dst = self.storage.dailies_dir / f"{date_for_file}_scd30.json"

        if scd_src.exists():
            if not scd_dst.exists():
                scd_src.rename(scd_dst)
            else:
                print("SCD30 daily already exists, skipping.")
        else:
            print("No SCD30 session file to back up.")

        # ---- PMS5003 ----
        pms_src = self.storage.data_dir / "current_session_details_pms5003.json"
        pms_dst = self.storage.dailies_dir / f"{date_for_file}_pms5003.json"

        if pms_src.exists():
            if not pms_dst.exists():
                pms_src.rename(pms_dst)
            else:
                print("PMS5003 daily already exists, skipping.")
        else:
            print("No PMS5003 session file to back up.")