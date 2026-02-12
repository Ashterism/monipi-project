import sys, logging
from pathlib import Path
from .config import mode as config_mode
from .mgr_sensor_state import Sensorstate

repo_root = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_root))
from tests.mock_sampler import get_mock_pms5003_sample

ss = Sensorstate()

"""
Samples the PMS5003 Sensor and returns 5 particle size readings
    - in DEV MODE uses mock data and avoids initialising code / ports not on mac
    - in PROD MODE uses real data from the sensor
    
    ONLY runs one cycle - repetition managed by Sampler.py
"""

def pms5003_get_sample(mode=config_mode):

    if mode == "dev":
        print(f"PMS5003: In {mode} mode")

        try:
            (pm1, pm25, pm10, pc03, pc25) = get_mock_pms5003_sample()
            print(f"PMS5003 DEV SAMPLE → PM1: {pm1} µg/m³, PM2.5: {pm25} µg/m³, PM10: {pm10} µg/m³, PC0.3: {pc03}, PC2.5: {pc25}")
            return (pm1, pm25, pm10, pc03, pc25)

        except Exception as exception_reason:
            print(f"Excepted: {exception_reason}")

    else:
        # check if PMS5003 initialised on serial port
        ss.pms5003_check()

        try:
            d = ss.pms.read()

            pm1 = d.pm_ug_per_m3(1)
            pm25 = d.pm_ug_per_m3(2.5)
            pm10 = d.pm_ug_per_m3(10)

            pc03 = d.pm_per_0_1l_air(0.3)
            pc25 = d.pm_per_0_1l_air(2.5)

            return (pm1, pm25, pm10, pc03, pc25)

        except Exception as exception_reason:
            logging.error(f"PMS5003 prod sample error: {exception_reason}")


if __name__ == "__main__":
    pms5003_get_sample()
