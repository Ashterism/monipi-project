import logging, sys, time
from datetime import datetime, timezone
from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection, CrcCalculator
from sensirion_driver_adapters.i2c_adapter.i2c_channel import I2cChannel
from sensirion_i2c_scd30.device import Scd30Device
from dataman import Dataman     # class to manage database / csv interactions

from pathlib import Path
repo_root = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_root))
from tests.mock_sampler import get_mock_sample

dm = Dataman()

"""
    this file controls the sampling process and makes use of the
    dataman class to read/write to the data to csv

    there is a dev mode so the code can be tested without the 
    sensor connected
"""

def scd30_get_samples(times_to_loop=5, time_between_samples=1, mode="dev"):

    list_co2 = []; list_temp = []; list_hum = []

    if mode == "dev":
        print(f"In {mode} mode, looping {times_to_loop} times with {time_between_samples} delay")
        for i in range(times_to_loop):
            try:
                (co2, temp, hum) = get_mock_sample()
                dm.write_readings(datetime.now(timezone.utc), co2,temp, hum)
                list_co2.append(co2); list_temp.append(temp); list_hum.append(hum)
                # print(list_co2)

                time.sleep(time_between_samples)
            except Exception as exception_reason:
                print(f"Excepted: {exception_reason}")

    else:
        with LinuxI2cTransceiver("/dev/i2c-1") as i2c_transceiver:
            channel = I2cChannel(I2cConnection(i2c_transceiver),
                                slave_address=0x61,
                                crc=CrcCalculator(8, 0x31, 0xff, 0x0))
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
                    list_co2.append(co2); list_temp.append(temp); list_hum.append(hum)
                    # print(list_co2)

                    time.sleep(time_between_samples)

                except BaseException:
                    continue
            sensor.stop_periodic_measurement()

    # print(type(list_co2))
    # for _ in list_co2:
    #     print(f"{type(list_co2[_])} is {list_co2[_]}")

    timestamp_utc = datetime.now(timezone.utc)
    timestamp_local = datetime.now().strftime("%D/%M/%y %H:%M:%S")
    co2_avg = sum(list_co2) / len(list_co2)
    temp_avg = sum(list_temp) / len(list_temp)
    hum_avg = sum(list_hum) / len(list_hum)
    # drop outlier values (i.e the warm up ones)

    dm.write_averages(timestamp_local, co2_avg, temp_avg, hum_avg, timestamp_utc)

if __name__ == "__main__":
    scd30_get_samples()