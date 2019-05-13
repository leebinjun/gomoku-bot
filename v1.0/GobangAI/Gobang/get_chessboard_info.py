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


def get_chessboard_green(turn = 0):
    
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


    while ret is True and while_time < 5:
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
        alist = [[118, 54], [163, 51], [211, 45], [261, 44], [315, 40], [364, 37], [417, 35], [468, 31], [520, 29], [119, 102], [166, 99], [214, 96], [263, 93], [316, 92], [366, 89], [418, 87], [471, 81], [525, 79], [121, 150], [167, 150], [218, 147], [264, 143], [318, 142], [369, 138], [423, 136], [475, 134], [526, 130], [122, 200], [168, 200], [219, 198], [268, 194], [319, 192], [372, 191], [423, 187], [478, 183], [531, 182], [123, 251], [171, 247], [221, 245], [270, 245], [322, 242], [374, 241], [427, 239], [479, 238], [532, 234], [123, 301], [173, 297], [222, 297], [273, 296], [325, 295], [376, 291], [428, 291], [482, 288], [536, 289], [127, 351], [173, 350], [223, 349], [274, 345], [326, 345], [377, 343], [430, 342], [483, 341], [537, 338], [127, 401], [174, 399], [225, 399], [275, 399], [329, 396], [379, 397], [431, 394], [486, 395], [540, 393], [129, 448], [176, 447], [226, 448], [276, 448], [328, 448], [381, 445], [433, 446], [486, 445], [541, 444]]

        temp_lenth = len(new_chessboard_info_green)
        for i in range(9):
            # pos_x = mos_x + i * DD
            for j in range(9):
                # pos_y = mos_y + j * DD
                pos_x, pos_y = alist[i*9+j]
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
    get_chessboard_green()