import cv2
import numpy as np
from matplotlib import pyplot as plt


img = cv2.imread('MSPS_Serial_structure.png')


for i in range(10,201,10):
    ret,thresh_img = cv2.threshold(img,i,255, cv2.THRESH_BINARY)
    cv2.imwrite('thresh_'+str(i)+'.png',thresh_img)
