#-*- coding: utf-8 -*-
########################################################################
# Filename    : mDev.py
# Description : This is the Class mDev. Used for Control the Shield.
# auther      : www.freenove.com
# modification: 2020/03/26
########################################################################
import smbus
import time
import threading
from threading import Lock

def numMap(value,fromLow,fromHigh,toLow,toHigh):
    return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow

class mDEV:
    CMD_SERVO1      =   0
    CMD_SERVO2      =   1
    CMD_SERVO3      =   2
    CMD_SERVO4      =   3
    CMD_PWM1        =   4
    CMD_PWM2        =   5
    CMD_DIR1        =   6
    CMD_DIR2        =   7
    CMD_BUZZER      =   8
    CMD_IO1         =   9
    CMD_IO2         =   10
    CMD_IO3         =   11
    CMD_SONIC       =   12
    SERVO_MAX_PULSE_WIDTH = 2500
    SERVO_MIN_PULSE_WIDTH = 500
    SONIC_MAX_HIGH_BYTE = 50
    Is_IO1_State_True = False
    Is_IO2_State_True = False
    Is_IO3_State_True = False
    Is_Buzzer_State_True = False
    handle = True
    mutex = Lock()
    def __init__(self,addr=0x18):
        self.address = addr #default address of mDEV
        self.bus=smbus.SMBus(1)
        self.bus.open(1)
    def i2cRead(self,reg):
        self.bus.read_byte_data(self.address,reg)
        
    def i2cWrite1(self,cmd,value):
        self.bus.write_byte_data(self.address,cmd,value)
        
    def i2cWrite2(self,value):
        self.bus.write_byte(self.address,value)
    
    def writeReg(self,cmd,value):
        try:
            value = int(value)
            #print(value,type(value))
            self.bus.write_i2c_block_data(self.address,cmd,[value>>8,value&0xff])
            time.sleep(0.001)
            self.bus.write_i2c_block_data(self.address,cmd,[value>>8,value&0xff])
            time.sleep(0.001)
            self.bus.write_i2c_block_data(self.address,cmd,[value>>8,value&0xff])
            time.sleep(0.001)
        except Exception as e:
            print(Exception,"I2C Error :",e)
        
    def readReg(self,cmd):      
        ##################################################################################################
        #Due to the update of SMBus, the communication between Pi and the shield board is not normal. 
        #through the following code to improve the success rate of communication.
        #But if there are conditions, the best solution is to update the firmware of the shield board.
        ##################################################################################################
        for i in range(0,10,1):
            self.bus.write_i2c_block_data(self.address,cmd,[0])
            a = self.bus.read_i2c_block_data(self.address,cmd,1)
            
            self.bus.write_byte(self.address,cmd+1)
            b = self.bus.read_i2c_block_data(self.address,cmd+1,1)
            
            self.bus.write_byte(self.address,cmd)
            c = self.bus.read_byte_data(self.address,cmd)
            
            self.bus.write_byte(self.address,cmd+1)
            d = self.bus.read_byte_data(self.address,cmd+1)
            #print i,a,b,c,d
            #'''
            if(a[0] == c and c < self.SONIC_MAX_HIGH_BYTE ): #and b[0] == d
                return c<<8 | d
            else:
                continue
            #'''
            '''
            if (a[0] == c and c < self.SONIC_MAX_HIGH_BYTE) :
                return c<<8 | d
            elif (a[0] > c and c < self.SONIC_MAX_HIGH_BYTE) :
                return c<<8 | d
            elif (a[0] < c and a[0] < self.SONIC_MAX_HIGH_BYTE) :
                return a[0]<<8 | b[0]
            else :
                continue
            '''
        return 0
        #################################################################################################
        #################################Old codes#######################################################
        #[a,b]=self.bus.read_i2c_block_data(self.address,cmd,2)
        #print "a,b",[a,b]
        #return a<<8 | b
        #################################################################################################
    def move(self,left_pwm,right_pwm,steering_angle=90):
        self.setServo('1',steering_angle)
        if left_pwm>0:
            mdev.writeReg(mdev.CMD_DIR2,1)
            mdev.writeReg(mdev.CMD_PWM2,left_pwm)
        else:
            mdev.writeReg(mdev.CMD_DIR2,0)
            mdev.writeReg(mdev.CMD_PWM2,abs(left_pwm))
        if right_pwm>0:
            mdev.writeReg(mdev.CMD_DIR1,1)
            mdev.writeReg(mdev.CMD_PWM1,right_pwm)
        else:
            mdev.writeReg(mdev.CMD_DIR1,0)
            mdev.writeReg(mdev.CMD_PWM1,abs(right_pwm))
        
    def setServo(self,index,angle):
        angle=numMap(angle,0,180,500,2500)
        if index=="1":
            self.writeReg(mdev.CMD_SERVO1,angle)
        elif index=="2":
            self.writeReg(mdev.CMD_SERVO2,angle)
        elif index=="3":
            self.writeReg(mdev.CMD_SERVO3,angle)
        elif index=="4":
            self.writeReg(mdev.CMD_SERVO4,angle)
            
    def setLed(self,R,G,B):
        if R==1:
            mdev.writeReg(mdev.CMD_IO1,0)
        else:
            mdev.writeReg(mdev.CMD_IO1,1)
        if G==1:
            mdev.writeReg(mdev.CMD_IO2,0)
        else:
            mdev.writeReg(mdev.CMD_IO2,1)
        if B==1:
            mdev.writeReg(mdev.CMD_IO3,0)
        else:
            mdev.writeReg(mdev.CMD_IO3,1)
    def setBuzzer(self,PWM):
        mdev.writeReg(mdev.CMD_BUZZER,PWM)
    def getSonicEchoTime():
        SonicEchoTime = mdev.readReg(mdev.CMD_SONIC)
        return SonicEchoTime
        
    def getSonic(self):
        SonicEchoTime = mdev.readReg(mdev.CMD_SONIC)
        distance = SonicEchoTime * 17.0 / 1000.0
        return distance
    def setShieldI2cAddress(self,addr): #addr: 7bit I2C Device Address 
        if (addr<0x03) or (addr > 0x77) :
            return 
        else :
            mdev.writeReg(0xaa,(0xbb<<8)|(addr<<1))
            
mdev = mDEV()   
def loop(): 
    mdev.readReg(mdev.CMD_SONIC)
    while True:
        SonicEchoTime = mdev.readReg(mdev.CMD_SONIC)
        distance = SonicEchoTime * 17.0 / 1000.0
        print("EchoTime: %d, Sonic: %.2f cm"%(SonicEchoTime,distance))
        time.sleep(0.001)
    
if __name__ == '__main__':
    import sys
    print("mDev.py is starting ... ")
    #setup()
    try:
        if len(sys.argv)<2:
            print("Parameter error: Please assign the device")
            exit() 
        print(sys.argv[0],sys.argv[1])
        if sys.argv[1] == "servo":      
            cnt = 3 
            while (cnt != 0):       
                cnt = cnt - 1
                for i in range(50,140,1):   
                    mdev.writeReg(mdev.CMD_SERVO1,numMap(i,0,180,500,2500))
                    time.sleep(0.005)
                for i in range(140,50,-1):  
                    mdev.writeReg(mdev.CMD_SERVO1,numMap(i,0,180,500,2500))
                    time.sleep(0.005)
            mdev.writeReg(mdev.CMD_SERVO1,numMap(90,0,180,500,2500))
        if sys.argv[1] == "buzzer":
            mdev.writeReg(mdev.CMD_BUZZER,2000)
            time.sleep(3)
            mdev.writeReg(mdev.CMD_BUZZER,0)
        if sys.argv[1] == "RGBLED":
            for i in range(0,3):
                mdev.writeReg(mdev.CMD_IO1,0)
                mdev.writeReg(mdev.CMD_IO2,1)
                mdev.writeReg(mdev.CMD_IO3,1)
                time.sleep(1)
                mdev.writeReg(mdev.CMD_IO1,1)
                mdev.writeReg(mdev.CMD_IO2,0)
                mdev.writeReg(mdev.CMD_IO3,1)
                time.sleep(1)
                mdev.writeReg(mdev.CMD_IO1,1)
                mdev.writeReg(mdev.CMD_IO2,1)
                mdev.writeReg(mdev.CMD_IO3,0)
                time.sleep(1)
            mdev.writeReg(mdev.CMD_IO1,1)
            mdev.writeReg(mdev.CMD_IO2,1)
            mdev.writeReg(mdev.CMD_IO3,1)
        if sys.argv[1] == "ultrasonic" or sys.argv[1] == "s":
            while True:
                print("Sonic: ",mdev.getSonic())
                time.sleep(0.1)
        if sys.argv[1] == "motor":
                mdev.writeReg(mdev.CMD_DIR1,0)
                mdev.writeReg(mdev.CMD_DIR2,0)
                for i in range(0,1000,10):  
                    mdev.writeReg(mdev.CMD_PWM1,i)
                    mdev.writeReg(mdev.CMD_PWM2,i)
                    time.sleep(0.005)
                time.sleep(1)
                for i in range(1000,0,-10): 
                    mdev.writeReg(mdev.CMD_PWM1,i)
                    mdev.writeReg(mdev.CMD_PWM2,i)
                    time.sleep(0.005)
                mdev.writeReg(mdev.CMD_DIR1,1)
                mdev.writeReg(mdev.CMD_DIR2,1)
                for i in range(0,1000,10):  
                    mdev.writeReg(mdev.CMD_PWM1,i)
                    mdev.writeReg(mdev.CMD_PWM2,i)
                    time.sleep(0.005)
                time.sleep(1)
                for i in range(1000,0,-10): 
                    mdev.writeReg(mdev.CMD_PWM1,i)
                    mdev.writeReg(mdev.CMD_PWM2,i)
                    time.sleep(0.005)
    except KeyboardInterrupt:
        pass    
