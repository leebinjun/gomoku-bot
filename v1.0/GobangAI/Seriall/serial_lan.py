#coding=utf-8
# 语音模块

import serial

# print(serial.CR)
# b'\r'

# print(serial.LF)
# b'\n'


import threading
import time
import serial
import cv2

class ComThread:
    def __init__(self, Port='COM6'):
    #构造串口的属性
        self.l_serial = None
        self.alive = False
        self.waitEnd = None
        self.port = Port
        self.ID = None
        self.data = None
   #定义串口等待的函数
    def waiting(self):
        if not self.waitEnd is None:
            self.waitEnd.wait()

    def SetStopEvent(self):
        if not self.waitEnd is None:
            self.waitEnd.set()
        self.alive = False
        # self.stop()

    #启动串口的函数
    def start(self):
        self.l_serial = serial.Serial()
        self.l_serial.port = self.port
        self.l_serial.baudrate = 9600
        #设置等待时间，若超出这停止等待
        self.l_serial.timeout = 2
        self.l_serial.open()
        #判断串口是否已经打开
        if self.l_serial.isOpen() is not True:
            print("serial init failed.")
            exit()
    def get_info(self):
        data = ''
        data = data.encode('utf-8')                        #由于串口使用的是字节，故而要进行转码，否则串口会不识别
        n = self.l_serial.inWaiting()                      #获取接收到的数据长度
        if n: 
            #读取数据并将数据存入data
            data = data + self.l_serial.read(n)
            #输出接收到的数据
            print('get data from serial port:', data)
            return data
        else:
            return None       


if __name__ == '__main__':
    ser_lamp = ComThread()
    temp_a = 0
    ser_lamp.start()
    while 1:
        tmp = ser_lamp.get_info()
        if tmp:
            if tmp[-1] == 1:
                print('01')
            elif tmp[-1] == 2:
                print('02')


