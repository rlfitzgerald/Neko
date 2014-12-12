This readme explains how to properly use the current version of the car detecting software.


Our program depends on the following tools:

python 2.7.6
matplotlib 1.4.2
openCV 2.4.8
numpy 1.9.0
scipy 0.14.0
pymeanshift 0.2.1 


DESCRIPTION:

lowpassfilter.py and phasesym.py are a port of some MATLAB code provided by Peter Kovesi of
the Univeristy of Western Austrailia's department of Computer Science. This code is used for
the overall phase symmetry calculation. The original MATLAB source code is provided in the 
"references" folder, along with the paper in which the MATLAB source was referenced and the phase
symmetry calculation is explained.

In order for this program to function properly, a minimum of two inputs are needed from the user.
Primarily, the user must provide an image upon which the provided software will search through.
In addition, the user must select a reference vehicle from the image. This reference should contain
only one vehicle, and the vehicle should be easily identifiable within the reference image. 
Additionally, the reference image should be indicitive of the dataset's resolution and level of 
detail. Simply put, the reference image should be of a single vehicle, cropped out of the image to
be searched.

For testing purposes, both a sample reference car image (singleCar.png) and a sample dataset
(structure.jpg) have been included. In order to run the program with this input data, do the 
folowing in the working directory the program has been extracted to:

python histogram.py --ref=singleCar.png structure.jpg

NOTE: THE SIZE OF THE PASSED REFRENCE IMAGE MUST BE ODD AND SQUARE (i.e. 25x25)


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
    --edgeMin         specify minimum hysteresis value for edge detection. Defaults to 100.
    --edgeMax         specify maximum hysteresis value for edge detection. Defaults to 200.
    --ref             specify reference car image. THIS FLAG UST BE THROWN.
    --tol             specify shape description tolerance. Defaults to 0.07.
    --eps             specify maximum epsilon value for DBSCAN clustering algorithm. Defaults to 15.
    --min_samples     specify the number of minimum samples that constitute a cluster during DBSCAN. Defaults to 1.


Running this software on an image that requires non-deault flags will resemble the following:

python histogram.py --blur=1 --hmin=1 --wmin=1 --hmax=13 --wmax=13 --amin=1 --amax=10 --srad=3 --rrad=5 --den=2 --tol=0.60 --arat=0.33 
	--ref=<Name of reference car image> <Name of image to be searched>  

i.e. 
python histogram.py --blur=1 --hmin=1 --wmin=1 --hmax=13 --wmax=13 --amin=1 --amax=10 --srad=3 --rrad=5 --den=2 --tol=0.60 --arat=0.33 
	--ref=singleCar_la_port.png la_port_cropped.png



The final output of this program is set of images:
   Centroids.jpg:        image containing all possible cars (noted with red dot)
   Boxes_Centroids.jpg:  image containing a filtered set of centroids that are most likely to be cars based on the shape description stage
   clusterColors.jpg:    image containing centroids based on DBSCAN. Ideally these clusters represent a car




