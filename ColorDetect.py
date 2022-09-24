import cv2
import sys
import numpy as np

def nothing(x):
    pass

# Load image
# image = cv2.imread('1.png')

# Create pop up window
cv2.namedWindow('detector')

# create trackbars for color manipulations
cv2.createTrackbar('HMin', 'detector', 0, 255, nothing) # hue ranges from 0-179 for Opencv
cv2.createTrackbar('SMin', 'detector', 0, 255, nothing)
cv2.createTrackbar('VMin', 'detector', 0, 255, nothing)
cv2.createTrackbar('HMax', 'detector', 0, 179, nothing)
cv2.createTrackbar('SMax', 'detector', 0, 255, nothing)
cv2.createTrackbar('VMax', 'detector', 0, 255, nothing)

# Set default value for MAX HSV trackbars.
cv2.setTrackbarPos('HMax',  'detector',  179)
cv2.setTrackbarPos('SMax',  'detector',  255)
cv2.setTrackbarPos('VMax',  'detector',  255)

# Initialize to check if HSV min/max value changes
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0


wait_time = 33

cap=cv2.VideoCapture(0)
while(1):
    ret, image=cap.read()
    image=cv2.flip(image, 1)
    output = image
    # get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin', 'detector')
    sMin = cv2.getTrackbarPos('SMin', 'detector')
    vMin = cv2.getTrackbarPos('VMin', 'detector')

    hMax = cv2.getTrackbarPos('HMax', 'detector')
    sMax = cv2.getTrackbarPos('SMax', 'detector')
    vMax = cv2.getTrackbarPos('VMax', 'detector')

    # set minimum and max HSV values to display
    lower = np.array([hMin,  sMin,  vMin])
    upper = np.array([hMax,  sMax,  vMax])

    # create HSV image and threshold into a range
    hsv = cv2.cvtColor(image,  cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,  lower,  upper)
    output = cv2.bitwise_and(image, image,  mask= mask)

    # print if there is a change in HSV value
    if( (phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
        print("[%d, %d, %d], [%d, %d, %d]" % (hMin ,  sMin ,  vMin,  hMax,  sMax ,  vMax))
        phMin = hMin
        psMin = sMin
        pvMin = vMin
        phMax = hMax
        psMax = sMax
        pvMax = vMax

    # display output image
    cv2.imshow('detector', output)

    # freeze handling- wait a bit to prevent video freezing
    if cv2.waitKey(wait_time) & 0xFF == 27:
        break

cv2.destroyAllWindows()