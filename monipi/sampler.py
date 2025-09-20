import logging
import time
from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection, CrcCalculator
from sensirion_driver_adapters.i2c_adapter.i2c_channel import I2cChannel
from sensirion_i2c_scd30.device import Scd30Device

# def heartbeat(beat_frequency):
#     logging.info("Heartbeat")
#     time.sleep(beat_frequency)


def scd30_loop(times_to_loop, time_between_samples):

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
                time.sleep(time_between_samples)
                (co2_concentration, temperature, humidity
                ) = sensor.blocking_read_measurement_data()
                print(f"co2_concentration: {co2_concentration}; "
                    f"temperature: {temperature}; "
                    f"humidity: {humidity}; "
                    )
            except BaseException:
                continue
        sensor.stop_periodic_measurement()