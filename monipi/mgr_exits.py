import sys, logging
from .mgr_session import Sessionman

sm = Sessionman()


def pause_exit_till_loop_complete():
    answer = ""
    while answer not in ["Y", "N", "y", "n"]:
        answer = input(
            f"\n===================\nALLOW LOOP TO FINISH?\n{sm.secs_to_end()}\nEnter Y or N\n===================\n"
        )
        if answer in ["n", "N"]:
            exit_gracefully("Session aborted - stopped with keyboard")
        elif answer in ["y", "Y"]:
            # create secs to end + 1
            # update text to say ending them
            # call exit gradefully then
            print("Continuing with loop")
            continue


def exit_gracefully(exitmsg="no message provided", signum=""):
    sm.change_session_status(f"Loop terminated")
    logging.info(
        f"App exited - {exitmsg} {signum}",
    )

    sys.exit(exitmsg)
