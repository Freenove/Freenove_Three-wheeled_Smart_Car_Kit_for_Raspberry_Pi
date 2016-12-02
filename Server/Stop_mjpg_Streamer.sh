#!/bin/sh 

pid="$(pgrep mjpg_streamer)"
echo "mjpg_streamer pid: "$pid
kill -9 $pid
#kill -stop 9 $pid
#kill -s 9"$(pgrep mjpg_streamer)"
