import cv2
import numpy as np
import argparse
import sys
import optics
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
parser.add_argument('-r', "--rad", required = False, dest='rad', default=8, type=int, help='OPTICS max radius')
parser.add_argument('-s', "--minsamples", required = False, dest='minsamples', default=2, type=int, help='OPTICS minimum cluster size')
opts = parser.parse_args()


data = np.genfromtxt(opts.data, delimiter=' ')
image = cv2.imread(opts.image)
clone = image.copy()

hits = []
for i in range(0, data.shape[0]):
    if data[i][PROB] > opts.prob:
        hits.append(optics.Point(data[i][XCOORD] + WINDOW_DIM/2, data[i][YCOORD] + WINDOW_DIM/2))
        cv2.circle(clone, (int(data[i][XCOORD])+WINDOW_DIM/2, int(data[i][YCOORD])+WINDOW_DIM/2), 4, [0,0,255], -1) # FOR STU'S


opticsObj = optics.Optics(hits, WINDOW_DIM/2, opts.minsamples) # radius for neighbor consideration, cluster size >= 2 points
opticsObj.run()                    # run the algorithm
clusters = opticsObj.cluster(STEPSZ)   # threshold for clustering

utils_cluster.drawClusterColorsOptics(clone, clusters)
cv2.imwrite("output.jpg", clone)
