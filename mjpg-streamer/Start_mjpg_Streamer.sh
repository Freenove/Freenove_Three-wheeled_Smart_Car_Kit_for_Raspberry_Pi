#!/bin/sh 
#echo $0
curr_file=$0
cd "$(dirname "$curr_file")"
#pwd
#./mjpg_streamer -i "./input_uvc.so -y -d /dev/video0 -r 320*240 -f 12" -o "./output_http.so -p 8090 -w ./www"
./mjpg_streamer -i "./input_uvc.so -y -d /dev/video0 -n -r 320*240 -f 30" -o "./output_http.so -p 8090 -w ./www"

