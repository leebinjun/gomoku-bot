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


def get_chessboard_green(turn, while_time_threshold = 1):

    # 初始化
    import json # 使用json存储摄像头矫正参数
    file_name = '.\\Config\\config.txt'
    with open(file_name) as file_obj:
        temp_d = json.load(file_obj)  # 返回列表数据，也支持字典
    mtx = np.array(temp_d['mtx'])
    dist = np.array(temp_d['dist'])
    # print("读取参数：", mtx， dist)

    cap = cv2.VideoCapture(0)

    cap.set(3,640)
    cap.set(4, 480)

    ret,img = cap.read()
    img = img[60:420, 80:580, :]
    img = cv2.resize(img, (640,480))
    plt.ion()

    hand_time = 0
    temp = 0
    while_time = 0


    while ret is True and while_time < while_time_threshold:
        while_time +=1

        ret, img = cap.read()
        img = img[60:420, 80:580, :]
        img = cv2.resize(img, (640,480))
        # 去图像畸变
        # img = cv2.undistort(img, mtx, dist, None, mtx)
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
        alist = [[104, 59], [145, 59], [186, 59], [227, 59], [268, 59],
                 [309, 59], [350, 59], [391, 59], [432, 59], [104, 102],
                 [145, 102], [186, 102], [227, 102], [268, 102], [309, 102],
                 [350, 102], [391, 102], [432, 102], [104, 145], [145, 145],
                 [186, 145], [227, 145], [268, 145], [309, 145], [350, 145],
                 [391, 145], [432, 145], [104, 188], [145, 188], [186, 188],
                 [227, 188], [268, 188], [309, 188], [350, 188], [391, 188],
                 [432, 188], [104, 231], [145, 231], [186, 231], [227, 231],
                 [268, 231], [309, 231], [350, 231], [391, 231], [432, 231],
                 [104, 274], [145, 274], [186, 274], [227, 274], [268, 274],
                 [309, 274], [350, 274], [391, 274], [432, 274], [104, 317],
                 [145, 317], [186, 317], [227, 317], [268, 317], [309, 317],
                 [350, 317], [391, 317], [432, 317], [104, 360], [145, 360],
                 [186, 360], [227, 360], [268, 360], [309, 360], [350, 360],
                 [391, 360], [432, 360], [104, 403], [145, 403], [186, 403],
                 [227, 403], [268, 403], [309, 403], [350, 403], [391, 403],
                 [432, 403]]

        temp_lenth = len(new_chessboard_info_green)
        time_start = time.time()
        temp_c = classify.Classify()
        for i in range(9):
            # pos_x = mos_x + i * DD
            for j in range(9):
                # pos_y = mos_y + j * DD
                # pos_x, pos_y = alist[i*9+j]
                pos_x, pos_y = alist[i*9+8-j]
                box=(pos_x-dd, pos_y-dd, pos_x+dd, pos_y+dd)
                roi = img.crop(box) # 获取ROI截图
                # 颜色判断
                #result, temp_color = temp_c.classify(roi)
                roi.save('.\\Data\\result_cut\\' + 'test' + str(i+1) + str(j+1) +'.jpg')  # 保存图片
                result, temp_color = temp_c.chessidentify('.\\Data\\result_cut\\' +
                                                      'test' + str(i + 1) +
                                                      str(j + 1) + '.jpg')
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
        time_end = time.time()
        print('totally cost', time_end - time_start)

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