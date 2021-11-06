import cv2 
import numpy as np
from time import sleep


#---------------------------------ALL VARIABLES GO BELOW----------------------------------------------------
path = 'C:/Users/Ronnie/Downloads/testvid_full_pov.mp4'	# media path make 0 for webcam
			#'C:/Users/Ronnie/Downloads/testvid_full_pov.mp4'
			#/Users/sanjandmurthy/Desktop/Frojact OAsisi/yet.mp4
lb = 5														
lg = 190
lr = 121
ub = 25		# lower and upper BGR values
ug = 210
ur = 201

lower_colour_bound = np.array([lb,lg,lr])
upper_colour_bound = np.array([ub,ug,ur])

left_lane_threshold = 210 # Cx value, left 
right_lane_threshold = 360 # Cx value, right

sleep_val = 0.10 # increase for slower video feed, decrease for faster feed, make 0 for real time view

min_area_filtered = 2000 # minimum area criteria to pass. Anything below this value is noise 

kill_key_val = 0 # key binding to kill the program 

Frame_name = "Frame" # display name-  normal frame
Mask_Frame_name = "Mask Frame" # display name - masked frame

end_msg = "___Operation Ended___" # final message to be printed

red_left_path_threshold = 150

red_right_path_threshold = 400

Red_signature = 0 # Do not change, will cause errors

#-----------------------------------ALL FUNCTIONS GO BELOW--------------------------------------------------
def docs():
    print("The green dot: This is the centroid point of the contours mapped in real time")
    print("___________________________________________________")
    print("The black screen: This is the masked frame, where anything yellow is depicted in white and the rest is black. Here the track is yellow and is thus highlighted")
    print("___________________________________________________")
    print("The Red rectangles:  These are the object (track) contours being detected. They are obtained after passing through an area filter , to eliminate noise.")
    print("___________________________________________________")
    print("NOTE- The actions are displayed on the output screen, and they depict micro actions of the robot in real time")
    print("")
    print("------End of Docs------")


def red_follow():

	my_feed = cv2.VideoCapture(0)

	while True:

		_,frame = my_feed.read()

		
		hsv1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
		red_lb = np.array([136, 87, 111],np.uint8)
		red_ub = np.array([180, 255, 255],np.uint8)
		red_mask= cv2.inRange(hsv1,red_lb,red_ub)

		kernel=np.ones((40,40),"uint8")
		ret,thresh1 = cv2.threshold(red_mask,127,255,0)

		red_mask = cv2.dilate(red_mask,kernel)
		res_red = cv2.bitwise_and(frame,frame,mask=red_mask)
		#contour to track red color goes below- 
		contours, hierarchy = cv2.findContours(red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

		for current_contour in contours:

			M = cv2.moments(thresh1)

			if M["m00"] != 0:
				cx = int(M["m10"] / M["m00"])
				cy = int(M["m01"] / M["m00"])
			else:
				cx = 0
				cy = 0

			if(cx <= red_left_path_threshold):
				sleep(sleep_val)
				print("Go left since centroid's X-Co-ordinate:",cx)

			elif(cx >= red_right_path_threshold):
				sleep(sleep_val)
				print("Go right since centroid's X-Co-ordinate:",cx)

			else:
				sleep(sleep_val)
				print("Go Forward since centroid's X-Co-ordinate:",cx)


		for pic, contour in enumerate(contours):
			red_area = cv2.contourArea(contour)

			if(red_area > 10000):
				Red_signature = 1
				x, y, w, h = cv2.boundingRect(contour)
				frame = cv2.rectangle(frame, (x, y),(x + w, y + h),(0, 0, 255), 2)
				cv2.putText(frame, "RED", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0, 0, 255))

			elif(red_area < 10000):
				Red_signature = 0


		cv2.imshow("Frame",frame)
		cv2.imshow("Mask",red_mask)
		if(cv2.waitKey(1)==0):
			break
        
	my_feed.release()
	cv2.destroyAllWindows()
	

#red_follow()
	
	










