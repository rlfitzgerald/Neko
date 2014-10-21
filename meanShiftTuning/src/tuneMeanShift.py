import cv2
import pymeanshift as pms
import numpy as np
import time

def meanShift(img, sradius=6, rradius=4.5, mdensity=50):

    (segmented_image, labels_image, number_regions) = pms.segment(img, sradius, rradius, mdensity)
    return segmented_image


def blobDetect(img):
    #smooth image to reduce noise
    img1 = cv2.blur(img, (3,3))

    #convert to gray scale image
    img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)

    #threshold gray scale image
    (threshold, img_bw) = cv2.threshold(img1, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    #save black and white image (to debug)
    cv2.imwrite('Black_and_White.jpg', img_bw)

    #find contours in black and white image
    contours, hierarchy = cv2.findContours(img_bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    #convert to color for debugging purposes
    colorImg = cv2.cvtColor(img1, cv2.COLOR_GRAY2RGB)
    boxes = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area <= 2200:
            rect = cv2.minAreaRect(cnt)
            box = cv2.cv.BoxPoints(rect)
            box = np.int0(box)
            boxes.append(box)
            cv2.drawContours(colorImg, [box], 0, (0, 0, 255), 2)

    cv2.imwrite('Boxes.jpg', colorImg)
    return boxes

def compareBoxes(originalBox, newBox, cornerTolerance = 50):

    #Each box is a list of 4 arrays, each containing two integer entries (the x and Y coordinates for each
    #corrosponding point for the box)

    cornerMaxes = []
    cornerMins = []

    for i in range(len(originalBox)):
        cornerMaxes.append([originalBox[i][0] + cornerTolerance, originalBox[i][[1]] + cornerTolerance])
        cornerMins.append([originalBox[i][0] - cornerTolerance, originalBox[i][1] - cornerTolerance])

    cornersLowEnough = []
    cornersHighEnough = []

    for i in range(len(newBox)):
        cornersLowEnough.append(newBox[i][0] <= cornerMaxes[i][0] and newBox[i][1] <= cornerMaxes[i][1])
        cornersHighEnough.append(newBox[i][0] >= cornerMins[i][0] and newBox[i][1] >= cornerMins[i][1])

    result = True
    for i in range(len(cornersHighEnough)):
        result = result and cornersHighEnough[i] and cornersLowEnough[i]

    return result

def tuneMeanShift(filename):

    startTime = time.time()
    #Detect blobs on initial image, save blob locations
    img = cv2.imread(filename)
    boxes = blobDetect(img)
    goodConfigs = []

    for i in range(15):
        tempImg = meanShift(img, sradius=i)
        cv2.imwrite('shifted_sradius' + str(i) + '.jpg', tempImg)
        tempBoxes = blobDetect(tempImg)

        #if a different number of blobs is detected, auto reject this configuration
        if len(tempBoxes) == len(boxes):
            tempRes = False
            for j in range(len(tempBoxes)):
                tempRes = compareBoxes(boxes[j], tempBoxes[j])
                if i == 0 and j == 0:
                    goodConfigs.append(tempRes)
                else:
                    goodConfigs[i] = goodConfigs[i] and tempRes

    endTime = time.time()
    print("Good Configurations: \n")
    for i in range(len(goodConfigs)):
        if goodConfigs[i]:
            print i

    print("Runtime: %s seconds" % str(endTime - startTime))

