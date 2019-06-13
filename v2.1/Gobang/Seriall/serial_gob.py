import sys, os
sys.path.append(os.path.dirname(__file__) + os.sep + '..\\')

import serial
import time
from Seriall import com_thread

import math
def model_pre(x, y):
    x, y = x-(-4), y-4  #相对机械臂原点坐标
    x, y = 20*x, 20*y
    dl = math.sqrt(x**2 + y**2)
    theta6 = math.atan2(y,x)*180/math.pi
    # print(theta6)
    return dl, theta6

def model_solve(dl, dh = -75, alpha = 90):
    
    if dl < 180:
        alpha = 90
        dl = dl - 20
    else:
        alpha = 60
        dl = dl - 22
        dh = dh - 10 

    # theta3, theta4, theta5 = f(dh, dl, alpha)
    l5 = 100
    l4 = 100
    l3 = 150

    l = 100
    # solve theta5
    A = dl - l3 * math.sin(math.radians(90 + alpha))
    B = dh - l3 * math.cos(math.radians(90 + alpha))
    C = A**2 + B**2    # + l5**2 - l4**2 
    a = 4 * (A**2 + B**2) * l * l
    b = -4*B*C*l
    c = C**2 - 4*A*A*l*l
    if b*b - 4*a*c <= 0:
        print("1.No solve")
        return None
    theta5 = (-b+math.sqrt(b*b -4*a*c))/2/a
    theta4 = (-b-math.sqrt(b*b -4*a*c))/2/a
    print("-_val, +_val",theta4, theta5)

    if dl >= 100:
        theta5_t = math.acos(theta5)*180/math.pi
        theta4_t = math.acos(theta4)*180/math.pi
        print("theta4, theta5",theta4_t, theta5_t)
        theta5 = min(theta4_t, theta5_t)
        theta4 = abs(theta4_t - theta5_t)
    if dl < 100:
        theta5_t = -math.acos(theta5)*180/math.pi
        theta4_t = math.acos(theta4)*180/math.pi
        print("theta4, theta5",theta4_t, theta5_t)
        theta5 = theta5_t
        theta4 = theta4_t - theta5_t

    # solve theta3
    theta3 = 90 + alpha - theta5 - theta4

    print("dl", l5*math.sin(math.radians(theta5)) + 
                l4*math.sin(math.radians(theta4+theta5)) + 
                l3*math.sin(math.radians(theta3+theta4+theta5)))
    print("dh", l5*math.cos(math.radians(theta5)) + 
                l4*math.cos(math.radians(theta4+theta5)) + 
                l3*math.cos(math.radians(theta3+theta4+theta5)))

    return theta3, theta4, theta5
    # return int(theta3), int(theta4), int(theta5)




class marlin_serial(com_thread.ComThread):
    
    def __init__(self, port = 'COM3'):
        super(marlin_serial, self).__init__()
        self.port = port
        self.dict_servo = {1:500, 2:500, 3:500, 4:500, 5:500, 6:500}

    def reset_all_servo(self):
        print("reset all servos.")
        d=bytes.fromhex('55 55 17 03 06 E8 03 01 F4 01 02 F4 01 03 F4 01 04 F4 01 05 F4 01 06 F4 01')
        self.l_serial.write(d)
        # self.l_serial.write("\x55\x55\x08\x03\x01\x00\x00\x02\xf4\x01".encode('utf-8'))
        # TODO:@libing 上面方式\xf4 解析有问题
        return self.get_ok()
    
    def to_pos1(self):
        print("get to test1 position.")
        d=bytes.fromhex('55 55 17 03 06 E8 03 01 0a 00 02 F4 01 03 5E 01 04 BC 02 05 90 02 06 F4 01')
        self.l_serial.write(d)
        return self.get_ok()
    
    def to_pos2(self):    # 摄像头观察位置
        print("get to test1 position.")
        d=bytes.fromhex('55 55 17 03 06 E8 03 01 78 00 02 FE 01 03 54 01 04 E4 02 05 12 02 06 FE 01')
        self.l_serial.write(d)
        return self.get_ok()

    def one_servo_to_pos(self, servo_id, servo_pos):
        print("servo %d get to position %d" % (servo_id, servo_pos))
        low_bit  = servo_pos // 256
        high_bit = servo_pos % 256
        s_t = '%02x' % (high_bit)
        # s = '55 55 08 03 01 00 00 0' + str(servo_id) + ' ' + s_t + ' 0' + str(low_bit)
        s = '55 55 08 03 01 00 00 0' + str(servo_id) + ' ' + s_t + ' 0' + str(low_bit)
        print(s)
        d=bytes.fromhex(s)
        self.l_serial.write(d)
        return self.get_ok()

    def servos_to_pos(self, dict_servo):
        s = '55 55 17 03 06 E8 03'
        for i in range(1,7):
            print("servo %d get to position %d" % (i, dict_servo[i]))
            low_bit  = dict_servo[i] // 256
            high_bit = dict_servo[i] % 256
            s_t = '%02x' % (high_bit)
            s += ' 0' + str(i) + ' ' + s_t + ' 0' + str(low_bit) 
        print(s)
        d=bytes.fromhex(s)
        self.l_serial.write(d)
        return self.get_ok()

    def pick_up(self, dl=115):                               # 取子
        print("pick up.")
        adict = {1:500, 2:500, 3:500, 4:500, 5:500, 6:875}
        theta3, theta4, theta5 = model_solve(dl)
        adict[3], adict[4], adict[5] = int(500-theta3*100/24), int(500+theta4*100/24), int(500-theta5*100/24)
        self.servos_to_pos(adict)
        time.sleep(2)
        self.one_servo_to_pos(servo_id=1, servo_pos=10)
        time.sleep(1)
        self.to_pos1()
        return self.get_ok()

    def pick_down(self, x=0, y=0):                                    # 落子
        print("pick down.")
        #先到达指定位置上空 dh=-50
        adict = {1:10, 2:500, 3:500, 4:500, 5:500, 6:500}
        dl, theta6 = model_pre(x, y)
        theta3, theta4, theta5 = model_solve(dl, dh=-50)
        adict[3], adict[4], adict[5], adict[6] = int(500-theta3*100/24), int(500+theta4*100/24), int(500-theta5*100/24), int(500+theta6*100/24)
        print(adict)
        self.servos_to_pos(adict)
        time.sleep(1)
        #再缓缓落下
        adict = {1:10, 2:500, 3:500, 4:500, 5:500, 6:500}
        theta3, theta4, theta5 = model_solve(dl)
        adict[3], adict[4], adict[5], adict[6] = int(500-theta3*100/24), int(500+theta4*100/24), int(500-theta5*100/24), int(500+theta6*100/24)
        print(adict)
        self.servos_to_pos(adict)
        time.sleep(2)
        #放子
        self.one_servo_to_pos(servo_id=1, servo_pos=120)
        time.sleep(1)
        #再缓缓升起
        adict = {1:10, 2:500, 3:500, 4:500, 5:500, 6:500}
        dl, theta6 = model_pre(x, y)
        theta3, theta4, theta5 = model_solve(dl, dh=-40)
        adict[3], adict[4], adict[5], adict[6] = int(500-theta3*100/24), int(500+theta4*100/24), int(500-theta5*100/24), int(500+theta6*100/24)
        print(adict)
        self.servos_to_pos(adict)
        time.sleep(2)
        #返回待命位置pos2
        self.to_pos2()
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

    
    def get_ready(self):
        self.to_pos2()

        



if __name__ == '__main__':
    ser_lamp = marlin_serial()
    temp_a = 0
    ser_lamp.start()
    while(temp_a != 99):
        temp_a = int(input('input the action:'))
        if temp_a == 1:
            ser_lamp.reset_all_servo()
        elif temp_a == 21:
            ser_lamp.to_pos1()
        elif temp_a == 22:
            ser_lamp.to_pos2()
        elif temp_a == 3:
            adict = {1:500, 2:500, 3:500, 4:500, 5:500, 6:500}
            dh = int(input('input the dh:'))
            dl = int(input('input the dl:'))
            alpha = int(input('input the angle:'))
            theta3, theta4, theta5 = model_solve(dl, dh, alpha)
            adict[3], adict[4], adict[5] = int(500-theta3*100/24), int(500+theta4*100/24), int(500-theta5*100/24)
            print(adict)
            ser_lamp.servos_to_pos(adict)
        elif temp_a == 4:
            adict = {1:500, 2:500, 3:500, 4:500, 5:500, 6:500}
            x = int(input('input the x:'))
            y = int(input('input the y:'))
            dl, theta6 = model_pre(x, y)
            theta3, theta4, theta5 = model_solve(dl)
            adict[3], adict[4], adict[5], adict[6] = int(500-theta3*100/24), int(500+theta4*100/24), int(500-theta5*100/24), int(500+theta6*100/24)
            print(adict)
            ser_lamp.servos_to_pos(adict)
        elif temp_a == 5:
            input_x = int(input('input the id:'))
            input_y = int(input('input the pos:'))
            ser_lamp.one_servo_to_pos(input_x, input_y)
        elif temp_a == 6:
            ser_lamp.pick_up()
        elif temp_a == 7:
            x = int(input('input the x:'))
            y = int(input('input the y:'))
            ser_lamp.pick_down(x, y)


    # while(temp_a != 99):
        # temp_x = int(input('input the x:'))
        # temp_y = int(input('input the y:'))
        # ser_lamp.send_mov_info(100*temp_x, 100*temp_y+50, 20000)
        # temp_a = int(input('input the action:'))
        

