
# Monipi

Monipi is a Raspberry Pi–based environmental monitoring system designed to measure indoor air quality continuously and reliably.

It currently integrates two sensors:
* SCD30 – CO₂ (ppm), temperature (°C), and relative humidity (%)
* PMS5003 – Particulate matter (PM1.0, PM2.5, PM10) and particle counts

The system runs continuously, samples both sensors on a fixed interval, logs raw readings to CSV, and writes averaged data over a defined reporting window.

The focus of the project is learning clean architecture and building a robust, understandable monitoring pipeline rather than producing a polished commercial device.

## How Monipi works

Monipi runs as a continuous loop.

At each sampling interval:
* Both sensors are read
* Raw readings are written to CSV
* Values are added to in-memory lists for averaging

At the end of each reporting window:
* Averages are calculated
* Averaged values are written to separate CSV files

Each raw row includes:
* A local timestamp (for human readability)
* A UTC timestamp (for consistency and later processing)

Averaged rows represent the end of the reporting window.

## Architecture

The project is structured to separate responsibilities cleanly:
* sampler.py controls the sampling loop and averaging window
* sample_scd30.py reads one SCD30 cycle
* ample_pms5003.py reads one PMS5003 cycle
* mgr_sensor_state.py handles one-time sensor initialisation and prevents repeated hardware resets
* mgr_data.py owns the CSV schema and file writing
* mgr_time.py, mgr_session.py, and mgr_exits.py support time control, session logic, and controlled shutdown behaviour
* config.py defines timing and mode configuration

Sensors are initialised once and kept running. They are not reset between samples when running on mains power.

## Date Storage

Raw readings are stored separately per sensor:
* current_samples_scd30.csv
* current_samples_pms5003.csv

Averaged readings are stored separately:
* current_sample_averages_scd30.csv
* current_sample_averages_pms5003.csv

The schema is intentionally simple and explicit. CSV is used for transparency, portability, and ease of later integration into a website or similar.


## Raspberry Pi Setup
On the Raspberry Pi:
* Enable I²C (for SCD30)
* Enable Serial (for PMS5003)

Monipi is intended to run continuously via systemd. A service file is included in the config directory and can be copied into /etc/systemd/system/.

Logs can be monitored using journalctl.


## Development Environment

Development is typically done using a local Python virtual environment. The .venv directory is used on macOS for development only and is not required (though fine to use) on the Pi.  

Required libraries:
* sensirion-i2c-scd30
* pms5003

Mock sensor data is used in development mode to allow coding without hardware attached.


## Wiring

### SCD30 (I²C)

Connected via I²C to the Raspberry Pi.

Only the required pins are connected:
	•	VDD
	•	GND
	•	SCL
	•	SDA
	•	SEL (for interface selection)

https://github.com/Sensirion/raspberry-pi-i2c-scd30/blob/master/images/raspi-i2c-pinout-3.3V-SEL.png

![alt text](/setup/pi_ios.png)

![alt text](/setup/scd30_ios.png)

| *Pin* | *Cable Color* | *Name* | *Description*  | *Comments* |
|-------|---------------|:------:|----------------|------------|
| 1 | red | VDD | Supply Voltage | 3.3V to 5.5V
| 2 | black | GND | Ground |
| 3 | yellow | SCL | I2C: Serial clock input |
| 4 | green | SDA | I2C: Serial data input / output |
| 5 |  | RDY |  | High when data is available - do not connect
| 6 |  | PWM |  | do not connect
| 7 | blue | SEL | Interface select | Pull to ground or floating for I2C



### PMS5003 (Serial)

Connected via serial using /dev/serial0.

Uses the Pimoroni PMS5003 Python library.


## Power Considerations

The system is currently designed to run on mains power.

Sensors remain powered and in continuous measurement mode. There is no power-cycling between readings.

If deployed on battery in future, optimisation could include:
* Sleeping PMS5003 between reads
* Reducing WiFi usage
* Increasing reporting interval


## Relevant sources



## Useful notes

Can be easiest to use venv on both environments:
- source .venv/bin/activate)

There are libraries for both Sensors:

*SCD*
- pip install sensirion-i2c-scd30 pms5003
- SCD30 Guidance / docs: https://sensirion.github.io/python-i2c-scd30/index.html
- PMS5003 Guidance / docs: https://github.com/pimoroni/pms5003-python?utm_source=chatgpt.com

---
*Pi set up*

sudo raspi-config
    enable I²C (for SCD30)
    enable Serial (for PMS5003).?

To set up the Pi to autorun at beginning, run:
- sudo cp ~/monipi_project/config/monipi.service /etc/systemd/system/monipi.service
- check on heartbeat after reboot:
        journalctl -u monipi.service -f
