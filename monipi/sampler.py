import logging
import time


def heartbeat(beat_frequency):
    logging.info("Heartbeat")
    time.sleep(beat_frequency)
