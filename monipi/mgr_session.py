import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

"""
Session manager for tracking the lifecycle of an active sampling run.

This class handles creation and maintainance of a small JSON file
that represents the current session state. The file acts as lightweight,
persistent state so that long-running or restarted processes can:

- know when a session started
- understand the configured sampling parameters
- determine the expected end time
- report remaining time
- update session status (e.g. in progress, completed, stopped)

The session file is written to disk so it can be shared across modules
and survive restarts or crashes.
"""

class Sessionman:
    def __init__(self):
        # get and store the path to the json file in class "memory"
        self.file_path = (
            Path(__file__).resolve().parent / "data/current_session_details.json"
        )

    def create_session(
        self, reporting_period_in_mins, secs_between_samples, times_to_loop
    ):
        # get start and end times and convert to JSON-friendly strings
        s_start_raw = datetime.now(timezone.utc)
        s_start = s_start_raw.strftime("%Y-%m-%d %H:%M:%S")

        s_end_calc = s_start_raw + timedelta(
            seconds=secs_between_samples * times_to_loop
        )
        s_end = s_end_calc.strftime("%Y-%m-%d %H:%M:%S")
        # populate details for JSON
        session_details = {
            "start": s_start,
            "reporting period in mins": reporting_period_in_mins,
            "secs between samples": secs_between_samples,
            "times to loop": times_to_loop,
            "expected end time": s_end,
            "status": "in progress",
        }
        #(json.dumps(session_details))
        # write to file
        with open(self.file_path, "w") as json_file:
            json.dump(session_details, json_file)

    def check_session_end(self):
        with open(self.file_path, "r") as json_file:
            session_details = json.load(json_file)
            return session_details["expected end time"]

    def secs_to_end(self):
        exp_end_time_astime = datetime.strptime(
            self.check_session_end(), "%Y-%m-%d %H:%M:%S"
        ).replace(tzinfo=timezone.utc)
        time_to_completion = exp_end_time_astime - datetime.now(timezone.utc)
        total_seconds = int(time_to_completion.total_seconds())
        hrs, remainder = divmod(total_seconds, 3600)
        mins, secs = divmod(remainder, 60)

        return f"Time remaining is {hrs} hours, {mins} mins, and {secs} secs"

    def change_session_status(self, new_status):
        with open(self.file_path, "r+") as json_file:
            session_details = json.load(json_file)
            session_details["status"] = new_status
            json_file.seek(0)  # return to the start
            json.dump(session_details, json_file)
            json_file.truncate()  # delete stuff after
            print(session_details)


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
