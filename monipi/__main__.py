import sys, os
import logging, signal
from datetime import datetime, timezone
from pathlib import Path
from .sample_scd30 import scd30_get_samples
from .mgr_session import Sessionman
from .mgr_time import run_on_min, Datetracker
from .mgr_exits import pause_exit_till_loop_complete, exit_gracefully
from .config import monipi_active, debug_status

DEBUG = debug_status

"""
    RUN AS PACKAGE: python -m monipi

    __main__ is the "runner" file
        (variables live in the config file)
        main designed to run once on an infinite loop

    Main:
        whilst Monipi_Active is True:
            runs until/unless keyboard interupt (or error)
                
            calls the SCD30 sensor (sample_scd30.py).
                loops for a reporting period of X, with Y secs between samples
                at the end of the reporting period, it averages the samples
                all samples and averages are saved to respective csvs

                X and Y are defined in the Config

                the first sample is taken when the time aligns with the reporting interval
                    the averaged value is timestamped to the end of the period 
                    e.g. reporting period = 5 mins and sample gap = 60 seconds
                        run at 12:34:23, starts at 12:35, averaged values timestamped 12:40
                            value is average of values at: 12:35, 12:36, 12:37, 12:38, 12:39
                
            mgr_data handles data manipulation and writing to csv
            mgr_time handles timing and date operations
            mgr_exits handles exiting gracefully
            mgr_session handles tracking a single sampling session with a json file
            sample_scd30 orchestrates sampling from the SCD30 sensor
"""

# BACKLOG
#   - backup "current" to named daily (samples) and weekly (averages) files and clear csv as part of process

dt = Datetracker()

def debug(msg):
    if DEBUG:
        print(msg)


logging.basicConfig(
    # configuration for the built-in python logger function
    level=logging.INFO,
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def ensure_runtime_dirs():
    # check used directories exist, and if not create them
    base_dir = Path (__file__).resolve().parent #/monipi/
    data_dir = base_dir / "data"                #/monipi/data/
    dailies_dir = data_dir / "dailies"          #/monipi/data/dailies/
    
    data_dir.mkdir(parents=True, exist_ok=True)
    dailies_dir.mkdir(parents=True, exist_ok=True)


def main():
    ensure_runtime_dirs
    logging.info("App started")
    debug(f"Monipi_active is set to: {monipi_active}")
    i = 0

    while monipi_active:
        dt.backup_dailies_on_date_change()
        run_on_min() # blocks operation until time condition met
        try:
            # run at next reporting period
            i += 1
            debug(f"Averaged sample loop {i}")
            scd30_get_samples()
        except KeyboardInterrupt:
            pause_exit_till_loop_complete()


def sigterm_handler(signum, frame):
    exit_gracefully(f"sigterm received (signum: {signum})")


signal.signal(signal.SIGTERM, sigterm_handler)

if __name__ == "__main__":
    main()
