from .mgr_session import Sessionman
from .mgr_data import Dataman
from .mgr_time import Datetracker
from .config import reporting_period_in_mins, secs_between_samples
import time
from pathlib import Path
from datetime import datetime, timedelta

session = Sessionman()
dm = Dataman()
cd = Datetracker()


def test_sessionman():
    t2l = int((reporting_period_in_mins * 60) / secs_between_samples)
    times_to_loop = t2l
    time_between_samples = secs_between_samples

    # session.create_session(reporting_period_in_mins, secs_between_samples,times_to_loop)

    # session.check_session_end()
    # output = session.secs_to_end()
    # print(output)

    # session.change_session_status("terminated")


def test_dataman():
    dm.read_averages()


def test_current_day():
    #cd.set_initial_date()
    cd.backup_dailies_on_date_change
    time.sleep(5)
    cd.backup_dailies_on_date_change()


def test_renamefile():
    path = Path(__file__).resolve().parent
    # above already in Dataman

    file_path = path / "data/current_session_details.json"
    date_for_file = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    file_path.rename(f"{path}/data/dailies/{date_for_file}.json")


test_current_day()


"""
basically

- create a json that stores:
    - when the job started
    - reporting_period_in_mins
    - secs_between_samples 
    - times_to_run
    - time_to_end

- method to read it
    - esp time_to_end

"""
