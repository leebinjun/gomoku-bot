from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
import cv2
import time

dd = 10
x, y = 50, 50

def on_press(event):
    x, y = event.xdata, event.ydata  
    print("my position:" ,event.button,event.xdata, event.ydata)
    # 获取鼠标点击点坐标
    box=(x-dd, y-dd, x+dd, y+dd)
    roi = img.crop(box) # 获取ROI截图
    roi.save('.\\Data\\result_cut\\'+'test'+str(time.time())+'.jpg') # 保存图片
    plt.subplot(1,2,2), plt.title('roi')
    plt.imshow(roi),plt.axis('off')
    fig.canvas.draw()


if __name__ == '__main__':

    img = Image.open('.\\Data\\result_calib\calibresult_gobangboard.png')  #打开图像
    fig = plt.figure("gobang")
    plt.subplot(1,2,1), plt.title('origin')
    plt.imshow(img, animated= True),plt.axis('off')
    
    fig.canvas.mpl_connect('button_press_event', on_press)
    plt.show()

    