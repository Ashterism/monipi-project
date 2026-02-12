import logging, time
from datetime import datetime, timezone
from .mgr_data import Dataman  # class to manage database / csv interactions
from .mgr_session import Sessionman
from .config import mode as config_mode, reporting_period_in_mins, secs_between_samples

from .sample_pms5003 import pms5003_get_sample
from .sample_scd30 import scd30_get_samples

sm = Sessionman()
dm = Dataman()
t2l = int((reporting_period_in_mins * 60) / secs_between_samples)

"""

add explainer here

"""

def get_samples(times_to_loop=t2l, time_between_samples=secs_between_samples, mode=config_mode
):
    #--SCD30--#
    list_co2 = []
    list_temp = []
    list_hum = []
    
    #--PMS5003--#
    list_pm1 = []
    list_pm25 = []
    list_pm10 = []
    list_pc03 = []
    list_pc25 = []

    sm.create_session(reporting_period_in_mins, secs_between_samples, times_to_loop)

    for i in range(times_to_loop):

        #--GET TIME--#
        timestamp_utc = datetime.now(timezone.utc)
        timestamp_local = datetime.now().strftime("%D/%M/%y %H:%M:%S")
        #--READ SCD30 & PMS5002--#
        pm1, pm25, pm10, pc03, pc25 = pms5003_get_sample()
        co2, temp, hum = scd30_get_samples()
        #--Write readings--#
        dm.write_readings_pms5003(timestamp_utc, pm1, pm25, pm10, pc03, pc25)
        dm.write_readings_scd30(timestamp_utc, co2, temp, hum)

        #--Add values to respective lists--#
        list_pm1.append(pm1)
        list_pm25.append(pm25)
        list_pm10.append(pm10)
        list_pc03.append(pc03)
        list_pc25.append(pc25)

        list_co2.append(co2)
        list_temp.append(temp)
        list_hum.append(hum)

        #--Wait for next sample--#
        time.sleep(time_between_samples)

    #--EXIT LOOP, AVERAGE AND WRITE TO CSV--#

    avg_pm1 = sum(list_pm1) / len(list_pm1)
    avg_pm25 = sum(list_pm25) / len(list_pm25)
    avg_pm10 = sum(list_pm10) / len(list_pm10)
    avg_pc03 = sum(list_pc03) / len(list_pc03)
    avg_pc25 = sum(list_pc25) / len(list_pc25)

    avg_co2 = sum(list_co2) / len(list_co2)
    avg_temp = sum(list_temp) / len(list_temp)
    avg_hum = sum(list_hum) / len(list_hum)

    dm.write_averages_scd30(timestamp_local, avg_co2, avg_temp, avg_hum, timestamp_utc) 
    dm.write_averages_pms5003(timestamp_local, avg_pm1, avg_pm25, avg_pm10, avg_pc03, avg_pc25, timestamp_utc)
  

if __name__ == "__main__":
    get_samples()

