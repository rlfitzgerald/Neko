
DESCRIPTION:

blobs.py is a simple blob detection method applied to a sample image using openCV.
This method illustrates some of the difficulties and challenges inherent to this 
computer vision problem, such as seperating cars from their shadows. This program
takes an input image, detects all the blobs in the image, and draws a box around a
detected blob if the blob in question is within certain size requirements. These 
size parameters were tuned by hand, and are only a loose metric.

Example usage:
	
	python blobs.py inputImage.jpg

Note: input image need not be .jpg. File format can be any image format supported
      by the imread(...) function provided by openCV. 
