import numpy as np
import cv2

def eyeTracking(eyelist):
	eye1, eye2 = eyelist[0], eyelist[1]
	if eye1[0] < eye2[0]:
		right = eye1
		left = eye2
	else:
		right = eye2
		left = eye1
	right_w = right[2] - right[0]
	right_h = right[3] - right[1]

	left_w = left[2] - left[0]
	left_h = left[3] - left[1]

	ud = (float(right[3] + right[1] + left[3] + left[1])/4 - 190)/190 * 5
	right_area = float(right_w * right_h)
	left_area = float(left_w * left_h)
	
	if right_area < left_area:
		lw = right_area/left_area * -15
	else:
		lw = left_area/right_area * 15
	return lw, ud

def getEyes(image):
	frame = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
	pupilFrame=frame
	clahe=frame
	blur=frame
	edges=frame
	eyes = cv2.CascadeClassifier('haarcascade_eye.xml')
	detected = eyes.detectMultiScale(frame, 1.25, 5)
	eyelist = []
	for (x,y,w,h) in detected: #similar to face detection
		cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (0,0,255),1)	 #draw rectangle around eyes
		cv2.line(frame, (x,y), ((x+w,y+h)), (0,0,255),1)   #draw cross
		cv2.line(frame, (x+w,y), ((x,y+h)), (0,0,255),1)
		eyelist.append((x,y, x+w,y+h))
                       
		#pupilFrame = cv2.equalizeHist(frame[y+(h*.25):(y+h), x:(x+w)]) #using histogram equalization of better image. 
		cl1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)) #set grid size
		clahe = cl1.apply(pupilFrame)  #clahe
		blur = cv2.medianBlur(clahe, 7)  #median blur
	x, y = 240, 170
	if len(eyelist) == 1:
		lower, upper = eyelist[0]
		x, y = (lower[0] + upper[0])/2, (lower[1] + upper[1])/2
	if len(eyelist) == 2:
		lr, ud = eyeTracking(eyelist)
		x = int(240 + 240 * lr/15)
		y = int(170 + 170 * ud / 5)
	frame = cv2.rectangle(frame, (x,y), ((x+1),(y+1)), (255,255,255),3)
	cv2.imshow("Webcam", frame)
	cv2.waitKey(1)
	

	
def closeWindows():
	cv2.destroyAllWindows()