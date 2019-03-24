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
import argparse
import imagenet
import os
import json
import shutil

parser = argparse.ArgumentParser(description='Sentry')

parser.add_argument('-d', action="store_true", dest='disarm', default=False)
parser.add_argument('-x', action="store_true", dest='headless', default=False)
options = parser.parse_args() 
#print( options ) 
if options.headless == True:
    print( "Running headless (no image display)." )
else:
    print( "Running regular mode (images display)." )

if options.disarm == True:
    print( "Running toothless (no sprinkling)." )
else:
    print( "Running armed (wet!)." )

#pdb.set_trace()
cap = cv2.VideoCapture(0)
firstFrame = None
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
frame_counter = 0
suspects = {}
sprinkler = LED(17) # GPIO for transistor
last = time.time()
#counter = 0 # consecutive shot counter to help us get out of malfunction. No valid reason why we should be sprinkling more than X times in a row
last_shot = None

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
    if options.headless == False:
        cv2.imshow( 'raw_thresh', thresh )

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.erode(thresh, None, iterations=settings.erosions)
    thresh = cv2.dilate(thresh, None, iterations=settings.dilations)
    if options.headless == False:
        cv2.imshow( 'opened_thresh', thresh )

    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len( cnts ) > 5:
        continue

    max_area = 1000
    big_blob = None
    # loop over the contours
    # seems before I wasn't finding the largest but allowing suspects. Let's pick largest blob and see how that works
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
	if x < 50 or x > 330: # 400/2?
            print( "Ignoring blob/contour because x coord ({0}) too small or big (not near center of image).".format( y ) )
	    continue

	if y > 330:
	#if y < 50 or y > 330:
	#if y < settings.min_y_start:
            print( "Ignoring blob/contour because y coord ({0}) too close to edge.".format( y ) )
	    continue

	#if h > w: # let's find an aspect ratio that works to filter on
            #print( "Ignoring blob/contour because taller than wide.".format( y ) )
	    #continue

	if cv2.contourArea(c) > max_area:
		max_area = cv2.contourArea(c)
		big_blob = c

    del cnts[:]
    if big_blob != None:
	    cnts.append( big_blob )

    for c in cnts: # just one in this "list" the way I have it now
	(x, y, w, h) = cv2.boundingRect(c)
        sus_tuple = (x, y, w, h)
	padding = 50
        cv2.rectangle(frame, (x-padding,y-padding), (x+w+padding, y+h+padding), (0, 255, 0), 2)
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

    #shots_fired = False
    # disp recurrents loop
    for suspect in suspects:
        if suspects[ suspect ] == 1: # This leads to a lot of pictures if not careful!!!

	    #if y < settings.min_y_start:
            #    print( "BUG!!! How did this suspect get this far? REALLY ignoring blob/contour because y coord ({0}) too high.".format( y ) )
	    #    continue

            (x,y,w,h) = suspect
            if suspect == last_shot:
                print( "Not re-shooting same candidate." )
                break
            # Let's increase size of sub-image and save to disk
            candidate_file_path = "images/cat_candidate_sub_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".png"
            x_to_use = x
            y_to_use = y
            w_to_use = w
            h_to_use = h
            if( x+2*w<width ):
                w_to_use = 2*w
            if( y+2*h<height ):
                h_to_use = 2*h
            if( x-w>0 ):
                x_to_use = x-w
            if( y-h>0 ):
                y_to_use = y-h
            cv2.imwrite( candidate_file_path , frame[y_to_use:y+h_to_use, x_to_use:x+w_to_use] );
            time.sleep(0.1)

            #cv2.imwrite( "images/cat_candidate_sub_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg", frame[y-h:y+2*h, x-w:x+2*w] );
            means = cv2.mean(frame)
	    #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

	    # Draw a green rectangle around the sub-image we identified
	    cv2.rectangle(frame, (x_to_use, y_to_use), (x + w_to_use, y + h_to_use), (0, 255, 0), 2)
	    text = "Occupied?"
	    cv2.putText(frame, "Garden Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            #cv2.imwrite( "images/cat_candidate_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg", frame );
            if options.headless == False:
                #cv2.imshow('main',frame[x:y, x+w:y+h])
    	        cv2.imshow('main',frame[y:y+h, x:x+w ])
	    print( "Saw something (2x in a row) (area={0}) at {1}. Box = {2}. Mean(s) = {3}.".format( w*h, str( datetime.datetime.now() ), str( (x,y,w,h) ), str( means ) ) )
            last_shot = suspect
	    #shots_fired = True

            ignores = [ "birdhouse", "plane", "milk_can", "pencil_sharpener", "pole", "banister", "hammer", "oscilloscope", "reel", "bannister", "hook", "beaker", "chime", "indigo_bunting", "maypole", "swab" ]
            try:
                # ('Predicted:', [(u'n02843684', u'birdhouse', 0.74303865), (u'n03976657', u'pole', 0.062421516), (u'n04367480', u'swab', 0.054841164)])
                ai_guess = imagenet.recognize( "file:///home/pi/SENTRY/" + candidate_file_path )[0]
                if ai_guess[0][1] in ignores or ai_guess[1][1] in ignores or ai_guess[2][1] in ignores:
                    # delete file from disk
                    print( "Just birdhouse. Delete file and try again." )
                    os.remove( candidate_file_path )
                elif ai_guess[0][1] == "chickadee": # move expected bird species recognized into folders
                    dest_path = candidate_file_path.replace( "images", "images/chickadee_auto" )
                    print( "CHICKADEE!: move to " + dest_path )
                    shutil.move( candidate_file_path, dest_path )
                elif ai_guess[0][1] == "junco": # move expected bird species recognized into folders
                    dest_path = candidate_file_path.replace( "images", "images/junco_auto" )
                    print( "JUNCO!: move to " + dest_path )
                    shutil.move( candidate_file_path, dest_path )
                elif ai_guess[0][1] == "house_finch": # move expected bird species recognized into folders
                    dest_path = candidate_file_path.replace( "images", "images/housefinch_auto" )
                    print( "HOUSE FINCH!: move to " + dest_path )
                    shutil.move( candidate_file_path, dest_path )
		else:
		    print( "Some other bird. Leave in images dir." )
            except Exception as ex:
                print( "Error loading/processing candidate file?!" + str(ex) )

            last_bg_time = now # refresh timer
            if options.disarm == False:
                sprinkler.on()
            #time.sleep( 2 )
            #cv2.imwrite( "images/cat_candidate_post_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg", frame );
            #time.sleep(settings.sprinkler_on_time - 1 )
            #sprinkler.off()
            suspects = {}
            #time.sleep(settings.sprinkler_off_pause)
            break 

    if( len( suspects ) == 0 and ( now - last_bg_time > settings.refresh_bg_time ) ): # don't refresh too frequently, > 1ce per minute
        # constantly replace background due to changing light conditions if no suspects in frame
        firstFrame = gray_blur
        print( "Replaced/updated background frame." )
        last_bg_time = now
        counter = 0

    # Display the resulting frame
    #cv2.imshow('frame',gray)
    if options.headless == False:
        cv2.imshow('main',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
