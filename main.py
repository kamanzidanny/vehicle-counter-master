import cv2
import time
import numpy as np
from time import sleep
import mysql.connector

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

seconds = 56
minutes = 59
hours = 2

def centroid_points(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

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

    seconds = seconds + 1
    time.sleep(1)
    
    if seconds == 60:
        seconds = 0
        minutes = minutes + 1

    if minutes == 60:
        minutes = 0
        hours = hours + 1

    if seconds == 25:
        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="",
          database="trafficAnalyzer"
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO statistics (road,numberOfVehicles) VALUES (%s, %s)"
        val = ("KN 123" ,cars)
        mycursor.execute(sql, val)

        mydb.commit()

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
                if ():
                    pass
                cars +=1 
                #draw a blue line
                cv2.line(frame, (25, pos_line), (1200, pos_line), (0,127,255), 3)  
                #remove a green box(contours).
                detect.remove((x,y))
                print("Detected vehicles: "+str(cars))

    print(str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2))
    
    cv2.putText(frame, "VEHICLES: "+str(cars), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)
    cv2.imshow("output" , frame)
    cv2.imshow("Detector",dilatada)

    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
cap.release()