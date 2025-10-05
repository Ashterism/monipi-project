from datetime import datetime, timezone
import time

timestamp_utc = datetime.now(timezone.utc)
timestamp_local = datetime.now()

# print(timestamp_utc)
# print(timestamp_local)

# print(timestamp_utc.strftime("%Y-%m-%d %H:%M:%S"))


def run_on_sec():
    x = "x"
    while int(time.strftime("%S")) % 5 > 1:
        try:
            print(f"Time is:{time.strftime('%H:%M:%S')}!")
            time.sleep(0.9)
            if int(time.strftime("%S")) % 5 < 1:
                print("does task")
                break
        
        except KeyboardInterrupt:
            break

def run_on_min(min):
    
    while int(time.strftime("%M")) % min > 1:
        try:
            print(f"Time is:{time.strftime('%H:%M:%S')}!")
            time.sleep(0.9)
            if int(time.strftime("%S")) % min < 1:
                print("does task")
                break
        
        except KeyboardInterrupt:
            break

run_on_min(00) 


# print(time.ctime())
# print(type(int(time.strftime("%S"))))