#!/usr/bin/env python
'''
Usage:
openimage.py [image_filename] --slice --rotate
'''

import numpy as np
import cv2, sys, time, os
import pdb

positive_image_count = 0
negative_image_count = 0
neg_count = 0
current_image = ""

image_height = 64
image_width = 64

positive_image_folder = "positives"
negative_image_folder = "negatives"
center = (image_height/2, image_width/2)
one_eighty = cv2.getRotationMatrix2D(center, 180, 1.0)
ninety = cv2.getRotationMatrix2D(center, 90, 1.0)
two_seventy = cv2.getRotationMatrix2D(center, 270, 1.0)

def rotate_single(raw_name, directory, img):
	image_width = img.shape[0]
	image_length = img.shape[1]
	directory = directory
	center = (image_width/2, image_height/2)

	rotated90 = cv2.warpAffine(img, ninety, (image_width, image_height))
	cv2.imwrite(directory + raw_name + "-90" + extension, rotated90)

	rotated180 = cv2.warpAffine(img, one_eighty, (image_width, image_height))
	cv2.imwrite(directory + raw_name + "-180" + extension, rotated180)

	rotated270 = cv2.warpAffine(img, two_seventy, (image_width, image_height))
	cv2.imwrite(directory + raw_name + "-270" + extension, rotated270)

	flipped = cv2.flip(img,0)
	cv2.imwrite(directory + raw_name + "-flip" + extension, flipped)

	flopped = cv2.flip(img,1)
	cv2.imwrite(directory + raw_name + "-flop" + extension, flipped)

def save_positive_ROI(x1, x2, y1, y2, pic):
	"Show (green) and save positive ROI"
	global positive_image_count
	##
	directory = str(os.getcwd() + "/" + positive_image_folder + "/")
	image_name = current_image[:-4] + str(positive_image_count)
	image_name = 'pos_'+image_name
	## roi info
	roi = pic[y1:y2, x1:x2]
	cv2.namedWindow("ROI", cv2.WINDOW_NORMAL)
	cv2.imshow("ROI", roi)

	## original image
	## e.g., /tmp/X/y1560-0.jpg
	picname = directory + image_name+"-"+str(positive_image_count) + ".jpg"
	cv2.imwrite(picname, roi)

	## rotate the image 90, 180, 270, flip, flop
	if rot_flag == 1:
		rotate_single(image_name, directory, roi)

	## reset
	for w in range(x1, x2)[::2]:
		for h in range (y1, y2)[::2]:
			#pic[h, w] = 0
			pic[h, w] = [0, 255, 0]
	cv2.imwrite(sys.argv[1], pic)	# This line write over the original image with "green haze"

	pic2 = cv2.imread("test.jpg")
	for w in range(x1,x2):
		for h in range(y1, y2):
			pic2[h, w] = 0
	cv2.imwrite("test.jpg", pic2)

def save_negative_ROI(x1, x2, y1, y2, pic):
	"Show (green) and save positive ROI"
	global negative_image_count
	##
	directory = str(os.getcwd() + "/" + negative_image_folder + "/")
	image_name = current_image[:-4]+str(negative_image_count)
	image_name = 'neg_'+image_name
	## roi info
	roi = pic[y1:y2, x1:x2]
	cv2.namedWindow("ROI", cv2.WINDOW_NORMAL)
	cv2.imshow("ROI", roi)

	## original image
	## e.g., /tmp/X/y1560-0.jpg
	picname = directory + image_name + "-" + str(negative_image_count) + ".jpg"
	cv2.imwrite(picname, roi)

	## rotate the image 90, 180, 270, flip, flop
	if rot_flag ==1:
		rotate_single(image_name, directory, roi)
	## reset
	for w in range(x1, x2)[::2]:
		for h in range(y1, y2)[::2]:
			#pic[h, w] = 0
			pic[h, w] = [0, 0, 255]
	cv2.imwrite(sys.argv[1], pic)    # line writes over the original image with "green haze"

	pic2 = cv2.imread("test.jpg")
	for w in range(x1, x2): 
		for h in range(y1, y2):
			pic2[h, w] = 0
	cv2.imwrite("test.jpg", pic2)

def draw_positive_box(x, y, pic):
	"Get a box centered on the point clicked"
	global positive_image_count
	x1 = x - (image_width/2)
	x2 = x + (image_width/2)
	y1 = y - (image_height/2)
	y2 = y + (image_height/2)
	save_positive_ROI(x1, x2, y1, y2, pic)
	positive_image_count = positive_image_count + 1

def draw_negative_box(x, y, pic):
	"Get a box centered on the point clicked"
	global negative_image_count
	x1 = x - (image_width/2)
	x2 = x + (image_width/2)
	y1 = y - (image_height/2)
	y2 = y + (image_height/2)
	save_negative_ROI(x1, x2, y1, y2, pic)
	negative_image_count = negative_image_count + 1

def onmouse(event, x, y, flags, param):
	"Send point coordinates to draw_box function"
	if event == cv2.EVENT_LBUTTONDOWN:
		draw_positive_box(x, y, img)
	if event == cv2.EVENT_MBUTTONDOWN:
		draw_negative_box(x, y, img)

def slice_image(pic):
	"Slice remainingimage and store in negative_image_folder upon exit"
	global neg_count
	directory = str(os.getcwd() + "/" + negative_image_folder + "/")
	picture = cv2.imread(pic)
	height, width = picture.shape[:2]
	num_y = height/64
	num_x = width/64

	cur_y = 0
	for h in range(num_y):
		cur_x = 0
		for w in range(num_x):
			roi = picture[cur_y:(cur_y+64), cur_x:(cur_x+64)]
			# save image
			picname = directory + "/" + str(neg_count) + current_image[(current_image.index('.')):]
			cv2.imwrite(picname, roi)
			cur_x = cur_x + 65
			neg_count = neg_count + 1
		cur_y = cur_y + 65
	os.remove(pic)

# for a color image:
img = cv2.imread(sys.argv[1])
# for a B&W image:
#img = cv2.imread(sys.argv[1], )
current_image = sys.argv[1]

# copy current image so that it's not destroyed
current_image_copy = np.copy(img)
x = (sys.argv[1]).index(".")
extension = (sys.argv[1])[x:]
cv2.imwrite((sys.argv[1])[:x] + "_original" + extension, current_image_copy)

# copy current image again for negative-slicing
neg_img = np.copy(img)
cv2.imwrite("test.jpg", neg_img)

# look for/create positive/negative image folders
if not os.path.exists(positive_image_folder):
	os.makedirs(positive_image_folder)
if not os.path.exists(negative_image_folder):
	os.makedirs(negative_image_folder)

cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("image", img.shape[1], img.shape[0])
cv2.setMouseCallback("image", onmouse)
os.system('clear')
print "Left-click to select a positive ROI,"
print "Middle-click to select a negative ROI,"
print "ESC to exit."

rot_flag = 0
# Main program loop
if "--rotate" in sys.argv:
	rot_flag = 1
while(1):
	cv2.imshow("image", img)
	if cv2.waitKey(20) & 0xFF == 27:
		break

cv2.destroyAllWindows()
	

