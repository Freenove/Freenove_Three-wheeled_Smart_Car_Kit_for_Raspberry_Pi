#!/bin/bash

sudo kill $(ps aux | grep -m 1 "./mjpg_streamer" | awk '{ print $2 }')
sudo kill $(ps aux | grep -m 1 "python2 Main.py" | awk '{ print $2 }')
