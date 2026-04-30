import sys, os
import logging, signal
from datetime import datetime, timezone
from pathlib import Path
from .control.sampler import get_samples
from .process.session_manager import SessionManager
from .runtime.mgr_time import run_on_min, Datetracker
from .runtime.mgr_exits import pause_exit_till_loop_complete, exit_gracefully
from .config import monipi_active, debug_status

DEBUG = debug_status


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


def ensure_runtime_dirs():
    # check used directories exist, and if not create them
    base_dir = Path(__file__).resolve().parent #/monipi/
    data_dir = base_dir / "data"                #/monipi/data/
    dailies_dir = data_dir / "dailies"          #/monipi/data/dailies/
    
    data_dir.mkdir(parents=True, exist_ok=True)
    dailies_dir.mkdir(parents=True, exist_ok=True)


def main():
    ensure_runtime_dirs()
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
            get_samples()
        except KeyboardInterrupt:
            pause_exit_till_loop_complete()


def sigterm_handler(signum, frame):
    exit_gracefully(f"sigterm received (signum: {signum})")


signal.signal(signal.SIGTERM, sigterm_handler)

if __name__ == "__main__":
    main()
