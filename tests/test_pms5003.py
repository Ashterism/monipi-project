

from pms5003 import PMS5003

pms5003 = PMS5003(device="/dev/serial0", baudrate=9600)


"""
Sample values 
PM1.0 ug/m3 (ultrafine particles):                             pm1_cf1
PM2.5 ug/m3 (combustion particles, organic compounds, metals): pm25_cf1
PM10 ug/m3  (dust, pollen, mould spores):                      pm10_cf1
PM1.0 ug/m3 (atmos env):                                       pm1
PM2.5 ug/m3 (atmos env):                                       pm25
PM10 ug/m3 (atmos env):                                        pm10
>0.3um in 0.1L air:                                            pc03
>0.5um in 0.1L air:                                            pc05
>1.0um in 0.1L air:                                            pc10
>2.5um in 0.1L air:                                            pc25
>5.0um in 0.1L air:                                            pc50
>10um in 0.1L air:                                             pc100

"""


try:
    while True:
        d = pms.read()

        pm1      = d.pm_ug_per_m3(1)
        pm25     = d.pm_ug_per_m3(2.5)
        pm10     = d.pm_ug_per_m3(10)

        pm1_cf1  = d.pm_ug_per_m3_cf1(1)
        pm25_cf1 = d.pm_ug_per_m3_cf1(2.5)
        pm10_cf1 = d.pm_ug_per_m3_cf1(10)

        pc03     = d.pm_per_0_1l_air(0.3)
        pc05     = d.pm_per_0_1l_air(0.5)
        pc10     = d.pm_per_0_1l_air(1.0)
        pc25     = d.pm_per_0_1l_air(2.5)
        pc50     = d.pm_per_0_1l_air(5.0)
        pc100    = d.pm_per_0_1l_air(10)

        print(f"pm1: {pm1}")
        print(f"pm25: {pm25}")
        print(f"pm10: {pm10}")
        print(f"pm1_cf1: {pm1_cf1}")
        print(f"pm25_cf1: {pm25_cf1}")
        print(f"pm10_cf1: {pm10_cf1}")
        print(f"pc03: {pc03}")
        print(f"pc05: {pc05}")
        print(f"pc10: {pc10}")
        print(f"pc25: {pc25}")
        print(f"pc50: {pc50}")
        print(f"pc100: {pc100}")
        print("-" * 40)

except KeyboardInterrupt:
    pass