#!/bin/bash
trap ctrl_c INT

function ctrl_c() {
    killall flask;
}

source /home/jobava/sandbox/2018-03-06/venv/bin/activate;

./run_server.sh &
./run_scraper.sh

trap ctrl_c EXIT

