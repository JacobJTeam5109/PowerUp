import cv2
import numpy as np
from time import time
def find_center(img):
    
    ret,thresh = cv2.threshold(img,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    center_x = []
    center_y = []
    for cnt in contours:
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        center_x.append(cx)
        center_y.append(cy)
    
    avgx= (center_x[0]+center_x[1])/2
    avgy= (center_y[0]+center_y[1])/2
    return avgx, avgy

cap = cv2.VideoCapture(0)
while(cap.isOpened()):
    
    #cur_time = time()
    
    a, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv,(5,5),0)
    hsv = cv2.bilateralFilter(hsv,9,75,75)
    
    # Threshold the HSV image to get only green colors
    range = 20
    mask = cv2.inRange(hsv, np.array([65-range,50,50]), np.array([65+range,255,255]))
    
    cv2.imshow('1', mask)
    cv2.imwrite("current_frame.png", mask)
    gray = cv2.imread("current_frame.png", 0)
    
    try:
        avgx, avgy = find_center(gray)
        print avgx
        cv2.circles(frame, (avgx, avgy), 4, (0, 0, 2555), 2)
        print "rectangele found"
        
    except:
        #print "no Rectangles found"
        pass
        
    cv2.imshow('frame',frame)
    k = cv2.waitKey(5) & 0xFF
    if k == ord('q'):
        break
    #print time()-cur_time
cv2.destroyAllWindows()
   
   
