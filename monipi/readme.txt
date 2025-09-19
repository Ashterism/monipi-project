

Libraries used:

(used .venv) - not on pi tho

PyYAML  # to use yaml for config.yaml
SCD30   # climate sensor
PMS5003 # particulate matter sensor 

pip install sensirion-i2c-scd30 pms5003
pip install "sensirion-i2c-scd30[test]" (for testing via pytest on mac)

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