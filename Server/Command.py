# -*- coding: utf-8 -*-
"""
 ******************************************************************************
 * File  Command.py
 * Author  Freenove (http://www.freenove.com)
 * Date    2016/11/14
 ******************************************************************************
 * Brief
 *   This is sent by the client to the server command word
 ******************************************************************************
 * Copyright
 *   Copyright © Freenove (http://www.freenove.com)
 * License
 *   Creative Commons Attribution ShareAlike 3.0 
 *   (http://creativecommons.org/licenses/by-sa/3.0/legalcode)
 ******************************************************************************
"""

class COMMAND:
    CMD_FORWARD = ">Move Forward"
    CMD_BACKWARD = ">Move Backward"
    CMD_TURN_LEFT = ">Turn Left"
    CMD_TURN_RIGHT = ">Turn Right"
    CMD_STOP = ">Move Stop"
    CMD_TURN_CENTER = ">Turn Center"
    CMD_CAMERA_UP = ">Camera Up"
    CMD_CAMERA_DOWN = ">Camera Down"
    CMD_CAMERA_LEFT = ">Camera Left"
    CMD_CAMERA_RIGHT = ">Camera Right"
    CMD_CAMERA_STOP = ">Camera Stop"
    CMD_CAMERA_CENTER = ">Camera Center"
    
    CMD_SPEED_SLIDER = ">Speed Slider"
    CMD_DIR_SLIDER = ">Direction Slider"
    CMD_CAMERA_SLIDER = ">Camera Slider"
    
    CMD_RGB_R = ">RGB Red"
    CMD_RGB_G = ">RGB Green"
    CMD_RGB_B = ">RGB Blue"
    
    CMD_BUZZER_ALARM = ">Buzzer Alarm"
    CMD_BUZZER_STOP = ">Buzzer Stop"
    CMD_ULTRASONIC = ">Ultrasonic"
    CMD_SONIC_LEFT = CMD_CAMERA_LEFT
    CMD_SONIC_RIGHT = CMD_CAMERA_RIGHT
    def __init__(self):
        pass
