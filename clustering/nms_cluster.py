import cv2
import numpy as np
from nms import non_max_suppression_fast
import argparse
import sys
import matplotlib.pyplot as plt
import utils_cluster


WINDOW_DIM = 64
STEPSZ = 8

XCOORD = 0
YCOORD = 1
PROB = 2



parser = argparse.ArgumentParser()
parser.add_argument('-i', "--image", required = True, dest='image', help='input image name')
parser.add_argument('-d', "--data", required = True, dest='data', help='metadata image name')
parser.add_argument('-p', "--prob", required = False, dest='prob', default=0.7, type=float, help='minimum probability')
parser.add_argument('-s', "--minsamples", required = False, dest='minsamples', default=2, type=int, help='NMS minimum cluster size')
opts = parser.parse_args()


data = np.genfromtxt(opts.data, delimiter=' ')
image = cv2.imread(opts.image)
clone = image.copy()
boxes = []

for i in range(0, data.shape[0]):

    if data[i][PROB] > opts.prob:
        x1 = int(data[i][XCOORD])
        y1 = int(data[i][YCOORD])
        x2 = x1 + WINDOW_DIM
        y2 = y1 + WINDOW_DIM

        boxes.append([x1,y1,x2,y2])
        cv2.circle(clone, (int(data[i][XCOORD])+WINDOW_DIM/2, int(data[i][YCOORD])+WINDOW_DIM/2), 4, [0,0,255], -1) # FOR STU'S

boxes = np.array(boxes)
boxes_nonmax = non_max_suppression_fast(boxes, 0.5,opts.minsamples-1)

utils_cluster.drawClusterColorsNMS(clone, boxes_nonmax)
cv2.imwrite("output.jpg", clone)



#minHits = [0,1,3,5,7]
#overlapPercent = np.arange(0.0,1.05,0.05) 
#for hit in minHits:
#    nBoxes = []
#    for overlap in overlapPercent:
#        boxes_nonmax = non_max_suppression_fast(boxes, overlap,hit)
#        nBoxes.append(len(boxes_nonmax))
#    nBoxes = np.array(nBoxes)
#    nCars = [88 for i in range(len(overlapPercent))]
#    nCars = np.array(nCars)
#    plt.figure(num=None, figsize=(9.5, 4.5), dpi=80, facecolor='w', edgecolor='k')
#    plt.plot(overlapPercent*100,nBoxes ,alpha=0.85, label="Number of Boxes",color="#348ABD")
#    plt.plot(overlapPercent*100,nCars ,alpha=0.85, label="Number of Cars (88)",color="#E24A33")
#    plt.title("Overlap Percent vs Number of Boxes (Cars)  Min_Hits=%d"%(hit+1))
#    plt.xlim(0,100)
#    plt.xlabel("% Overlap")
#    plt.ylabel("Number of Boxes")
#    lgd=plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#    plt.savefig("overlap_vs_numBoxes_min_%d.jpg"%(hit+1), bbox_extra_artists=(lgd,), bbox_inches='tight')


