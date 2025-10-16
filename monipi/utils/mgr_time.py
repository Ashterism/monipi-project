from datetime import datetime, timezone
import time, sys
from .mgr_exits import pause_exit_till_loop_complete

from monipi.config import reporting_period_in_mins, secs_between_samples

timestamp_utc = datetime.now(timezone.utc)
timestamp_local = datetime.now()

def run_on_min(min = reporting_period_in_mins):
    print(reporting_period_in_mins)
    while int(time.strftime("%M")) % min > 1:
        try:
            # print(min)
            # print(type(min))
            print(time.strftime("%M"))
            print(f"Time is:{time.strftime('%H:%M:%S')}!")
            time.sleep(0.9)
            if int(time.strftime("%M")) % min < 1:
                print("does task")
                return
        
        except KeyboardInterrupt:
            pause_exit_till_loop_complete()

