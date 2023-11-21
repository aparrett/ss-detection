import cv2
import datetime
import math
import os
import ntpath
import glob
import numpy as np 

### SETTINGS ###

# Example file: C:\\Users\\username\\Documents\\files\\video.mp4
# Example folder: C:\\Users\\username\\Documents\\files 
filePath = "C:\\Users\\aparr\\Documents\\Stars\\files\\faint.mp4"

# if the object in motion is moving slower than the speedThreshold, it will be ignored *after the initial detection*.
# default: 15
motionSpeedThreshold = 15

# strength of noise removal
# default: 11
blurThreshold = 15 

# comparison threshold
# default: 10
differenceThreshold = 10

# motion less than this size will be ignored
# default: 100
sizeOfMovementThreshold = 100

# change to True to show a video with rectangles around detected motion
# this can be useful for playing with the thresholds
showVideo = False # this is currently broken 

# change to True to include an outline (a yellow rectangle) of the detected motion in the saved screenshot
saveOutline = True

### Program ###

print('Starting meteor detection.')

def isRectangular(w, h):
  return w > h * 1.7 or h > w * 1.7

def isPossibleMeteor(contour):
  rect = cv2.minAreaRect(contour)
  w, h = rect[1]
  return isRectangular(w, h) and cv2.contourArea(contour) > sizeOfMovementThreshold:

def processVideo(filePath):
  print(f'Processing video at {filePath}')
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

    shouldSaveFrame = False

    for contour in cnts:
      if (not isPossibleMeteor(contour)):
        continue

      rect = cv2.minAreaRect(contour)
      x, y = rect[0]
      w, h = rect[1]

      # distanceMoved = math.hypot(prevX - x, prevY - y)
      if (saveOutline == True):
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        cv2.drawContours(frame,[box],0,(0,255,255),2)

      prevX = x
      prevY = y
      # if (showVideo == True):
      #   cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0), 1)

    if (shouldSaveFrame == True):
      seconds = i / fps
      secondsDisplay = math.floor((seconds % 60 * 100)) / 100
      minutesDisplay = math.floor((seconds / 60) % 60)
      hoursDisplay = math.floor(seconds / 60 / 60)
      motionTimestamp = f'{hoursDisplay}h-{minutesDisplay}m-{secondsDisplay}s'
      cv2.imwrite(f'{outputPath}/motion-{motionTimestamp}.jpg', frame)
      log.write(f'Detected motion at {motionTimestamp} \n')
      print(f'Detected motion at {motionTimestamp}')

    if (showVideo == True):
      cv2.imshow("All Contours", frame)

  log.close()
  video.release()

# Don't touch anything below this
if os.path.isdir(filePath):
  for file in glob.iglob(f'{filePath}\\*', recursive=True):
    processVideo(file)
elif os.path.isfile(filePath):
  processVideo(filePath)
else:
  print(f'Could not find file at {filePath}. Exiting.')

print('Finished processing.')