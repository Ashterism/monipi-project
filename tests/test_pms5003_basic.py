

from pms5003 import PMS5003

pms5003 = PMS5003(device="/dev/serial0", baudrate=9600)


"""
Sample values 
PM1.0 ug/m3 (ultrafine particles):                             19
PM2.5 ug/m3 (combustion particles, organic compounds, metals): 29
PM10 ug/m3  (dust, pollen, mould spores):                      33
PM1.0 ug/m3 (atmos env):                                       19
PM2.5 ug/m3 (atmos env):                                       29
PM10 ug/m3 (atmos env):                                        33
>0.3um in 0.1L air:                                            1180
>0.5um in 0.1L air:                                            954
>1.0um in 0.1L air:                                            220
>2.5um in 0.1L air:                                            22
>5.0um in 0.1L air:                                            0
>10um in 0.1L air:                                             0

"""


try:
    while True:
        data = pms5003.read()
        print(data)

except KeyboardInterrupt:
    pass