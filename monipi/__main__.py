import sys, os
import logging, signal
from datetime import datetime, timezone
from .sample_scd30 import scd30_get_samples
from .mgr_session import Sessionman
from .mgr_time import run_on_min, Datetracker
from .mgr_exits import pause_exit_till_loop_complete, exit_gracefully
from .config import monipi_active, debug_status

DEBUG = debug_status

"""
    RUN AS PACKAGE: python -m monipi

    main "runner" file
    whilst Monipi_Active is True:
        runs on an infinite loop (unless keyboard interupt)
            
            calls the SCD30 sensor (sampler.py).
                loops for a reporting period of X, with Y secs between samples
                at the end of the reporting period, it averages the samples
                all samples and averages are saved to respective csvs

                X and Y are defined in the Config

                the first sample is taken when the time aligns with the reporting interval
                    the averaged value is timestamped to the end of the period 
                    e.g. reporting period = 5 mins and sample gap = 60 seconds
                        run at 12:34:23, starts at 12:35, averaged values timestamped 12:40
                            value is average of values at: 12:35, 12:36, 12:37, 12:38, 12:39
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


def main():
    logging.info("App started")
    debug(f"Monipi_active is set to: {monipi_active}")
    i = 0

    while monipi_active:
        dt.backup_dailies_on_date_change()
        run_on_min()
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
