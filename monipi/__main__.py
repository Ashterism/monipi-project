import sys, os
import logging, signal
import yaml
from datetime import datetime

from monipi.sampler import heartbeat


logging.basicConfig(
    level=logging.INFO,
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    config = load_config()
    beat_frequency = config["beat_frequency_seconds"]

    logging.info("App started")

    while True:
        try:    
            heartbeat(beat_frequency)
        except KeyboardInterrupt:
            exit_gracefully("User stopped with keyboard")


def load_config():
    try:
        # Prod path (on the Pi)
        with open("/etc/monipi/config.yaml", "r") as c:
            return yaml.safe_load(c)
    except FileNotFoundError:
        # Dev path (for dev on mac)
        here = os.path.dirname(__file__)
        project_root = os.path.dirname(here)
        dev_config_path = os.path.join(project_root, "config", "dev.yaml")
        with open(dev_config_path, "r") as c:
            return yaml.safe_load(c)


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


# for MAC
# logging needs diverting to a file to stop it printing in terminal
