import logging, sys, time
from datetime import datetime, timezone
from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection, CrcCalculator
from sensirion_driver_adapters.i2c_adapter.i2c_channel import I2cChannel
from sensirion_i2c_scd30.device import Scd30Device
from .mgr_data import Dataman  # class to manage database / csv interactions
from .mgr_session import Sessionman

from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_root))
from tests.mock_sampler import get_mock_sample
from .config import mode as config_mode, reporting_period_in_mins, secs_between_samples

sm = Sessionman()
dm = Dataman()
t2l = int((reporting_period_in_mins * 60) / secs_between_samples)

"""
SCD30 sampling runner.

Controls one full sampling cycle for a single reporting period:
- initialises a sampling session
- collects multiple sensor readings at a fixed interval
- aggregates readings over the reporting window
- writes raw samples (dev) and averaged values (dev + prod) via Dataman

Supports a dev mode using mock samples so the sampling and persistence
logic can be exercised without the physical sensor attached.

This module runs once per call; repetition and scheduling are handled
by the package entrypoint.
"""


def scd30_get_samples(
    times_to_loop=t2l, time_between_samples=secs_between_samples, mode=config_mode
):

    list_co2 = []
    list_temp = []
    list_hum = []
    loop = 1

    sm.create_session(reporting_period_in_mins, secs_between_samples, times_to_loop)

    if mode == "dev":
        print(
            f"In {mode} mode, looping {times_to_loop} times with {time_between_samples} delay"
        )
        for i in range(times_to_loop):
            try:
                (co2, temp, hum) = get_mock_sample()
                dm.write_readings(datetime.now(timezone.utc), co2, temp, hum)
                list_co2.append(co2)
                list_temp.append(temp)
                list_hum.append(hum)
                print(f"Writing to csv... e.g.{list_co2}")
                time.sleep(time_between_samples)

            except Exception as exception_reason:
                print(f"Excepted: {exception_reason}")

    else:
        with LinuxI2cTransceiver("/dev/i2c-1") as i2c_transceiver:
            channel = I2cChannel(
                I2cConnection(i2c_transceiver),
                slave_address=0x61,
                crc=CrcCalculator(8, 0x31, 0xFF, 0x0),
            )
            sensor = Scd30Device(channel)
            try:
                sensor.stop_periodic_measurement()
                sensor.soft_reset()
                time.sleep(2.0)
            except BaseException:
                logging.warning("SCD30 sensor reset errored")

            sensor.start_periodic_measurement(0)
            for i in range(times_to_loop):
                try:
                    (co2, temp, hum) = sensor.blocking_read_measurement_data()
                    list_co2.append(co2)
                    list_temp.append(temp)
                    list_hum.append(hum)
                    # print(list_co2)

                    time.sleep(time_between_samples)

                except BaseException:
                    continue
            sensor.stop_periodic_measurement()

    timestamp_utc = datetime.now(timezone.utc)
    timestamp_local = datetime.now().strftime("%D/%M/%y %H:%M:%S")
    co2_avg = sum(list_co2) / len(list_co2)
    temp_avg = sum(list_temp) / len(list_temp)
    hum_avg = sum(list_hum) / len(list_hum)

    dm.write_averages(timestamp_local, co2_avg, temp_avg, hum_avg, timestamp_utc)


if __name__ == "__main__":
    scd30_get_samples()
