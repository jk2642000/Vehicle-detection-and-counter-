import cv2
import numpy as np
from time import sleep

length_min=80 #length min  rectangle
height_min=80 #height min  rectangle

offset=6 #allowance of entre pixel  

post_line=550 #line position 

delay= 60 #FPS 

detect = []
counter= 0

	
def paste_centroid(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

cap = cv2.VideoCapture('video.mp4')
sub = cv2.bgsegm.createBackgroundSubtractorMOG()

while True:
    ret , frame1 = cap.read()
    temp = float(1/delay)
    sleep(temp) 
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey,(3,3),5)
    img_sub = sub.apply(blur)
    dilat = cv2.dilate(img_sub,np.ones((5,5))) # increase white region and erosion means decrease of white region 
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  #decrease of white region 
    dilatada = cv2.morphologyEx (dilat, cv2. MORPH_CLOSE , kernel) # draws outline 
    dilatada = cv2.morphologyEx (dilatada, cv2. MORPH_CLOSE , kernel)
    contorno,h=cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #rectangle ni boundry banve che by joining matrix 
    
    cv2.line(frame1, (25, post_line), (1100, post_line), (255,127,0), 3) 
    for(i,c) in enumerate(contorno):
        (x,y,w,h) = cv2.boundingRect(c)
        validar_contorno = (w >= length_min) and (h >= height_min)
        if not validar_contorno:
            continue

        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)        
        centro = paste_centroid(x, y, w, h)
        detect.append(centro)
        cv2.circle(frame1, centro, 4, (0, 0,255), -1)

        for (x,y) in detect:
            if y<(post_line+offset) and y>(post_line-offset):
                counter+=1
                cv2.line(frame1, (25, post_line), (1200, post_line), (0,127,255), 3)  
                detect.remove((x,y))
                print("car is detected : "+str(counter))        
       
    cv2.putText(frame1, "VEHICLE COUNT : "+str(counter), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)
    cv2.imshow("Video Original" , frame1)
    #cv2.imshow("Detectar",dilatada)

    if cv2.waitKey(1) == 13:
        break
    
cv2.destroyAllWindows()
cap.release()