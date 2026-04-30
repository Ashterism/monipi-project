import logging, sys
from pathlib import Path
from ..config import mode as config_mode
from ..process.sensor_state import Sensorstate

repo_root = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_root))
from tests.mock_sampler import get_mock_scd30_sample

ss = Sensorstate()


"""
Refactored for control of cycle to live in sampler.py (see macair 
VS Code monipi archive for the pre-refactored version)

Samples the SCD Sensor and returns 3 climate readings
    - in DEV MODE uses mock data 
    - in PROD MODE uses real data from the sensor
    
    ONLY runs one cycle
"""

def scd30_get_samples(mode=config_mode):

    if mode == "dev":
        print(f"SCD30: In {mode} mode")

        try:
            (co2, temp, hum) = get_mock_scd30_sample()
            print(f"SCD30 DEV SAMPLE → CO2: {co2}, Temp: {temp}, Hum: {hum}")
            return (co2, temp, hum)

        except Exception as exception_reason:
            logging.error(f"SCD30 dev sample error: {exception_reason}")
            return (None, None, None)

    # PROD
    ss.scd30_check()
    try:
        (co2, temp, hum) = ss.scd.blocking_read_measurement_data()
        return (co2, temp, hum)
    except Exception as exception_reason:
        logging.error(f"SCD30 prod sample error: {exception_reason}")
        return (None, None, None)


if __name__ == "__main__":
    scd30_get_samples()
