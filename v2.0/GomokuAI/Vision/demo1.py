from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
import cv2
import time

import colorsys  
  
def get_dominant_color(image):  
    max_score = 0.0001  
    dominant_color = None  
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

dd = 10
x, y = 50, 50

def on_press(event):
    x, y = event.xdata, event.ydata  
    print("my position:" ,event.button,event.xdata, event.ydata)
    # 获取鼠标点击点坐标
    box=(x-dd, y-dd, x+dd, y+dd)
    roi = img.crop(box) # 获取ROI截图
    roi.save('.\\Data\\result_cut\\'+'test'+str(time.time())+'.jpg') # 保存图片
    # 颜色判断
    image = roi.convert('RGB')  
    x, y, z = get_dominant_color(image)
    if x*y*z > 1500000:
        print(x, y, z, 'white')
        result = 'white' 
    elif y < 4 and z < 4:
        print(x, y, z, 'red')
        result = 'red' 
    else:
        print(x, y, z, 'green')
        result = 'green' 
    plt.subplot(1,2,2), plt.title(result)
    plt.imshow(roi),plt.axis('off')

    fig.canvas.draw()


if __name__ == '__main__':

    img = Image.open('.\\Data\\result_calib\calibresult_gobangboard_new.png')  #打开图像
    fig = plt.figure("gobang")
    plt.subplot(1,2,1), plt.title('origin')
    plt.imshow(img, animated= True),plt.axis('off')
    
    fig.canvas.mpl_connect('button_press_event', on_press)
    plt.show()

    