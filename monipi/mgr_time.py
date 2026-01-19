from datetime import datetime, timezone
import time, sys
from .mgr_exits import pause_exit_till_loop_complete
from .mgr_data import Dataman
from .config import debug_status

from monipi.config import reporting_period_in_mins, secs_between_samples

dm = Dataman()

DEBUG = debug_status


def debug(msg):
    if DEBUG:
        print(msg)


def run_on_min(min=reporting_period_in_mins):
    debug(f"Reporting time in mins: {reporting_period_in_mins}")
    while int(time.strftime("%M")) % min > 1:
        try:
            print(f"Time is:{time.strftime('%H:%M:%S')}!")
            time.sleep(0.9)
            if int(time.strftime("%M")) % min < 1:
                print("does task")
                return

        except KeyboardInterrupt:
            pause_exit_till_loop_complete()


class Datetracker:

    def __init__(self):
        self.DATE_FMT = "%Y-%m-%d"
        self.currentDate = datetime.now().strftime(self.DATE_FMT)

    def backup_dailies_on_date_change(self):
        if datetime.now().strftime(self.DATE_FMT) == self.currentDate:
            debug(f"Still current day, self current date: {self.currentDate}")
            debug(f"local time: {datetime.now().strftime(self.DATE_FMT)}")
        else:
            debug(f"No longer current day, self current date: {self.currentDate}")
            debug(f"local time: {datetime.now().strftime(self.DATE_FMT)}")
            dm.backup_dailies()
            self.currentDate = datetime.now().strftime(self.DATE_FMT)
            debug(f"self.currentDate now: {self.currentDate}")
