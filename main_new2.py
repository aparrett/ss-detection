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
filePath = "C:\\Users\\aparr\\Documents\\Stars\\files"

# default: 15
proximityThreshold = 100

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
  return isRectangular(w, h) and cv2.contourArea(contour) > sizeOfMovementThreshold

def getProximity(previousDetections, currentDetection):
  result = False
    
  return result

def getTimeStamp(frameNumber, fps):
  seconds = frameNumber / fps
  secondsDisplay = math.floor((seconds % 60 * 100)) / 100
  minutesDisplay = math.floor((seconds / 60) % 60)
  hoursDisplay = math.floor(seconds / 60 / 60)
  motionTimestamp = f'{hoursDisplay}h-{minutesDisplay}m-{secondsDisplay}s'
  return motionTimestamp

def saveFrame(outputPath, saveFrameTimestamp, frame):
  outputLogPath = outputPath + '/log.txt'
  log = open(outputLogPath, "a")

  fileName = getUniqueFileName(f'{outputPath}/motion-{saveFrameTimestamp}')
  cv2.imwrite(f'{fileName}.jpg', frame)
  log.write(f'Detected motion at {saveFrameTimestamp} \n')
  log.close()
  print(f'Detected motion at {saveFrameTimestamp}')

def drawBox(frame, rect):
  box = cv2.boxPoints(rect)
  box = np.intp(box)
  img = cv2.drawContours(frame,[box],0,(0,255,255),2)
  return img

def getUniqueFileName(fileName):
  if os.path.isfile(fileName + '.jpg') is False:
    return fileName

  lastChar = fileName[-1]
  if lastChar.isnumeric():
    fileName = f'{fileName[:-1]}{int(lastChar)+1}'
  else:
    fileName = f'{fileName}1'

  if os.path.isfile(fileName + '.jpg') is True:
    return getUniqueFileName(fileName)
  else: 
    return fileName

def processVideo(filePath):
  print(f'Processing video at {filePath}')
  fileName = ntpath.basename(filePath)

  outputPath = 'logs/' + os.path.splitext(fileName)[0]
  outputFolderExists = os.path.exists(outputPath)
  if outputFolderExists == False:
    os.makedirs(outputPath)

  video = cv2.VideoCapture(filePath)
  fps = video.get(cv2.CAP_PROP_FPS)
  background = None
  i = 0
  debounceCount = 0
  prevX = 0
  prevY = 0
  previousDetections = []

  while True:
    i += 1 # start at frame 1
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

    meteorDetected = False

    for contour in cnts:
      if (not isPossibleMeteor(contour)):
        print('no motion found')
        continue

      meteorDetected = True
      rect = cv2.minAreaRect(contour)
      x1, y1 = rect[0]
      w1, h1 = rect[1]

      print(len(previousDetections))
      foundPreviousDetection = False
      for previousDetection in previousDetections:
        [x2, y2] = previousDetection[0][0]
        [w2, h2] = previousDetection[0][1]
        distanceMoved = math.hypot(x1 - x2, y1 - y2)
        print('distance ', distanceMoved)
        # If it's the same meteor and the previous detection was bigger than the current detection
        # save the previous detection and remove the meteor from previousDetections.
        if (distanceMoved < proximityThreshold): # motion is likely the same meteor
          foundPreviousDetection = True
          # previousDetections.remove(previousDetection)
          print('found previous detection')
          if (w2 * h2 >= w1 * h1):
            print('previous was bigger')
            # if (saveOutline == True):
            #   saveFrame(outputPath, previousDetection[1], drawBox(previousDetection[2], previousDetection[0]))
            # else:
            #   saveFrame(outputPath, previousDetection[1], previousDetection[2])
          else:
            previousDetections.remove(previousDetection)
            previousDetections.append([rect, getTimeStamp(i, fps), frame])
        
      if (foundPreviousDetection == False):
        previousDetections.append([rect, getTimeStamp(i, fps), frame])

      # if (showVideo == True):
      #   cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0), 1)

    if meteorDetected == False and len(previousDetections) > 0:
      print('meteor not detected')
      # saveFrame(outputPath, getTimeStamp(i, fps), frame)
      for previousDetection in previousDetections:
        if (saveOutline == True):
          saveFrame(outputPath, previousDetection[1], drawBox(previousDetection[2], previousDetection[0]))
        else:
          saveFrame(outputPath, previousDetection[1], previousDetection[2])

      previousDetections = []

    if (showVideo == True):
      cv2.imshow("All Contours", frame)

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