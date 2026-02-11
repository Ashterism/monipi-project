
import logging, time
from .mgr_data import Dataman  # class to manage database / csv interactions
from .mgr_session import Sessionman
from .config import mode as config_mode, reporting_period_in_mins, secs_between_samples
from .sample_pms5003 import pms5003_get_sample

sm = Sessionman()
dm = Dataman()
t2l = int((reporting_period_in_mins * 60) / secs_between_samples)

"""

the sampler should:
	•	know how often a sample cycle runs (eg every 2s, 5s, etc)
	•	know how long a window lasts (eg 60s)
	•	on each tick:
	•	call sample_scd30
	•	call sample_pms5003
	•	merge the results into one combined record
	•	collect records until a window is complete
	•	hand the window off for averaging
	•	reset and repeat

"""

def get_samples(times_to_loop=t2l, time_between_samples=secs_between_samples, mode=config_mode
):
    
    list_pm1 = []
    list_pm25 = []
    list_pm10 = []
    list_pc03 = []
    list_pc25 = []

    sm.create_session(reporting_period_in_mins, secs_between_samples, times_to_loop)

    for i in range(times_to_loop):

        #ADD IF DEV LOGIC HERE OR IN SAMPLE_PMS/SCD?

        pm25, pm10, pm1, pc03, pc25 = pms5003_get_sample()
        # add run get_SCD_samples here
        list_pm1.append(pm1)
        list_pm25.append(pm25)
        list_pm10.append(pm10)
        list_pc03.append(pc03)
        list_pc25.append(pc25)
        # map out SCD samples here

        time.sleep(time_between_samples)

    # do averaging and writes here i guess
    # av_pm25 = sum(list_pm25) / len(list_pm25)

 


if __name__ == "__main__":
    get_samples()

"""

SCD
-----------------------
- only initialise once?  currently doing a warm up (do here?)


Aggregator (new class?)
------------------------
	•	receive a list of sample dicts
	•	compute:
	•	means
	•	mins/maxes (maybe later)
	•	counts / validity
	•	return one aggregated dict


"""
