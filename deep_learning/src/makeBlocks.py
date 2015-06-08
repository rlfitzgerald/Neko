import cv2
import numpy as np
#from windowOb import windowOb
import sliding_window
import caffe.io
import skimage
import time

def makeBlocks(blockW, blockH, step, imageName):
	#init blockW and blockH should be parameters and step
	#import pdb; pdb.set_trace()
	#image = cv2.imread(imageName, cv2.CV_LOAD_IMAGE_GRAYSCALE)
	image = cv2.imread(imageName)
	image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
	start_time = time.time()
	
	blockArr = []
	i = 0
	for (x, y, window) in sliding_window.sliding_window(image, stepSize = step, windowSize=(blockW, blockH)):
		if window.shape[0] != blockH or window.shape[1] != blockW:
			continue #if the block is too small should I proccess it?

		#going to assume that the block is always a square
		#otherwise I'll need another parameter for the windowOb
		window = window[:, :, np.newaxis]
		window = skimage.img_as_float(window).astype(np.float32) 			
		blockArr.append(window.copy())

		i += 1
	#print ("---%s seconds ---" %(time.time() - start_time))                                                        
	return blockArr	
