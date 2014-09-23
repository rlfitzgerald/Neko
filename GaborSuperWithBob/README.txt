
DESCRIPTION:


This progam takes the Gabor Wavelet Transform of an input image 40 times.
Specifically, the transform is taken at 8 different angles, each at 5 
different scales. The result of the transform is used to attempt a phase
symmetry calculation. This calculation should, in theory, provide us with 
reigons of high symmetry in the image. The main motivating factor behind
this approach is simple: most manmade objects tend to be highly symmetrical,
especially vehicles. Using these reigons of symmetry would allow us to detect
ROI's with a higher degree of accuracy. However, after further examination
it was discovered that the log Gabor Wavelet Transformation is needed instead
of the Gabor Wavelet Transoformation. This is why this method prodiuced incorrect
results, and has since been abandoned.

Example usage:
	
	python GaborTransform.py inputImage.png
