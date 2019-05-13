from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
import cv2
import time

import colorsys  
  
dd = 10
x, y = 50, 50
alist = [[118, 54], [163, 51], [211, 45], [261, 44], [315, 40], [364, 37], [417, 35], [468, 31], [520, 29], [119, 102], [166, 99], [214, 96], [263, 93], [316, 92], [366, 89], [418, 87], [471, 81], [525, 79], [121, 150], [167, 150], [218, 147], [264, 143], [318, 142], [369, 138], [423, 136], [475, 134], [526, 130], [122, 200], [168, 200], [219, 198], [268, 194], [319, 192], [372, 191], [423, 187], [478, 183], [531, 182], [123, 251], [171, 247], [221, 245], [270, 245], [322, 242], [374, 241], [427, 239], [479, 238], [532, 234], [123, 301], [173, 297], [222, 297], [273, 296], [325, 295], [376, 291], [428, 291], [482, 288], [536, 289], [127, 351], [173, 350], [223, 349], [274, 345], [326, 345], [377, 343], [430, 342], [483, 341], [537, 338], [127, 401], [174, 399], [225, 399], [275, 399], [329, 396], [379, 397], [431, 394], [486, 395], [540, 393], [129, 448], [176, 447], [226, 448], [276, 448], [328, 448], [381, 445], [433, 446], [486, 445], [541, 444]]
# res = []
# for i in alist:
#     x, y = i
#     res.append([int(x), int(y)])
# print(res)

def on_press(event):
    x, y = event.xdata, event.ydata  
    print("my position:" ,event.button,event.xdata, event.ydata)
    # 获取鼠标点击点坐标
    # if x != None and y != None:
    #     alist.append([int(x), int(y)])
    # print(alist)

    mos_x, mos_y = 113, 27.5  

    plt.subplot(1,2,2), plt.title('result')
    plt.imshow(img, animated= True),plt.axis('off')
    
    for i in range(9):
        for j in range(9):
            if i*8+j <= len(alist):
                for _ in alist:
                    x, y = _
                    plt.scatter(x, y)
            else:
                break
        break

    fig.canvas.draw()


if __name__ == '__main__':

    img = Image.open('.\\Data\\result_calib\calibresult_gobangboard_new.png')  #打开图像
    fig = plt.figure("gobang")
    plt.subplot(1,2,1), plt.title('origin')
    plt.imshow(img, animated= True),plt.axis('off')
    

    fig.canvas.mpl_connect('button_press_event', on_press)
    plt.show()






    