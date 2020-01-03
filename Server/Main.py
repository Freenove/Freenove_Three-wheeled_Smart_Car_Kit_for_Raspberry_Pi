# -*- coding: utf-8 -*-
"""
 ******************************************************************************
 * File  Main.py
 * Author  Freenove (http://www.freenove.com)
 * Date    2016/11/14
 ******************************************************************************
 * Brief
 *   This is the Freenove Three-wheeled Smart Car for Raspberry Pi the Server code.
 *   Execute this file with Python2.7.
 ******************************************************************************
 * Copyright
 *   Copyright © Freenove (http://www.freenove.com)
 * License
 *   Creative Commons Attribution ShareAlike 3.0 
 *   (http://creativecommons.org/licenses/by-sa/3.0/legalcode)
 ******************************************************************************
"""
"""
Module implementing Main.

"""

from Camera_Server import *
from mTCPServer import mTCPServer


if __name__ == "__main__":
    tcp = mTCPServer()
    tcp.setDaemon(True)
    tcp.start()

    cmr_Thread = Camera_Server()
    cmr_Thread.setDaemon(True)
    cmr_Thread.start()

    tcp.join()
    cmr_Thread.join()
