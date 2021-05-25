
import cv2
import numpy as np
from time import sleep 
import Singularity_supplementary as ss

def self_drive():

    feed = cv2.VideoCapture(ss.path)
        
    while True:

        ret, frame = feed.read()
            
        if(not ret):
            feed = cv2.VideoCapture(ss.path)
            continue

        hsv1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        	
        yel_lb = ss.lower_colour_bound
        yel_ub = ss.upper_colour_bound
        yel_mask = cv2.inRange(hsv1, yel_lb, yel_ub)

        kernel=np.ones((120,120),"uint8")

        ret,thresh1 = cv2.threshold(yel_mask,127,255,0)

        #dilation and filtering- 
        #yellow
        yel_mask = cv2.dilate(yel_mask,kernel)
        res_yel = cv2.bitwise_and(frame,frame,mask=yel_mask)
        #contour to track yellow color goes below- 
        contours, hierarchy = cv2.findContours(yel_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)       
            
        for current_contour in contours:

            M = cv2.moments(thresh1)

            if(2>1): # didn't wanna remove and indent

                
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                
                else:
                    cx, cy = 0, 0

                if(cx <= ss.left_lane_threshold):
                    sleep(ss.sleep_val)
                    print("Go right since centroid's X-Co-ordinate:",cx)

                elif(cx >= ss.right_lane_threshold):
                    sleep(ss.sleep_val)
                    print("Go Left since centroid's X-Co-ordinate:",cx)

                else:
                    sleep(ss.sleep_val)
                    print("Go Forward since centroid's X-Co-ordinate:",cx)   

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > ss.min_area_filtered):
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x, y),(x + w, y + h),(0,0,255), 4)
                cv2.putText(frame, "PATH", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0,0,255)) # showing the highlighted rectangle
                cv2.circle(frame,(cx,cy),5,(0,255,0),-1)
                cv2.putText(yel_mask, "CTR", (cx - 25, cy - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        		
        cv2.imshow(ss.Frame_name, frame)
        cv2.imshow(ss.Mask_Frame_name,yel_mask)
            
        if(cv2.waitKey(1)==ss.kill_key_val):
            break
                
    feed.release()
    cv2.destroyAllWindows()
    print(ss.end_msg)
    print("")

    go_again = input("Would you like to run it again ? (y/n)\n")
    if(go_again == 'y'):
        terminal_front()
    else:
        exit()


  
def terminal_front():
    print("Welcome to the Singularity Software")
    print("***********************************")
    print("")
    read_docs = input("Do you want to read the documentation as well as run ? (y/n) \n")
    if(read_docs=='y'):
        print("")
        ss.docs()

        print("")
        self_drive()
        print("")

              
    else:
        print("")
        print("Running without loading docs")
        print("")
        self_drive()
        
terminal_front()




