##############################################################################
Chapter Part of the Code
##############################################################################

If you have any concerns, please feel free to contact us via support@freenove.com

In this chapter, we will explain the working principle and the key code of the whole project.

Server and Client 
******************************

Server
===============================

The server is working on the RPi, and provides mjpg-streamer service and TCP service. And mjpg-streamer is for the transmission of camera data, TCP service for the transfer of the command.

mjpg-streamer
-------------------------------

In the Camera_Server.py under "Server" folder, define a class Camera_Server, which inherits from the class threading.Thread. So when method .start () is called, Shell script file "Start_mjpg_Streamer.sh" is called, then the mjpg-streamer service is opened in a new thread. After mjpg-streamer starts, when the end signal (Ctrl-C, Ctrl-\, etc.) is received, it will exit, the thread will end.

Class Stop_Camera_Server is used to close the mjpg-streamer service. The class calls the Shell script file "Stop_mjpg_Streamer.sh" in a new thread, obtains the pid of the mjpg-streamer process, and then sends the end signal to end the service. And then the two threads will end.

Camera_Server.py

.. literalinclude:: ../../../freenove_Kit/Server/Camera_Server.py
    :linenos: 
    :language: python
    :dedent:

About the command for opening “mjpg-streamer”, you can open the file “Start_mjpg_Streamer.sh” to view.

.. literalinclude:: ../../../freenove_Kit/Server/Start_mjpg_Streamer.sh
    :linenos: 
    :language: sh
    :dedent:

The meaning of the option parameters is as follows:

"-i", means the video input method, where the "input_uvc.so" is the input mode of USB Video Class (uvc).

The parameters can be specified as below:

.. code-block:: text

    [-d | --device ].......: video device to open (your camera)
    [-r | --resolution ]...: the resolution of the video device,
                            can be one of the following strings:
                            QSIF QCIF CGA QVGA CIF VGA 
                            SVGA XGA SXGA 
                            or a custom value like the following
                            example: 640x480
    [-f | --fps ]..........: frames per second
    [-y | --yuv ]..........: enable YUYV format and disable MJPEG mode
    [-q | --quality ]......: JPEG compression quality in percent 
                            (activates YUYV format, disables MJPEG)
    [-m | --minimum_size ].: drop frames smaller then this limit, useful
                            if the webcam produces small-sized garbage frames
                            may happen under low light conditions
    [-n | --no_dynctrl ]...: do not initalize dynctrls of Linux-UVC driver
    [-l | --led ]..........: switch the LED "on", "off", let it "blink" or leave
                            it up to the driver using the value "auto"

"-o" means the video output method, where the "output_http.so" is used. The parameters can be specified as below:

.. code-block:: text

    [-w | --www ]...........: folder that contains webpages in 
                              flat hierarchy (no subfolders)
    [-p | --port ]..........: TCP port for this HTTP server
    [-c | --credentials ]...: ask for "username:password" on connect
    [-n | --nocommands ]....: disable execution of commands

The following is the file "Stop_mjpg_Streamer.sh", in which the pid of "mjpg_streamer" process is obtained, and then the kill command is used to end the process.

.. literalinclude:: ../../../freenove_Kit/Server/Stop_mjpg_Streamer.sh
    :linenos: 
    :language: sh
    :dedent:

TCP
---------------------------

In the mTCPServer.py under folder "Server", define a class mTCPServer, which is used to create a TCP monitor port, and, to forward the commands to Shield after receiving request from the client. Because the monitor port function is also blocked, it will be created in a new thread. You can open file mTCPServer.py to view the details.

mDEV
--------------------------

In the mDev.py under folder "Server", define class mDEV, which contains the control commands and methods for Shield. The following is the content of class mDEV.

.. literalinclude:: ../../../freenove_Kit/Server/mDev.py
    :linenos: 
    :language: python
    :dedent:

The following table is corresponding Shield interface of the command. You can operate them through the member function writeReg and readReg.

+------------+-----------------+------------+-------------+
|  Command   |    Interface    | Read/Write | Valid value |
+============+=================+============+=============+
| CMD_SERVO1 | Servo1          | W          | 0-20000     |
+------------+-----------------+------------+-------------+
| CMD_SERVO2 | Servo2          | W          | 0-20000     |
+------------+-----------------+------------+-------------+
| CMD_SERVO3 | Servo3          | W          | 0-20000     |
+------------+-----------------+------------+-------------+
| CMD_SERVO4 | Servo4          | W          | 0-20000     |
+------------+-----------------+------------+-------------+
| CMD_PWM1   | Motor1 Speed    | W          | 0-1000      |
+------------+-----------------+------------+-------------+
| CMD_PWM2   | Motor2 Speed    | W          | 0-1000      |
+------------+-----------------+------------+-------------+
| CMD_DIR1   | Motor1 Steering | W          | 0 or non-0  |
+------------+-----------------+------------+-------------+
| CMD_DIR2   | Motor2 Steering | W          | 0 or non-0  |
+------------+-----------------+------------+-------------+
| CMD_BUZZER | Buzzer          | W          | 0-65535     |
+------------+-----------------+------------+-------------+
| CMD_IO1    | IO1             | W          | 0 or non-0  |
+------------+-----------------+------------+-------------+
| CMD_IO2    | IO2             | W          | 0 or non-0  |
+------------+-----------------+------------+-------------+
| CMD_IO3    | IO3             | W          | 0 or non-0  |
+------------+-----------------+------------+-------------+
| CMD_SONIC  | TRIG/ECHO       | R                        |
+------------+-----------------+--------------------------+

Default I2C address of the Shield is 0x18 (7bit). Member function setShieldI2cAddress (self, addr) is used to modify the I2C address of Shield. Don't change its address unless it conflicts with the I2C address of your other device. Because detection range of the I2CTool is 0x03-0x77, so the range of parameter “addr” is limited to 0x03-0x77. It is invalid when beyond this range. When the I2C address is modified, the Shield need to be restarted. when there is a need, change the parameter addr of the class constructor to the new I2C address to facilitate use later. Please use this function with caution.

.. code-block:: python

    def __init__(self,addr=0x18):
    ......
    def setShieldI2cAddress(self,addr): #addr: 7bit I2C Device Address 
        if (addr<0x03) or (addr > 0x77) :
            return 
        else :
            mdev.writeReg(0xaa,(0xbb<<8)|(addr<<1))

Client 
========================

Connect the Client to the server through the TCP port. Then define class TCPClient in the TCPClient.py under "Client" folder, which contains the method for connecting to server and sending data.

.. literalinclude:: ../../../freenove_Kit/Server/mDev.py
    :linenos: 
    :language: python
    :dedent:

In “main.py”, monitor the action of the control and keyboard, and send a command to the server.

View “main.py” for detailed information.

In “Config.txt”, preserve the IP address of successful connection to the server last time, and load it the next time start the client. This enables you to connect to the server quickly without entering the IP address of the server in the edit box each time.