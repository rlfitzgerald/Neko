from makeBlocks import makeBlocks
import cv2
import numpy as np
#import classifier
import argparse
#referenced nbviewer.ipython.org/github/BVLC/caffe/blob/master/examples/classification.ipynb
import caffe
import caffe.io
import time
import sys
import pdb
from nms import non_max_suppression_fast


WINDOW_DIM = 64
IMAGE_DIMS = (WINDOW_DIM,WINDOW_DIM)

start_time = time.time()
mean = np.load('./mean_test.npy')
net = caffe.Classifier('./cifar10_quick.prototxt','./cifar10_quick_iter_10000.caffemodel',mean=mean, image_dims=IMAGE_DIMS, raw_scale=255)
caffe.set_mode_gpu()
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())



picArr = makeBlocks(64, 64, 8, args["image"])
#picArr_sub = picArr[0:100000]
#predictions = net.predict(picArr_sub)
if len(picArr) < 100000:
	predictions = net.predict(picArr) 
	#change the prediction code to print the coords and make the circle
else:
	predictions = np.empty([len(picArr), 2])
	numChunks = len(picArr)/100000 #this will give the number of 200000 sized blocks
	lastIndex = len(picArr) - (100000 * numChunks)
	indices = []
	i = 0
	x = 0
	for i in range (0, 100000*(numChunks), 100000):
		indices.append((i, i+100000))
		print indices[x]
		x += 1
	indices.append((i + 100000,len(picArr)))
	print indices[x]

	for j in range(0,numChunks+1):
		start = indices[j][0]
		end = indices[j][1]
		#picArr_sub = picArr[start:end]
		predictions[start:end] = net.predict(picArr[start:end])
		
print("---%s seconds ---" %(time.time() - start_time))


#part two
#process the prediction data and make an output image
image = cv2.imread(args["image"])
image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
clone = image.copy()
xcoords = (image.shape[1]/8) - (8 - 1) #width of picture/stepSize - (stepSize - 1) 
ycoords = (image.shape[0]/8) - (8 - 1) #height of picture/stepSize - (stepSize - 1) 
boxes = []
for i in range(0, predictions.shape[0]):
    if predictions[i][1] > .4:
        x1 = ((i % xcoords)*8)
        y1 = ((i / xcoords)*8)
        x2 = x1 + WINDOW_DIM 
        y2 = y1 + WINDOW_DIM 
        boxes.append([x1,y1,x2,y2])
        circX = ((i % xcoords)*8)+32
        circY = ((i / xcoords)*8)+32 #caution! This may be a hacky fix!!!!
        cv2.circle(clone, (circX, circY), 4, 255, -1)

boxes = np.array(boxes)
boxes_nonmax = non_max_suppression_fast(boxes, 0.5)
for i in range(len(boxes_nonmax)):
    x1 = boxes_nonmax[i][0]
    y1 = boxes_nonmax[i][1]
    x2 = boxes_nonmax[i][2]
    y2 = boxes_nonmax[i][3]
    cv2.rectangle(clone, (x1,y1),(x2,y2), 255)

cv2.imwrite("output.jpg", clone)
