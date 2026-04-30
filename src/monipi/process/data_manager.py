import csv
from pathlib import Path
from datetime import datetime, timedelta

""" 
    this is a utility class to manage the data 
    read / write operations to csv
"""


class DataManager:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[3]
        self.data_dir = self.project_root / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.csvpath_samples_scd30 = self.data_dir / "current_samples_scd30.csv"
        self.csvpath_sample_averages_scd30 = self.data_dir / "current_sample_averages_scd30.csv"
        
        self.csvpath_samples_pms5003 = self.data_dir / "current_samples_pms5003.csv"
        self.csvpath_sample_averages_pms5003 = self.data_dir / "current_sample_averages_pms5003.csv"

        self.dailies_dir = self.data_dir / "dailies"

    #==== SCD30 ====#

    def write_readings_scd30(self, t_utc, c, t, h):
        with open(self.csvpath_samples_scd30, "a", newline="") as samples_csv:
            writer = csv.writer(samples_csv)  # loads csv into writer
            writer.writerow([t_utc, c, t, h])

    def write_averages_scd30(self, t_lcl, c, t, h, t_utc):
        with open(self.csvpath_sample_averages_scd30, "a", newline="") as averages_csv:
            writer = csv.writer(averages_csv)  # loads csv into writer
            writer.writerow([t_lcl, c, t, h, t_utc])


    #==== PMS5003 ====#

    def write_readings_pms5003(self, t_utc, pm1, pm25, pm10, pc03, pc25):
        with open(self.csvpath_samples_pms5003, "a", newline="") as samples_csv:
            writer = csv.writer(samples_csv)  # loads csv into writer
            writer.writerow([t_utc, pm1, pm25, pm10, pc03, pc25])

    def write_averages_pms5003(self, t_lcl, pm1, pm25, pm10, pc03, pc25, t_utc):
        with open(self.csvpath_sample_averages_pms5003, "a", newline="") as averages_csv:
            writer = csv.writer(averages_csv)  # loads csv into writer
            writer.writerow([t_lcl, pm1, pm25, pm10, pc03, pc25, t_utc])

    #==== Backup management ====#
 
    def backup_dailies(self):
        date_for_file = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        self.dailies_dir.mkdir(parents=True, exist_ok=True)

        # ---- SCD30 ----
        scd_src = self.data_dir / "current_session_details_scd30.json"
        scd_dst = self.dailies_dir / f"{date_for_file}_scd30.json"

        if scd_src.exists():
            if not scd_dst.exists():
                scd_src.rename(scd_dst)
            else:
                print("SCD30 daily already exists, skipping.")
        else:
            print("No SCD30 session file to back up.")

        # ---- PMS5003 ----
        pms_src = self.data_dir / "current_session_details_pms5003.json"
        pms_dst = self.dailies_dir / f"{date_for_file}_pms5003.json"

        if pms_src.exists():
            if not pms_dst.exists():
                pms_src.rename(pms_dst)
            else:
                print("PMS5003 daily already exists, skipping.")
        else:
            print("No PMS5003 session file to back up.")