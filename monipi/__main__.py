import sys, os
import logging, signal
from datetime import datetime
from sampler import scd30_get_samples

from pathlib import Path                                        # can remove this and should work
repo_root = Path(__file__).resolve().parent.parent              # with just from config.config once
sys.path.append(str(repo_root))                                 # ready to use packaged load commands all the time 
from config.config import monipi_active, samples_to_average, secs_between_samples         # i.e. python -m monipi.__main__ etc

"""
    calls the SCD30 sensor (sampler.py) and feeds in how many
    times should sample on a loop.  
"""

logging.basicConfig(
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