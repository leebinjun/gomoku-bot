#! /usr/bin/env python  
# -*- coding: utf-8 -*-  
import sys, os
sys.path.append(os.path.dirname(__file__) + os.sep + '..\\')
import time  
from Vision import *
from Vision import classify


from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
import cv2
import time
import copy
import colorsys  

dd = 10
DD = 53
x, y = 50, 50
chessboard_info = np.zeros((9,9))
chessboard_info_green = list()
new_chessboard_info_green = list()

green_num = 0
red_num = 0

def get_dominant_color(image):  
    max_score = 0.0001  
    # dominant_color = None
    dominant_color = (200,200,200)  
    for count,(r,g,b) in image.getcolors(image.size[0]*image.size[1]):  
        # 转为HSV标准  
        saturation = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)[1]  
        y = min(abs(r*2104+g*4130+b*802+4096+131072)>>13,235)  
        y = (y-16.0)/(235-16)  
        #忽略高亮色  
        if y > 0.9:  
            continue  
        score = (saturation+0.1)*count  
        if score > max_score:  
            max_score = score  
            dominant_color = (r,g,b)  
    return dominant_color 


def get_chessboard_green(turn, while_time_threshold = 5):
    
    # 初始化
    import json # 使用json存储摄像头矫正参数 
    file_name = '.\\Config\\config.txt'
    with open(file_name) as file_obj:
        temp_d = json.load(file_obj)  # 返回列表数据，也支持字典
    mtx = np.array(temp_d['mtx'])   
    dist = np.array(temp_d['dist']) 
    # print("读取参数：", mtx， dist)    

    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    plt.ion()
    
    hand_time = 0
    temp = 0
    while_time = 0
    temp_c = classify.ColorClassify()


    while ret is True and while_time < while_time_threshold:
        while_time +=1

        ret, img = cap.read()
        # 去图像畸变  
        img = cv2.undistort(img, mtx, dist, None, mtx)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite(".\\Data\\test\\test.jpg", img)
        # TODO(binjun):此处应该转格式
        img = Image.open(".\\Data\\test\\test.jpg") 
        fig = plt.figure("gobang")
        plt.subplot(1,2,1), plt.title('origin')
        plt.imshow(img, animated= True),plt.axis('off')
        
        ax = plt.subplot(1,2,2), plt.title('result')
        plt.imshow(img),plt.axis('off')

        mos_x, mos_y = 113, 27.5  
        
        green_num = 0
        red_num = 0
         
        # pot_pos
        alist = [[72, 86], [119, 86], [163, 86], [210, 84], [255, 85], [299, 84], [343, 87], [388, 82], [434, 83], [74, 132], [120, 131], [165, 130], [210, 129], [255, 129], [300, 129], [346, 127], [390, 126], [433, 126], [75, 178], [120, 177], [166, 176], [209, 172], [256, 174], [300, 173], [346, 172], [391, 171], [437, 172], [78, 222], [120, 221], [166, 221], [211, 220], [257, 218], [303, 219], [347, 218], [392, 217], [437, 217], [77, 268], [124, 268], [169, 267], [213, 266], [257, 266], [302, 263], [347, 264], [393, 261], [435, 261], [80, 312], [125, 311], [168, 312], [213, 313], [257, 311], [304, 312], [349, 309], [392, 307], [440, 306], [78, 359], [125, 359], [170, 358], [216, 357], [259, 355], [304, 354], [350, 352], [394, 350], [440, 352], [81, 404], [128, 403], [170, 403], [217, 399], [262, 399], [305, 398], [349, 397], [394, 396], [437, 394], [84, 451], [128, 447], [172, 445], [218, 444], [264, 443], [307, 442], [350, 440], [395, 439], [439, 441]]

        temp_lenth = len(new_chessboard_info_green)
        for i in range(9):
            # pos_x = mos_x + i * DD
            for j in range(9):
                # pos_y = mos_y + j * DD
                # pos_x, pos_y = alist[i*9+j]
                pos_x, pos_y = alist[i*9+8-j]
                box=(pos_x-dd, pos_y-dd, pos_x+dd, pos_y+dd)
                roi = img.crop(box) # 获取ROI截图
                # 颜色判断
                result, temp_color = temp_c.classify(roi)
                plt.scatter(pos_x, pos_y, c = temp_color)
                if result == 2:
                    green_num += 1
                    if (i,j) not in new_chessboard_info_green:
                        new_chessboard_info_green.append((i,j))
                else:
                    if result == 1: 
                        red_num += 1
                    if (i,j) in new_chessboard_info_green:
                        new_chessboard_info_green.remove((i,j))
                chessboard_info[j][i] = result
                
        if green_num == turn:
            if abs(red_num - green_num) < 2:
                for (i, j) in new_chessboard_info_green:
                    if (i, j) not in chessboard_info_green:
                        chessboard_info_green.append((i, j))
        
        if green_num == turn and green_num - red_num == 1:
            break

        # TODO: 检验可以放在机械臂执行动作时
        # 检验 
        # for (i, j) in chessboard_info_green:
        #     if chessboard_info[i][j] != 2:
        #         if temp == 0:  new_time = while_time
        #         temp += 1
        #         if temp > 5 and while_time - new_time < 8:
        #             temp = 0
        #             chessboard_info_green.remove((i,j))
        #             while_time = new_time = 0

        # temp_a = len(new_chessboard_info_green) - temp_lenth
        # if temp_a == 0: 
        #     pass
        # elif temp_a == 1:
        #     if new_chessboard_info_green[-1] not in chessboard_info_green:
        #         chessboard_info_green.append(new_chessboard_info_green[-1])
        #     else:
        #         new_chessboard_info_green = new_chessboard_info_green[:-1]
        # else:
        #     new_chessboard_info_green = new_chessboard_info_green[:-temp_a]
        # # 检验
        # for (i, j) in chessboard_info_green[-2:]:
        #     if chessboard_info[i][j] != 2:
        #         if temp == 0:  new_time = while_time
        #         temp += 1
        #         if temp > 5 and while_time - new_time < 8:
        #             temp = 0
        #             chessboard_info_green.remove((i,j))
        #             while_time = new_time = 0

        print('chess_info:', chessboard_info_green)
        

        # chessboard_info_green2 = []
        # for i in range(9):
        #     for j in range(9):
        #         if chessboard_info[i][j] == 2 and (i, j) in chessboard_info_green:
        #             chessboard_info_green2.append((i,j))

        plt.show()
        plt.pause(0.5)
        plt.clf()

    if 1:
        print(chessboard_info_green)
        return chessboard_info_green
    
if __name__ == '__main__':
    get_chessboard_green(1, while_time_threshold=5)