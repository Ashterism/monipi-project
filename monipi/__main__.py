import sys, os
import logging, signal
from datetime import datetime, timezone
from .sample_scd30 import scd30_get_samples
from .mgr_session import Sessionman
from .utils.mgr_time import run_on_min
from .utils.mgr_exits import pause_exit_till_loop_complete, exit_gracefully
from .config import monipi_active


# note to self:
#     run with:
#         python -m monipi (from monipi_project)
#     or for a script:
#         python -m monipi/__main__.py (that folder)

"""
    main "runner" file
    calls the SCD30 sensor (sampler.py).
        takes a sample every X econds, for a loop of Y:
            all samples are written to samples.csv
            all samples in the loop are averaged and written to sample_averages
        the first sample is taken when the time aligns with the reporting interval
            the averaged value is timestamped to the end of the period 
            e.g. sample period = 5 mins and sample gap = 60 seconds
                run at 12:34:23, starts at 12:35, averaged values timestamped 12:40
                    value is average of values at: 12:35, 12:36, 12:37, 12:38, 12:39

    is intended to run in perpetuity unless stopped via config
    by changing 'polling_active' to false.

    BACKLOG
    - backup "current" to named daily (samples) and weekly (averages) files and clear csv as part of process

"""

DEBUG = True

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
