#coding=utf-8

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
    def __init__(self, Port='COM5'):
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
    def get_ok(self):
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


    def pick_up(self):
        print("up start")
        self.l_serial.write("M280 P1 S100".encode())        # 升爪
        self.l_serial.write(serial.LF)
        self.l_serial.write(serial.CR)
        return self.get_ok()

    def pick_down(self):
        print("down start")
        self.l_serial.write("M280 P1 S160".encode())       # 落爪
        self.l_serial.write(serial.LF)
        self.l_serial.write(serial.CR)
        return self.get_ok()
        
    def pick_open(self):
        print("down start")
        self.l_serial.write("M280 P2 S80".encode())         # 松爪
        self.l_serial.write(serial.LF)
        self.l_serial.write(serial.CR)
        return self.get_ok()

    def pick_close(self):
        print("down start")
        self.l_serial.write("M280 P2 S120".encode())        # 收爪
        self.l_serial.write(serial.LF)
        self.l_serial.write(serial.CR)
        return self.get_ok()
    
    def send_gcode_g91(self):
        self.l_serial.write("G91".encode())                 # 使用相对坐标
        self.l_serial.write(serial.LF)
        self.l_serial.write(serial.CR)
        return self.get_ok()

    def send_gcode_g1(self, x, y, v):                       # 相对移动距离
        string = 'G1 X' + str(x) + ' Y' + str(y) + ' F' + str(v)
        print(string)
        self.l_serial.write(string.encode())
        self.l_serial.write(serial.LF)
        self.l_serial.write(serial.CR)
        return self.get_ok()

    def send_gcode_g1_2(self, x, y, v):                       # 相对移动距离
        string = 'G1 X' + str(x-100) + ' F' + str(v)
        print(string)
        self.l_serial.write(string.encode())
        self.l_serial.write(serial.LF)
        self.l_serial.write(serial.CR)
        time.sleep(1)
        string = 'G1 Y' + str(y-100) + ' F' + str(v)
        print(string)
        self.l_serial.write(string.encode())
        self.l_serial.write(serial.LF)
        self.l_serial.write(serial.CR)
        string = 'G1 X100 Y100 F' + str(v)
        print(string)
        self.l_serial.write(string.encode())
        self.l_serial.write(serial.LF)
        self.l_serial.write(serial.CR)
        return self.get_ok()

    def send_gcode_g1_3(self, x, y, v):                       #undo 相对移动距离
        string = 'G1 X-100 Y-100 F' + str(v)
        print(string)
        self.l_serial.write(string.encode())
        self.l_serial.write(serial.LF)
        self.l_serial.write(serial.CR)
        string = 'G1 X-' + str(x-100) + ' F' + str(v)
        print(string)
        self.l_serial.write(string.encode())
        self.l_serial.write(serial.LF)
        self.l_serial.write(serial.CR)
        time.sleep(1)
        string = 'G1 Y-' + str(y-100) + ' F' + str(v)
        print(string)
        self.l_serial.write(string.encode())
        self.l_serial.write(serial.LF)
        self.l_serial.write(serial.CR)
        
        return self.get_ok()

    def send_mov_info(self, x, y, v):
        t = int((x + y) / 300)
        self.send_gcode_g91()
        time.sleep(1)
        self.pick_open()
        time.sleep(1)
        self.pick_down()
        time.sleep(1)
        self.pick_close()
        time.sleep(1)
        self.pick_up()
        time.sleep(1)
        self.send_gcode_g1_2(x, y, v)
        time.sleep(t)
        self.pick_down()
        time.sleep(1)
        self.pick_open()
        time.sleep(1)
        self.pick_up()
        time.sleep(1)
        self.send_gcode_g1(-x, -y, v)
        time.sleep(t)
        print('ok')

    def send_undo_info(self, x, y, v):
        t = int((x + y) / 300)
        self.send_gcode_g91()
        time.sleep(1)
        self.pick_open()
        time.sleep(1)
        self.pick_up()
        time.sleep(1)
        self.send_gcode_g1(x, y, v)
        time.sleep(t)
        self.pick_down()
        time.sleep(1)
        self.pick_close()
        time.sleep(1)
        self.pick_up()
        time.sleep(1)
        self.send_gcode_g1_3(x, y, v)
        time.sleep(t)
        print('ok')
    
    def get_ready(self):
        self.pick_open()
        time.sleep(1)
        self.pick_up()
        time.sleep(1)

        


if __name__ == '__main__':
    ser_lamp = ComThread()
    temp_a = 0
    ser_lamp.start()
    while(temp_a != 99):
        temp_a = int(input('input the action:'))
        if temp_a == 1:
            ser_lamp.pick_up()
        elif temp_a == 2:
            ser_lamp.pick_down()
        elif temp_a == 3:
            ser_lamp.pick_close()
        elif temp_a == 4:
            ser_lamp.pick_open()
        elif temp_a == 5:
            x = int(input('input the x:'))
            y = int(input('input the y:'))
            v = int(input('input the v:'))
            ser_lamp.send_gcode_g1(x, y, v) 
        elif temp_a == 6:
            ser_lamp.send_mov_info(600, 800, 20000)


    # while(temp_a != 99):
        # temp_x = int(input('input the x:'))
        # temp_y = int(input('input the y:'))
        # ser_lamp.send_mov_info(100*temp_x, 100*temp_y+50, 20000)
        # temp_a = int(input('input the action:'))
        

