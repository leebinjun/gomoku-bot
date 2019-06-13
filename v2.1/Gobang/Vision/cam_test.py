import numpy
import cv2
import time

if __name__ == '__main__':
    
    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    while ret is True:
        ret, img = cap.read()
        cv2.imshow("Test0",img)
        img = img[60:420, 80:580, :]
        img = cv2.resize(img, (640,480))
        cv2.imshow("Test",img)
        ch = cv2.waitKey(1)
        if ch == ord('c') :
            break
        if ch == ord('s') :
            print("save photo")
            cv2.imwrite(".\\Data\\origin\\"+'test'+str(time.time())+'.jpg', img)
            
    cv2.destroyAllWindows()
