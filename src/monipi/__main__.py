import logging, signal

import monipi.config as config

from .control.sampler import get_samples
from .process.session_manager import SessionManager
from .runtime.mgr_time import run_on_min, Datetracker
from .runtime.mgr_exits import pause_exit_till_loop_complete, exit_gracefully

DEBUG = config.debug_status


"""
Entry point for Monipi.
Run on (pi) start-up.

Runs a continuous loop:
- waits for next reporting interval
- calls sampler.get_samples()

Sensors are initialised once and reused.
Designed to run continuously via systemd.
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
    logging.info(f"Run mode detected: {config.mode}")
    debug(f"Monipi_active is set to: {config.monipi_active}")
    i = 0

    while config.monipi_active:
        dt.backup_dailies_on_date_change()
        run_on_min() # blocks operation until time condition met
        try:
            # run at next reporting period
            i += 1
            debug(f"Averaged sample loop {i}")
            get_samples()
        except KeyboardInterrupt:
            pause_exit_till_loop_complete()


def sigterm_handler(signum, frame):
    exit_gracefully(f"sigterm received (signum: {signum})")


signal.signal(signal.SIGTERM, sigterm_handler)

if __name__ == "__main__":
    main()
