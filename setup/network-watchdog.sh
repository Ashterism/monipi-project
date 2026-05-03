#!/usr/bin/env bash

set -u

DEVICE="wlan0"
LOG_TAG="network-watchdog"

STATE=$(nmcli -t -f DEVICE,STATE device | awk -F: -v device="$DEVICE" '$1 == device {print $2}')

if [ "$STATE" = "connected" ]; then
    logger -t "$LOG_TAG" "$DEVICE is connected; no action needed"
    exit 0
fi

logger -t "$LOG_TAG" "$DEVICE state is '$STATE'; restarting NetworkManager"
systemctl restart NetworkManager