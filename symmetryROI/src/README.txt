TL;DR VERSION
-------------

Specify a window size equal to the largest dimension of the car
(i.e. length) in pixels via the --win option.

   Ex) python symmetryROI.py --win=45 input_image.jpg

Suggested workflow for this option:
 * open input image in image viewer
 * measure longest car dimension (i.e. length), leave a 1-2 pixel buffer around car
 * call program with this window size (make sure its odd)



RTFM VERSION
------------

This readme explains how to properly use the current version of the car detecting software.


Our program depends on the following tools:

python 2.7.6
openCV 2.4.8
numpy 1.9.0
pymeanshift 0.2.1 


DESCRIPTION:

lowpassfilter.py and phasesym.py are a port of some MATLAB code provided by Peter Kovesi of
the Univeristy of Western Austrailia's department of Computer Science. This code is used for
the overall phase symmetry calculation. The original MATLAB source code is provided in the 
"references" folder, along with the paper in which the MATLAB source was referenced and the phase
symmetry calculation is explained.

In order for this program to function properly, the user must specify a window size:

	python symmetryROI.py --win=45 structure.jpg


There are a large number of command line parameters that can be set at execution time that will
affect the accuracy of the program. What follows is a description of those options:

    --scale           specify number of phasesym scales. Defaults to 4.
    --ori             specify number of phasesym orientations. Defauls to 6.
    --mult            specify multiplier for phasesym. Defaults to 3.0.
    --sig             specify sigma on frequncy for phasesym. Defaults to 0.55.
    --k               specify k value for phasesym. Defaults to 1.
    --blur            specify blur width value N for NxN blur operation. Defaults to 3.
    --srad            specify spatial radius for mean shift. Defaults to 5.
    --rrad            specify radiometric radius for mean shift. Defaults to 6.
    --den             specify pixel density value for mean shift. Defaults to 10.
    --amin            specify blob minimum area for boxing.Defaults to 5.
    --amax            specify blob maximum area for boxing. Defaults to 400.
    --wmin            specify box minimum width acceptance. Defaults to 3. 
    --wmax            specify box maximum width acceptance. Defaults to 35.
    --hmin            specify box minimum height acceptance. Defaults to 2.
    --hmax            specify box maximum height acceptance. Defaults to 55
    --arat            specify minimum box aspect ratio for acceptance. Defaults to 0.25.
    --win             specify search window size, default matches reference image size, EITHER THIS FLAG OR --ref UST BE THROWN, NOT BOTH.


Running this software on an image that requires non-deault flags will resemble the following:

python symmetryROI.py --blur=1 --hmin=1 --wmin=1 --hmax=13 --wmax=13 --amin=1 --amax=10 --srad=3 --rrad=5 --den=2 --arat=0.33 input_image.jpg 

i.e. 
python symmetryROI.py --blur=1 --hmin=1 --wmin=1 --hmax=13 --wmax=13 --amin=1 --amax=10 --srad=3 --rrad=5 --arat=0.33 la_port_cropped.png



The output of this program is two directories whose names are prepended with the input image filename:
	 filename_metadata/:    contains intermediate image files used for troubleshooting

   filename_windowTiles/: contains Centroids.jpg and image patches whose centroid is an area of symmetry
			 Centroids.jpg:     image containing all possible cars (noted with red dot)
       win_Y_X.jpg:       image tiles with centroid (Y,X) coordinates




