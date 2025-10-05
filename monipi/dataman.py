import csv, os
from pathlib import Path

class Dataman:
    def __init__(self):
        self.csvpath_readings = str("data/current_readings.csv")
        self.csvpath_avgs = str("data/current_avgs.csv")
        # if header row missing then add?

    def read_last_row(self):
        with open(self.csvpath_avgs, "r") as last_row_db:
            lastrow = last_row_db.readlines()[-1]
            print(lastrow)

    def read_row(self, option=''):
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
        with open(self.csvpath_readings, "a", newline='') as readings_db:
            writer = csv.writer(readings_db)   # loads csv into reader
            writer.writerow([t_utc, c,t,h])

    def write_averages(self, t_lcl, c,t,h, t_utc):
        with open(self.csvpath_avgs, "a", newline='') as averages_db:
            writer = csv.writer(averages_db)   # loads csv into reader
            writer.writerow([t_lcl, c,t,h, t_utc])


# dm = Dataman()
# dm.write_row("crack","snapple", "pop")