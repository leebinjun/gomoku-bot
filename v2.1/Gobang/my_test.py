





def servo_to_pos(servo_id, servo_pos):
    print("servo %d get to position %d" % (servo_id, servo_pos))
    low_bit  = servo_pos // 256
    high_bit = servo_pos % 256
    s_t = '%02x' % (high_bit)
    s = '55 55 08 03 01 00 00 0' + str(servo_id) + ' ' + s_t + ' 0' + str(low_bit)
    print(s)


def servos_to_pos(dict_servo):
    s = '55 55 08 03 01 00 00'
    for i in range(1,7):
        low_bit  = dict_servo[i] // 256
        high_bit = dict_servo[i] % 256
        s_t = '%02x' % (high_bit)
        s += ' 0' + str(i) + ' ' + s_t + ' 0' + str(low_bit) 
    # print("servo %d get to position %d" % (servo_id, servo_pos))
    print(s)


servo_to_pos(3, 780)
adict = {1:500, 2:500, 3:500, 4:500, 5:500, 6:500}
servos_to_pos(adict)


import math
def model_pre(x, y):
    x, y = x-(-4), y-4  #相对机械臂原点坐标
    x, y = 20*x, 20*y
    dl = math.sqrt(x**2 + y**2)
    theta6 = math.atan2(y,x)*180/math.pi
    # print(theta6)
    return dl, theta6

def model_solve(dl, dh = -80, alpha = 90):
    
    if dl < 180:
        alpha = 90
        dl = dl - 20
    else:
        alpha = 60
        dl = dl - 17
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


# dh, dl, alpha = -80, 180, 60
# print(model_solve(dl, dh, alpha))
# adict = {1:500, 2:500, 3:500, 4:500, 5:500, 6:500}
# theta3, theta4, theta5 = model_solve(dl, dh, alpha)
# adict[3], adict[4], adict[5] = int(500-theta3*100/24), int(500+theta4*100/24), int(500-theta5*100/24)
# print(adict)
# servos_to_pos(adict)


print("******************************************")

dh, dl, alpha = -50, 180, 90
# for dl in range(70,120, 5):
#     if dl < 180:
#         alpha = 90
#         dl = dl - 20
#     else:
#         alpha = 60 

#     print("dl:", dl)
#     print(model_solve(dl, dh, alpha))
dh, dl, alpha = -50, 80, 90
print(model_solve(dl, dh, alpha))
dh, dl, alpha = -75, 80, 90
print(model_solve(dl, dh, alpha))

# model_pre(0,0)

dh, dl, alpha = 200, 240, 0
print(model_solve(dl, dh, alpha))


