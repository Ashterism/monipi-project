

"""Restart the Monipi Flask web service.

Useful after pulling UI/template changes on the Pi when Flask debug autoreload is off.
"""

import subprocess
import sys


SERVICE_NAME = "monipi-web.service"


def run_command(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
    )


def restart_flask_service() -> int:
    print(f"Restarting {SERVICE_NAME}...")

    restart_result = run_command(["sudo", "systemctl", "restart", SERVICE_NAME])

    if restart_result.returncode != 0:
        print("Failed to restart Flask service.")
        print(restart_result.stderr.strip())
        return restart_result.returncode

    status_result = run_command(["systemctl", "is-active", SERVICE_NAME])
    status = status_result.stdout.strip()

    if status == "active":
        print(f"{SERVICE_NAME} is active.")
        return 0

    print(f"{SERVICE_NAME} restarted, but status is: {status or 'unknown'}")
    print("Check logs with:")
    print(f"journalctl -u {SERVICE_NAME} -n 50 --no-pager")
    return 1


if __name__ == "__main__":
    sys.exit(restart_flask_service())