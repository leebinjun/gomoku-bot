import sys, os
sys.path.append(os.path.dirname(__file__) + os.sep + '..\\')

import serial
import time
from Seriall import com_thread

class speak_serial(com_thread.ComThread):
    def __init__(self, port = 'COM5'):
        super(speak_serial, self).__init__()
        self.port = port
    
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
    ser_lamp = speak_serial()
    temp_a = 0
    ser_lamp.start()
    while 1:
        tmp = ser_lamp.get_info()
        if tmp:
            if tmp[-1] == 1:
                print('01')
            elif tmp[-1] == 2:
                print('02')


