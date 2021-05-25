import numpy as np
import cv2

is_running = 0

def vid_capt():					 		# TO FIX - I think blue and yellow HSV values are overlapping, modify it
	global is_running

	feed = cv2.VideoCapture(0)

	while(True):
		#_,frame = feed.read()
		is_running = 1

		ret,frame=feed.read()

		hsv1=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

		red_lb = np.array([136, 87, 111],np.uint8)
		red_ub = np.array([180, 255, 255],np.uint8)
		red_mask= cv2.inRange(hsv1,red_lb,red_ub)	#ub- upper bound, lb- lower bound

		gre_lb = np.array([50,100,100],np.uint8)
		gre_ub = np.array([70,255,255],np.uint8)
		gre_mask= cv2.inRange(hsv1,gre_lb,gre_ub)	#ub- upper bound, lb- lower bound,gre- green

		blu_lb = np.array([38,86,0],np.uint8)
		blu_ub = np.array([121,255,255],np.uint8)
		blu_mask= cv2.inRange(hsv1,blu_lb,blu_ub)	#ub- upper bound, lb- lower bound, blu- blue

		yel_lb = np.array([20,100,100],np.uint8)
		yel_ub = np.array([30,255,255],np.uint8)
		yel_mask = cv2.inRange(hsv1,yel_lb,yel_ub) # same same 

		kernel=np.ones((5,5),"uint8")

		#dilation effects go below- 

		#red
		red_mask = cv2.dilate(red_mask,kernel)
		res_red = cv2.bitwise_and(frame,frame,mask=red_mask)
		#contour to track red color goes below- 
		contours, hierarchy = cv2.findContours(red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		for pic, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if(area > 300):
				x, y, w, h = cv2.boundingRect(contour)
				frame = cv2.rectangle(frame, (x, y),(x + w, y + h),(0, 0, 255), 2)
				cv2.putText(frame, "RED", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0, 0, 255))
				

		#green
		gre_mask = cv2.dilate(gre_mask,kernel)
		res_green = cv2.bitwise_and(frame,frame,mask=gre_mask)
		#contour to track red color goes below- 
		contours, hierarchy = cv2.findContours(gre_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		for pic, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if(area > 300):
				x, y, w, h = cv2.boundingRect(contour)
				frame = cv2.rectangle(frame, (x, y),(x + w, y + h),(0, 255, 0), 2)
				cv2.putText(frame, "GREEN", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0, 255, 0))
				

		
		#yellow
		yel_mask = cv2.dilate(yel_mask,kernel)
		res_yel = cv2.bitwise_and(frame,frame,mask=yel_mask)
		#contour to track yel color goes below- 
		contours, hierarchy = cv2.findContours(yel_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		for pic, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if(area > 300):
				x, y, w, h = cv2.boundingRect(contour)
				frame = cv2.rectangle(frame, (x, y),(x + w, y + h),(20, 100, 100), 2)
				cv2.putText(frame, "YELLOW", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(20, 100, 100))

		#blue
		blu_mask = cv2.dilate(blu_mask,kernel)
		res_blu = cv2.bitwise_and(frame,frame,mask=blu_mask)
		#contour to track blu color goes below- 
		contours, hierarchy = cv2.findContours(blu_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		for pic, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if(area > 300):
				x, y, w, h = cv2.boundingRect(contour)
				frame = cv2.rectangle(frame, (x, y),(x + w, y + h),(255, 0, 0), 2)
				cv2.putText(frame, "BLUE", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(255, 0, 0))

		cv2.imshow("Colour Detection", frame)
		if((is_running == 1) and (cv2.waitKey(1)==0)):
			feed.release()
			cv2.destroyAllWindows()
			print("--------------------------------------------------------------")
			print("Operation Ended")
			break


def img_capt():

	path='C:/Users/Ronnie/Downloads/pic.jpeg'
	feed=cv2.imread(path)

	graypic=cv2.cvtColor(feed,cv2.COLOR_BGR2GRAY)
	edges=cv2.Canny(graypic,30,200)

	#_,feed = feed.read()
	is_running = 1

	#ret,feed=feed.read()

	hsv1=cv2.cvtColor(feed,cv2.COLOR_BGR2HSV)

	red_lb = np.array([136, 87, 111],np.uint8)
	red_ub = np.array([180, 255, 255],np.uint8)
	red_mask= cv2.inRange(hsv1,red_lb,red_ub)	#ub- upper bound, lb- lower bound

	gre_lb = np.array([71,76,84],np.uint8)
	gre_ub = np.array([91,96,164],np.uint8)
	gre_mask= cv2.inRange(hsv1,gre_lb,gre_ub)	#ub- upper bound, lb- lower bound,gre- green

	blu_lb = np.array([120,240,212],np.uint8)
	blu_ub = np.array([120,240,70],np.uint8)
	blu_mask= cv2.inRange(hsv1,blu_lb,blu_ub)	#ub- upper bound, lb- lower bound, blu- blue

	yel_lb = np.array([20,100,100],np.uint8)
	yel_ub = np.array([30,255,255],np.uint8)
	yel_mask = cv2.inRange(hsv1,yel_lb,yel_ub) # same same 

	kernel=np.ones((5,5),"uint8")

	#dilation effects go below- 

	#red
	red_mask = cv2.dilate(red_mask,kernel)
	res_red = cv2.bitwise_and(feed,feed,mask=red_mask)
	#contour to track red color goes below- 
	contours, hierarchy = cv2.findContours(red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 300):
			x, y, w, h = cv2.boundingRect(contour)
			feed = cv2.rectangle(feed, (x, y),(x + w, y + h),(0, 0, 255), 2)
			cv2.putText(feed, "RED", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0, 0, 255))
			print("Action-1")

	#green
	gre_mask = cv2.dilate(gre_mask,kernel)
	res_green = cv2.bitwise_and(feed,feed,mask=gre_mask)
	#contour to track red color goes below- 
	contours, hierarchy = cv2.findContours(gre_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 300):
			x, y, w, h = cv2.boundingRect(contour)
			feed = cv2.rectangle(feed, (x, y),(x + w, y + h),(0, 255, 0), 2)
			cv2.putText(feed, "GREEN", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0, 255, 0))
				

		
	#yellow
	yel_mask = cv2.dilate(yel_mask,kernel)
	res_yel = cv2.bitwise_and(feed,feed,mask=yel_mask)
	#contour to track yel color goes below- 
	contours, hierarchy = cv2.findContours(yel_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 300):
			x, y, w, h = cv2.boundingRect(contour)
			feed = cv2.rectangle(feed, (x, y),(x + w, y + h),(20, 100, 100), 2)
			cv2.putText(feed, "YELLOW", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(20, 100, 100))

	#blue
	blu_mask = cv2.dilate(blu_mask,kernel)
	res_blu = cv2.bitwise_and(feed,feed,mask=blu_mask)
	#contour to track blu color goes below- 
	contours, hierarchy = cv2.findContours(blu_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 300):
			x, y, w, h = cv2.boundingRect(contour)
			feed = cv2.rectangle(feed, (x, y),(x + w, y + h),(255, 0, 0), 2)
			cv2.putText(feed, "BLUE", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(255, 0, 0))

	cv2.imshow("Colour Detection",edges)
	if((is_running == 1) and (cv2.waitKey(0)==0)):
		cv2.destroyAllWindows()
		print("--------------------------------------------------------------")
		print("Operation Ended")
		
def terminal():
	print("Welcome to Team Singularity's image software")
	print("---------------------------------------------")

	val=int(input("Enter 1 for image, 2 for real time\n"))

	if(val==1):
		img_capt()
		
	if(val==2):
		vid_capt()

	else:
		print("Re-enter the choice")
		print("******************************************")
		print("")
		terminal()

terminal()
			


		



	
