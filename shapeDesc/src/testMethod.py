#!/bin/python
import cv2
import numpy as np

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



img = cv2.imread("car.jpg")
boxes = blobDetect(img)

