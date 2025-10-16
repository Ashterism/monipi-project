from .mgr_session import Sessionman
from .config import reporting_period_in_mins, secs_between_samples

session = Sessionman()


t2l = int((reporting_period_in_mins*60)/secs_between_samples)
times_to_loop=t2l
time_between_samples=secs_between_samples

#session.create_session(reporting_period_in_mins, secs_between_samples,times_to_loop)

# session.check_session_end()
#output = session.secs_to_end()
#print(output)

# session.change_session_status("terminated")




"""
basically

- create a json that stores:
    - when the job started
    - reporting_period_in_mins
    - secs_between_samples 
    - times_to_run
    - time_to_end

- method to read it
    - esp time_to_end

"""
