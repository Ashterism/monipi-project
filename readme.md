

Libraries used:

(used .venv) - not on pi tho
(source .venv/bin/activate)

SCD30   # climate sensor
PMS5003 # particulate matter sensor 

pip install sensirion-i2c-scd30 pms5003

https://sensirion.github.io/python-i2c-scd30/index.html

---
*Pi set up*

sudo raspi-config
    enable I²C (for SCD30)
    enable Serial (for PMS5003).?

--
Keep running (systemd)
    moved it manually:
        sudo cp ~/monipi_project/config/monipi.service /etc/systemd/system/monipi.service
    checked on heartbeat:
        journalctl -u monipi.service -f


monipi-project/


====================
Been a while??
--------------

connect via:

ssh ash@monipi.local
password: usual

in codebase use: source .venv/bin/activate




====
WIRING 


SCD30
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