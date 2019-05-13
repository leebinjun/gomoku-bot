import colorsys  
import PIL.Image as Image  
  
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
  
  

import colorsys  
import PIL.Image as Image  

class ColorClassify(object):

    def __init__(self):
        pass
    
    def get_dominant_color(self, image):  
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
    
    def classify(self, roi):
        image = roi.convert('RGB')  
        x, y, z = self.get_dominant_color(image)
        
        if (y-x)*(y-z) > 2500 and y > x:
            # print(x, y, z, 'green 1')
            result = 2 # 'green' 
            temp_s = 'g'   
            # plt.scatter(pos_x, pos_y, c = 'g')   
        elif x*y*z > 70*70*80 and y > 90:
            print(x, y, z, 'white 1')
            result = 0 # 'white'
            temp_s = 'k' 
            # plt.scatter(pos_x, pos_y, c = 'k') 
        elif y + z < 20 and x > y:
            print(x, y, z, 'red 1')
            result = 1 # 'red' 
            temp_s = 'r' 
            # plt.scatter(pos_x, pos_y, c = 'r') 
        elif (y-x)*(y-z) > 100 and y > x:
            # print(x, y, z, 'green 2')
            result = 2 # 'green' 
            temp_s = 'g' 
            # plt.scatter(pos_x, pos_y, c = 'g') 
        elif abs(x-y) < 10:
            print(x, y, z, 'white 2')
            result = 0 # 'white'
            temp_s = 'k' 
            # plt.scatter(pos_x, pos_y, c = 'k') 
        elif y > x:
            # print(x, y, z, 'green 3')
            result = 2 # 'green' 
            temp_s = 'g' 
            # plt.scatter(pos_x, pos_y, c = 'g') 
        else:
            print(x, y, z, 'else red')
            result = 1 # 'red'
            temp_s = 'r' 
            # plt.scatter(pos_x, pos_y, c = 'r') 
        return result, temp_s

  
if __name__ == '__main__':  
    # image = Image.open('.\\Data\\result_cut\\test1529486491.7212713.jpg')  
    # image = image.convert('RGB')  
    # print(get_dominant_color(image))  

    temp_c = ColorClassify()

    import glob
    images = glob.glob('.\\Data\\result_cut\\white\\*.jpg')
    for fname in images:
        image = Image.open(fname) 
        result, temp_color = temp_c.classify(image)
            

# if __name__ == '__main__':  
#     # image = Image.open('.\\Data\\result_cut\\test1529486491.7212713.jpg')  
#     # image = image.convert('RGB')  
#     # print(get_dominant_color(image))  

#     import glob
#     images = glob.glob('.\\Data\\result_cut\\white\\*.jpg')
#     for fname in images:
#         image = Image.open(fname) 
#         image = image.convert('RGB')  
#         (x, y, z) = get_dominant_color(image)
#         # print(get_dominant_color(image))  
#         if x*y*z > 1500000:
#             print(x, y, z, 'white')
#         elif y < 4 and z < 4:
#             print(x, y, z, 'red')
#         else:
#             print(x, y, z, 'green')
         
        




