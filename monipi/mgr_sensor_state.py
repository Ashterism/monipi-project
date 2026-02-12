import logging
import time

from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection, CrcCalculator
from sensirion_driver_adapters.i2c_adapter.i2c_channel import I2cChannel
from sensirion_i2c_scd30.device import Scd30Device


class Sensorstate:
    """
    Holds/controls state for sensor initialisation.

    Purpose:
      - Avoid initialising hardware in dev mode (e.g. mac)
      - Avoid repeatedly re-initialising sensors in a long-running loop

    This class should keep sensor objects alive for the lifetime of the process.
    """

    def __init__(self):
        # None equates to not initialised yet
        self.pms = None
        self.scd = None
        self._scd_i2c_transceiver = None

    def scd30_initialise(self):
        try:
            # Keep the transceiver open for the lifetime of the process.
            self._scd_i2c_transceiver = LinuxI2cTransceiver("/dev/i2c-1")
            channel = I2cChannel(
                I2cConnection(self._scd_i2c_transceiver),
                slave_address=0x61,
                crc=CrcCalculator(8, 0x31, 0xFF, 0x0),
            )
            self.scd = Scd30Device(channel)

            # One-time reset/start
            try:
                self.scd.stop_periodic_measurement()
                self.scd.soft_reset()
                time.sleep(2.0)
            except BaseException:
                logging.warning("SCD30 sensor reset errored")

            self.scd.start_periodic_measurement(0)

        except Exception as exception_reason:
            logging.error(f"SCD30 initialise error: {exception_reason}")
            self.scd = None
            self._scd_i2c_transceiver = None

    def scd30_check(self):
        if self.scd is None:
            self.scd30_initialise()

    def scd30_stop(self):
        """Stop periodic measurement if the SCD30 has been initialised."""
        if self.scd is None:
            return

        try:
            self.scd.stop_periodic_measurement()

        except Exception as exception_reason:
            logging.warning(f"SCD30 stop errored: {exception_reason}")

    # ==== PMS5003 ==== #

    def pms5003_initialise(self):
        # initialise PMS5003 device on serial
        # only in prod, not dev (not supported on mac)
        from pms5003 import PMS5003

        self.pms = PMS5003(device="/dev/serial0", baudrate=9600)

    def pms5003_check(self):
        # check if "nothing" initialised
        if self.pms is None:
            self.pms5003_initialise()
        else:
            return
