import cv2
import datetime
import numpy as np
from time import sleep

# the minimum width we are going to depend on
min_width=80
# the minimum height we are going to depend on
min_height=80 

offset=6  

# position of a blue line.
pos_line=550

delay= 60 

detect = []
cars= 0

datet = datetime.datetime.now()
# current_time = str(datet.strftime("%X"))
# ref_time = str("13:12:00")
current_min = str(datet.strftime("%M"))
current_hour = str(datet.strftime("%H"))
# minute = 45

def centroid_points(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

# while str(datetime.datetime.now()) < ref_time:
# while minute < 100:
cap = cv2.VideoCapture('video.mp4')
subtractor = cv2.bgsegm.createBackgroundSubtractorMOG()

while True:

    ret , frame = cap.read()
    tempo = float(1/delay)
    sleep(tempo) 
    grey = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey,(3,3),5)
    img_sub = subtractor.apply(blur)
    dilat = cv2.dilate(img_sub,np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx (dilat, cv2. MORPH_CLOSE , kernel)
    dilatada = cv2.morphologyEx (dilatada, cv2. MORPH_CLOSE , kernel)
    
    contours,h = cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.line(frame, (25, pos_line), (1200, pos_line), (255,127,0), 3) 

    
    # if (minute == 70):
    #     break
    # minute +=1

	#start counting using enumerate() method for each countours(rectangle) of an object in the foreground
    for(i,c) in enumerate(contours):
		# get x and y cordinate, width and height of each countour.
        (x,y,w,h) = cv2.boundingRect(c)
        valid_contour = (w >= min_width) and (h >= min_height)
		#if the width and height of an object they are less than the width and height we have set we move up. 
        if not valid_contour:
            continue
		# draw a green rectangle for our valid contour
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)        
		# get the center cordinates
        center = centroid_points(x, y, w, h)
		# Assign center cordinates on detect array
        detect.append(center)
		#draw a centroid on the countours
        cv2.circle(frame, center, 4, (0, 0,255), -1)
		# loop for counting cars
        for (x,y) in detect:
		# if the object is far from our positional line(blue) we increment and then remove a green box on it.
            if y<(pos_line+offset) and y>(pos_line-offset):
                cars+=1
				#draw a blue line
                cv2.line(frame, (25, pos_line), (1200, pos_line), (0,127,255), 3)  
				#remove a green box(contours).
                detect.remove((x,y))
                print("Detected vehicles: "+str(cars))
    #display minute                
    cv2.putText(frame, current_min, (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)   
    #display hour                
    cv2.putText(frame, current_hour, (25, 190), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)   
    
    cv2.putText(frame, "VEHICLES: "+str(cars), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)
    cv2.imshow("output" , frame)
    cv2.imshow("Detector",dilatada)

    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
cap.release()
