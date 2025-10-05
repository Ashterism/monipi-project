import sys, os
import logging, signal
from datetime import datetime
from sampler import scd30_get_samples
from datetime import datetime, timezone

from pathlib import Path                                        # can remove this and should work
repo_root = Path(__file__).resolve().parent.parent              # with just from config.config once
sys.path.append(str(repo_root))                                 # ready to use packaged load commands all the time 
from config.config import monipi_active, samples_to_average, secs_between_samples         # i.e. python -m monipi.__main__ etc

timestamp_utc = datetime.now(timezone.utc)
timestamp_local = datetime.now()

"""
    main "runner" file
    calls the SCD30 sensor (sampler.py).
        takes a sample every X seconds, for a loop of Y:
            all samples are written to samples.csv
            all samples in the loop are averaged and written to sample_averages
        the first sample is taken on the minute and then at X seconds after
            the averaged value is timestamped to the end of the period 
            e.g. sample period = 5 mins and sample gap = 60 seconds
                run at 12:34:23, starts at 12:35, timestamped 12:40
                    value is average of values at: 12:35, 12:36, 12:37, 12:38, 12:39

    is intended to run in perpetuity unless stopped via config
    by changing 'polling_active' to false.

    BACKLOG
    - backup "current" to named daily (samples) and weekly (averages) files and clear csv as part of process

"""

logging.basicConfig(
    # configuration for the built-in python logger function
    level=logging.INFO,
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def main():
    logging.info("App started")

    while monipi_active == True:
        try:    
            scd30_get_samples(samples_to_average, secs_between_samples)
        except KeyboardInterrupt:
            exit_gracefully("User stopped with keyboard")

## then add the runner here, to run at X secs / mins
##         -- pass in scd30_sensor as the variable, and it runs that

## add more tests?


def exit_gracefully(exitmsg="no message provided", signum=""):
    logging.info(
        f"App exited - {exitmsg} {signum}",
    )
    # 
    # finish logging
    # close any open files etc
    #
    sys.exit(exitmsg)


def sigterm_handler(signum, frame):
    exit_gracefully(f"sigterm received (signum: {signum})")


signal.signal(signal.SIGTERM, sigterm_handler)

if __name__ == "__main__":
    main()