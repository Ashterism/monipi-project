# tests/test_scd30_mock.py
from sensirion_driver_adapters.mocks.i2c_connection_mock import I2cConnectionMock
from sensirion_driver_adapters.mocks.i2c_sensor_mock import I2cSensorMock
from sensirion_driver_adapters.i2c_adapter.i2c_channel import I2cChannel
from monipi.scd30 import main

def test_quickstart_runs_with_mock():
    sensor = I2cSensorMock()
    ch = I2cChannel(I2cConnectionMock(sensor), slave_address=0x61)
    main(argv=["-p", "/dev/fake"], channel=ch)  # should not touch real /dev/i2c-1