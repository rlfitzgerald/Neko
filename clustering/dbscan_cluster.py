import cv2
import numpy as np
import argparse
import sys
from sklearn.cluster import DBSCAN
from scipy import spatial
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
parser.add_argument('-e', "--eps", required = False, dest='eps', default=8, type=int, help='DBSCAN epsilon')
parser.add_argument('-s', "--minsamples", required = False, dest='minsamples', default=2, type=int, help='DBSCAN minimum cluster size')
opts = parser.parse_args()


data = np.genfromtxt(opts.data, delimiter=' ')
image = cv2.imread(opts.image)
clone = image.copy()

hits = []
for i in range(0, data.shape[0]):
    if data[i][PROB] > opts.prob:
        hits.append((data[i][XCOORD] + WINDOW_DIM/2, data[i][YCOORD] + WINDOW_DIM/2))
        cv2.circle(clone, (int(data[i][XCOORD])+WINDOW_DIM/2, int(data[i][YCOORD])+WINDOW_DIM/2), 4, [0,0,255], -1) # FOR STU'S


#Get physical spatial differences
physical_distances = spatial.distance.pdist(hits, 'euclidean')
physical_distances = spatial.distance.squareform(physical_distances)
dbResult = DBSCAN(eps=opts.eps, min_samples=opts.minsamples, metric='precomputed').fit(physical_distances)

utils_cluster.drawClusterColorsDBSCAN(clone, hits, dbResult)
cv2.imwrite("output.jpg", clone)
