
import cv2
import time
import math

p1 = 530
p2 = 300

currentX = []
currentY = []

video = cv2.VideoCapture("footvolleyball.mp4")
#load tracker 
tracker = cv2.TrackerCSRT_create()

message = input("Press enter to move to the next frame after selecting a region of interest to track. Press enter to continue. Press space to quit anytime")

#read the first frame of the video
success,img = video.read()

#selct the bounding box on the image
bbox = cv2.selectROI("tracking",img,False)

#initialise the tracker on the img and the bounding box
tracker.init(img,bbox)

#indicate the initial box with an cross
def drawBox(img,bbox):
    x , y , w , h = int(bbox[0]) , int(bbox[1]) , int(bbox[2]) , int(bbox[3])

    cv2.line(img , (x,y) , ((x+w),(y+h)), (100,200,250), 3 , 1)
    cv2.line(img , ((x+w),y) , (x,(y+h)), (100,200,250), 3 , 1)
    
    cv2.putText(img, "Tracking ball", (100,100) , cv2.FONT_HERSHEY_TRIPLEX , 0.8 , (140,70,220) ,2)

def goal_track(img,bbox):
    #get bounding box values
    x , y , w , h = int(bbox[0]) , int(bbox[1]) , int(bbox[2]) , int(bbox[3])
    
    #get the initial points and then draw a point there
    centerX = x + int(w/8)
    centerY = y + int(h/8)

    #image , center ,radius , color ,thickness
    #cv2.circle(img,(centerX,centerY),3,(90,140,254), 4) 
    #cv2.circle(img,(int(p1),int(p2)),3,(230,25,43),4)


    # image , (xStart,yStart) , (xEnd,yEnd) , color , thickness
    cv2.line(img , (centerX,centerY) , ((centerX + int(w/8)),(centerY+int(h/8))), (100,200,250), 3 )
    cv2.line(img , ((centerX+int(w/8)), centerY) , (centerX,(centerY+int(h/8))), (100,200,250), 3 )

    #Adds to the list of all the points the ball passed through
    currentX.append(centerX)
    currentY.append(centerY)

    #Draws a X at each point the ball reaches (w/8 or h/8 makes the cross smaller , adding w/4 or h/4 fixes the position to be as centered as possible)
    for point in range(len(currentX)-1):
        #cv2.circle(img,(currentX[point],currentY[point]),2,(150,150,150),5)

        cv2.line(img , (currentX[point] + int(w/4),currentY[point] + int(h/4)) , ((currentX[point] + int(3*w/8)),(currentY[point]+int(3*h/8))), (100,200,250), 3 , 1)
        cv2.line(img , ((currentX[point]+int(3*w/8)), currentY[point]+int(h/4)) , (currentX[point] + int(w/4),(currentY[point]+int(3*h/8))), (100,200,250), 3 , 1)


while True:
   checkVideo , img = video.read() 
   isSuccessful , bbox = tracker.update(img)

   if (isSuccessful):  
    drawBox(img,bbox)
    goal_track(img,bbox)
   else:
    cv2.putText(img,"Ball can't be detected",(75,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)


   cv2.imshow("Volleyball game", img)
   key = cv2.waitKey(0)
   if ( key == 32 ):
    print("Closing window")
    break

   

   
video.release()
cv2.destroyAllWindows() 