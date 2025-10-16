import sys, logging
from ..mgr_session import Sessionman

sm = Sessionman()

def pause_exit_till_loop_complete():
    answer = ""
    while answer not in ["Y", "N", "y","n"]:
        answer = input(f"\n===================\nALLOW LOOP TO FINISH?\n{sm.secs_to_end()}\nEnter Y or N\n===================\n")
        if answer in ["n","N"]:
            exit_gracefully("Session aborted - stopped with keyboard")
        elif answer in ["y","Y"]:
            print("Continuing with loop")
            continue


def exit_gracefully(exitmsg="no message provided", signum=""):
    logging.info(
        f"App exited - {exitmsg} {signum}",
    )
    
    # finish logging
    # close any open files etc
    #

    sys.exit(exitmsg)