#!/usr/bin/python

import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import datetime
import numpy as np
import cv2
import imutils
from gpiozero import LED
import time
import pdb
import catcam_settings as settings

cap = cv2.VideoCapture(0)
firstFrame = None
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
frame_counter = 0
suspects = {}
sprinkler = LED(17)
last = time.time()

def do_faces( gray, frame ):
    #faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #faces = face_cascade.detectMultiScale(gray, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20) )
    faces = None
    if faces != None and len( faces ) > 0:
        print( str( len( faces ) ) )

    	for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            #eyes = eye_cascade.detectMultiScale(roi_gray)
            #for (ex,ey,ew,eh) in eyes:
            	#cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Resize for faster processing
    frame = imutils.resize(frame, width=360)
    width = 360
    height = width/480.0 * 640

    now = time.time()
    #last = now
    text = "Unoccupied"

    # Our operations on the frame come here
    # Do operations in grayspace
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Attempt to do face detection
    #do_faces( gray, frame )

    frame_counter += 1
    # Give time for autofocus/white-balance to stabilize
    # Not necessary since we figured out how to disable webcame autofocus
    if frame_counter < 25:
        continue

    # Let's try some motion detection
    gray_blur = cv2.GaussianBlur(gray, (21, 21), 0)
    if firstFrame == None:
        firstFrame = gray_blur
        last_bg_time = now
        continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray) 
    thresh = cv2.threshold(frameDelta, settings.threshold, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow( 'raw_thresh', thresh )

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.erode(thresh, None, iterations=settings.erosions)
    thresh = cv2.dilate(thresh, None, iterations=settings.dilations)
    cv2.imshow( 'opened_thresh', thresh )

    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    new_suspects = []
    for c in cnts:
	# if the contour is too small, ignore it
	if cv2.contourArea(c) < settings.min_area:
            print( "Ignoring blob/contour because area ({0}) too small.".format( cv2.contourArea(c) ) )
	    continue

	if cv2.contourArea(c) > (width*height*settings.max_area_fraction ):
            print( "Ignoring blob/contour because area ({0}) too big.".format( cv2.contourArea(c) ) )
	    continue

	# compute the bounding box for the contour, draw it on the frame,
	# and update the text
	(x, y, w, h) = cv2.boundingRect(c)
	#if x < 50/2 or y < 50/2 or y > 400/2:
	if y < settings.min_y_start:
            print( "Ignoring blob/contour because y coord ({0}) too high.".format( y ) )
	    continue

	if h > w:
            print( "Ignoring blob/contour because taller than wide.".format( y ) )
	    continue

        sus_tuple = (x, y, w, h)
        new_suspects.append( sus_tuple )
        #print( "Suspect at " + str( sus_tuple ) )
        if sus_tuple in suspects:
            suspects[ sus_tuple ] += 1
	else:
	    suspects[ sus_tuple ] = 1

    # purge loop
    remove = []
    for suspect in suspects:
        #print( "Considering previous suspect." )
        if suspect not in new_suspects:
            #print( "Removing suspect from tracking list since didn't occur this time." )
            remove.append( suspect )
    for cleared_suspect in remove:
	    suspects.pop( cleared_suspect )

    # disp recurrents loop
    for suspect in suspects:
        if suspects[ suspect ] == 2:
	    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	    print( "Saw something (2x in a row) (area={0}) at {1}.".format( w*h, str( datetime.datetime.now() ) ) )
	    text = "Occupied"
	    cv2.putText(frame, "Garden Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.imwrite( "images/cat_candidate_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg", frame );
    	    cv2.imshow('main',frame)

            last_bg_time = now # refresh timer
	    sprinkler.on()
            time.sleep(settings.sprinkler_on_time)
            sprinkler.off()
            suspects = {}
            time.sleep(settings.sprinkler_off_pause)
            break
 
    if len( suspects ) == 0 and ( now - last_bg_time > settings.refresh_bg_time ):
        # constantly replace background due to changing light conditions if no suspects in frame
        firstFrame = gray_blur
        print( "Replaced/updated background frame." )
        last_bg_time = now

    # Display the resulting frame
    #cv2.imshow('frame',gray)
    cv2.imshow('main',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
