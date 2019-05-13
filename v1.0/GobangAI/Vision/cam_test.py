import numpy
import cv2
import time

if __name__ == '__main__':
    
    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    while ret is True:
        cv2.imshow("Test",img)
        ret, img = cap.read()
        ch = cv2.waitKey(1)
        if ch == ord('c') :
            break
        if ch == ord('s') :
            print("save photo")
            cv2.imwrite(".\\Data\\origin\\"+'test'+str(time.time())+'.jpg', img)
            
    cv2.destroyAllWindows()
