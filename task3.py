import numpy as np
import cv2
from time import sleep
import Singularity_supplementary as ss

is_running = 0
area_r = 301
area_y = 301

def vid_capt():					 		# TO FIX - I think blue and yellow HSV values are overlapping, modify it
	global is_running
	global area_r
	global area_y

	feed = cv2.VideoCapture(0)

	while(True):
		#_,frame = feed.read()
		is_running = 1

		ret,frame=feed.read()

		hsv1=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

		red_lb = np.array([136,87,111],np.uint8)
		red_ub = np.array([180,255,255],np.uint8)
		red_mask= cv2.inRange(hsv1,red_lb,red_ub)	#ub- upper bound, lb- lower bound

		yel_lb = np.array([20,100,100],np.uint8)
		yel_ub = np.array([30,255,255],np.uint8)
		yel_mask = cv2.inRange(hsv1,yel_lb,yel_ub) # same same 

		kernel=np.ones((80,80),"uint8")

		ret,thresh1 = cv2.threshold(yel_mask,127,255,0)
		ret,thresh2 = cv2.threshold(red_mask,127,255,0)

		#dilation effects go below- 

		#red
		red_mask = cv2.dilate(red_mask,kernel)
		res_red = cv2.bitwise_and(frame,frame,mask=red_mask)
		#contour to track red color goes below- 
		contours_red, hierarchy = cv2.findContours(red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		for pic, contour in enumerate(contours_red):
			area_r = cv2.contourArea(contour)
			if(area_r > 1500):
                                
				#red_is_present = 'True' # means that the robot is detecting the ball
                                
				x, y, w, h = cv2.boundingRect(contour)
				frame = cv2.rectangle(frame, (x, y),(x + w, y + h),(0, 0, 255), 2)
				cv2.putText(frame, "RED", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0, 0, 255))
				
		
		#yellow
		yel_mask = cv2.dilate(yel_mask,kernel)
		res_yel = cv2.bitwise_and(frame,frame,mask=yel_mask)
		#contour to track yel color goes below- 
		contours_yel, hierarchy = cv2.findContours(yel_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		for pic, contour in enumerate(contours_yel):
			area_y = cv2.contourArea(contour)
			if(area_y > 300):
				x, y, w, h = cv2.boundingRect(contour)
				frame = cv2.rectangle(frame, (x, y),(x + w, y + h),(20, 100, 100), 2)
				cv2.putText(frame, "YELLOW", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(20, 100, 100))

		if(area_r > area_y): # this means that the red ball is there
                        
			for current_contour in contours_yel,contours_red:
				M = cv2.moments(thresh2)
			
				if M["m00"] != 0:
					cx = int(M["m10"] / M["m00"])
					cy = int(M["m01"] / M["m00"])
				else:
					cx = 0
					cy = 0

				if(cx <= ss.red_left_path_threshold):
					sleep(ss.sleep_val)
					print("Ball__Go left since centroid's X-Co-ordinate:",cx)
				elif(cx >= ss.red_right_path_threshold):
					sleep(ss.sleep_val)
					print("Ball__Go right since centroid's X-Co-ordinate:",cx)
				else:
					sleep(ss.sleep_val)
					print("Ball__Go Forward since centroid's X-Co-ordinate:",cx)

		elif(area_r < area_y): # means that there is no red in the frame or just minimal red noise 
                        
			for current_contour in contours_red,contours_yel:
				M = cv2.moments(thresh1)

				if M["m00"] != 0:
					cx = int(M["m10"] / M["m00"])
					cy = int(M["m01"] / M["m00"])
                
				else:
					cx, cy = 0, 0

				if(cx <= ss.left_lane_threshold):
					sleep(ss.sleep_val)
					print("Path__Go right since centroid's X-Co-ordinate:",cx)

				elif(cx >= ss.right_lane_threshold):
					sleep(ss.sleep_val)
					print("Path__Go Left since centroid's X-Co-ordinate:",cx)

				else:
					sleep(ss.sleep_val)
					print("Path__Go Forward since centroid's X-Co-ordinate:",cx)
		

		cv2.imshow("Robot's Vision", frame)
		if((is_running == 1) and (cv2.waitKey(1)==ss.kill_key_val)):
			feed.release()
			cv2.destroyAllWindows()
			print("--------------------------------------------------------------")
			print(ss.end_msg)
			break


		
def terminal():
	print("Welcome to Team Singularity's image software")
	print("---------------------------------------------")

	vid_capt()		

terminal()
			


		



	
