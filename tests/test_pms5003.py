

from pms5003 import PMS5003

pms5003 = PMS5003(device="/dev/serial0", baudrate=9600)

try:
    while True:
        data = pms5003.read()
        print(data)

except KeyboardInterrupt:
    pass
