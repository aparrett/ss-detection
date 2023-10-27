import cv2
import datetime
import math
import os
import ntpath

### SETTINGS ###

filePath = "medium.mp4"

# if the object in motion is moving slower than the speedThreshold, it will be ignored *after the initial detection*.
motionSpeedThreshold = 15

# strength of noise removal
# default: 11
blurThreshold = 11 

# comparison threshold
# default: 10
differenceThreshold = 10 

# motion less than this size will be ignored
# default: 100
sizeOfMovementThreshold = 100 

# number of frames to skip before creating another new file so we don't have 100 pictures of every meteor
# set to 1 to remove debounce
# default: 3
debounceLimit = 3

# change to True to show a video with rectangles around detected motion
# this can be useful for playing with the thresholds
showVideo = False 



### Program ###

# Don't touch anything below this
if os.path.exists(filePath) == False:
	print(f'Could not find file at {filePath}. Exiting.')
	exit()

fileName = ntpath.basename(filePath)

outputPath = 'logs/' + os.path.splitext(fileName)[0]
outputFolderExists = os.path.exists(outputPath)
if outputFolderExists == False:
	os.makedirs(outputPath)

outputLogPath = outputPath + '/log.txt'
# outputFileExists = os.path.isfile(outputLogPath)
# if outputFileExists == False:
log = open(outputLogPath, "a")


video = cv2.VideoCapture(filePath)
fps = video.get(cv2.CAP_PROP_FPS)
background = None
i = 0
debounceCount = 0
prevX = 0
prevY = 0

while True:
	i += 1
	status, frame = video.read()

	if status == False:
		break

	# i % 5 changes the background throughout the video so that stars aren't detected
	if i % 5 == 1:
		background = frame
		background = cv2.cvtColor(background,cv2.COLOR_BGR2GRAY)
		background = cv2.GaussianBlur(background,(blurThreshold,blurThreshold),0)
		if i == 1:
			continue

	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray,(blurThreshold,blurThreshold), 0)

	diff = cv2.absdiff(background,gray)

	thresh = cv2.threshold(diff,differenceThreshold,255,cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations = 2)

	cnts,res = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	j = 0
	for contour in cnts:
		if cv2.contourArea(contour) > sizeOfMovementThreshold :
			j += 1

			(x,y,w,h) = cv2.boundingRect(contour)

			distanceMoved = abs(prevX - x) + abs(prevY - y)
			if distanceMoved < motionSpeedThreshold:
				prevX = x
				prevY = y
				continue

			if j == 1: # only log a single detected motion per frame
				if debounceCount == 0:
					seconds = i / fps
					secondsDisplay = math.floor((seconds % 60 * 10)) / 10
					minutesDisplay = math.floor(seconds / 60)
					hoursDisplay = math.floor(seconds / 60 / 60)
					motionTimestamp = f'{hoursDisplay}h-{minutesDisplay}m-{secondsDisplay}s'
					log.write(f'Detected motion at {motionTimestamp} \n')
					print(f'Detected motion at {motionTimestamp}')
					cv2.imwrite(f'{outputPath}/motion-{motionTimestamp}.jpg', frame)

				debounceCount += 1
				if debounceCount == debounceLimit:
					debounceCount = 0

			prevX = x
			prevY = y
			if (showVideo == True):
				cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0), 3)

	if (showVideo == True):
		cv2.imshow("All Contours", frame)

	key = cv2.waitKey(1)
	if key == ord('q'):
		break

log.close()
video.release()