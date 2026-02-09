

from pms5003 import PMS5003

try:
    while True:
        data = pms5003.read()
        print(data)

except KeyboardInterrupt:
    pass
