import csv, os
from pathlib import Path
path = Path(__file__).resolve().parent

""" 
    this is a utility class to manage the data 
    read / write operations to csv
"""

class Dataman:
    def __init__(self):
        self.csvpath_samples = str(path / "data/current_samples.csv")
        self.csvpath_sample_averages = str(path / "data/current_sample_averages.csv")
        # if header row missing then add?

    def read_row(self, tbc=''):
        # this is a placeholder method for now
        with open(self.csvpath, "r") as currentdb:
            reader = csv.reader(currentdb)   # loads csv into reader
            
            if tbc == '':
                for row in reader:
                    print(row)
            else:
                return
                
    # read_last_entry
    # read_total entries
    # read_high_low (and datetime)
    
    def write_readings(self, t_utc, c,t,h):
        with open(self.csvpath_samples, "a", newline='') as samples_csv:
            writer = csv.writer(samples_csv)   # loads csv into writer
            writer.writerow([t_utc, c,t,h])

    def write_averages(self, t_lcl, c,t,h, t_utc):
        with open(self.csvpath_sample_averages, "a", newline='') as averages_csv:
            writer = csv.writer(averages_csv)   # loads csv into writer
            writer.writerow([t_lcl, c,t,h, t_utc])