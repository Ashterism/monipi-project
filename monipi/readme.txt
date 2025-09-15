

Libraries used:

(used .venv)

PyYAML  # to use yaml for config.yaml
SCD30   # climate sensor
PMS5003 # particulate matter sensor 

pip install adafruit-circuitpython-scd30 pms5003

---
*Pi set up*

sudo raspi-config
    enable I²C (for SCD30)
    enable Serial (for PMS5003).

