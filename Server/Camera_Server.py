#-*- coding: utf-8 -*-
########################################################################
# Filename    : Camrea_Server.py
# Description : This file include  the Class Camera_Server and Stop_Camera_Server.
#               Used for turn on/off mjpg-streamer.
# auther      : www.freenove.com
# modification: 2020/03/26
########################################################################
import threading
import os

class Camera_Server(threading.Thread):
    def camera_Http_Server(self):
        os.system("sudo sh Start_mjpg_Streamer.sh")
        
    def run(self):
        print(".............Camera server starting ......")
        self.camera_Http_Server()
        print(".............Camera server stop...........")
        
    def stop(self):
        os.system("sudo sh Stop_mjpg_Streamer.sh")
        
class Stop_Camera_Server(threading.Thread):
    def run(self):
        os.system("sudo sh Stop_mjpg_Streamer.sh")

