import sys, os
import logging, signal
from datetime import datetime, timezone
from pathlib import Path
from .sampler import get_samples
from .mgr_session import Sessionman
from .mgr_time import run_on_min, Datetracker
from .mgr_exits import pause_exit_till_loop_complete, exit_gracefully
from .config import monipi_active, debug_status

DEBUG = debug_status

"""
RUN AS PACKAGE: python -m monipi

__main__ is the application runner.
Configuration values live in config.py.

Main loop behaviour:

While `monipi_active` is True:

    • Wait until the next reporting interval boundary (managed by mgr_time).
    • Call sampler.get_samples() once.

The sampler:
    • Samples BOTH sensors (SCD30 and PMS5003) on a fixed interval.
    • Writes raw readings for each sensor to CSV (including local + UTC timestamps).
    • Accumulates values in memory during the reporting window.
    • Calculates averages at the end of the window.
    • Writes averaged values to separate CSV files.

Timing example:
    Reporting period = 5 minutes
    Sample gap = 60 seconds

    If started at 12:34:23:
        First aligned sample at 12:35
        Raw samples at: 12:35, 12:36, 12:37, 12:38, 12:39
        Averaged row timestamped to end of window (12:40)

Supporting modules:
    • mgr_data          CSV schema + file writing
    • mgr_time          Interval alignment + date tracking
    • mgr_exits         Graceful shutdown handling
    • mgr_session       Session tracking via JSON
    • mgr_sensor_state  One-time hardware initialisation
    • sample_*          Single-cycle sensor reads

Design intent:
    • Sensors initialise once and remain active.
    • Separation of concerns between timing, sampling, and storage.
    • Continuous, unattended operation via systemd.
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
