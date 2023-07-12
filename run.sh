#!/bin/bash

export DISPLAY=:0

export HOME=/home/pi2
export PATH=/home/pi2/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
export CONTROLLER_RUNNER_PATH=/home/pi2/Documents/battery-firmware/main


poetry run python -m battery_distributed
