#!/bin/sh 
#echo $0
curr_file=$0
cd "$(dirname "$curr_file")"
pwd
python2 Main.py -mnt
