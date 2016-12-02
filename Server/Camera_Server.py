#-*- coding: utf-8 -*-
"""
 ******************************************************************************
 * File  Camrea_Server.py
 * Author  Freenove (http://www.freenove.com)
 * Date    2016/11/14
 ******************************************************************************
 * Brief
 *   This file include  the Class Camera_Server and Stop_Camera_Server. Used for turn on/off mjpg-streamer.
 ******************************************************************************
 * Copyright
 *   Copyright © Freenove (http://www.freenove.com)
 * License
 *   Creative Commons Attribution ShareAlike 3.0 
 *   (http://creativecommons.org/licenses/by-sa/3.0/legalcode)
 ******************************************************************************
"""

import threading
import os

class Camera_Server(threading.Thread):
	def camera_Http_Server(self):
		os.system("sudo sh Start_mjpg_Streamer.sh")
		
	def run(self):
		print ".............Camera server starting ......"
		self.camera_Http_Server()
		print ".............Camera server stop..........."
		
	def stop(self):
		os.system("sudo sh Stop_mjpg_Streamer.sh")
		
class Stop_Camera_Server(threading.Thread):
	def run(self):
		os.system("sudo sh Stop_mjpg_Streamer.sh")

