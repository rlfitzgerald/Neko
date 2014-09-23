import numpy as np
import bob
import sys
import optparse
import cv2
from matplotlib import pyplot


def gabor(filename):
    #read image
    imArray = cv2.imread(filename)
    imArray = cv2.cvtColor(imArray, cv2.COLOR_RGB2GRAY)
    
    #transform image
    kernel = bob.ip.GaborKernel(imArray.shape, (1,0))
    GaborImage = kernel(imArray)
    abs = np.abs(GaborImage)
    phase = np.angle(GaborImage)
    real = np.real(GaborImage)
    
    #write images
    absName = ("Magnitude_%s" %(str(filename)))
    phaseName = ("Phase_%s"  %(str(filename)))
    realName = ("Real_%s" %(str(filename)))
    cv2.imwrite(absName, abs)
    cv2.imwrite(phaseName, phase)
    cv2.imwrite(realName, real)
    
    #show images
    pyplot.figure(figsize=(20,5))
    pyplot.subplot(141)
    pyplot.imshow(imArray, cmap='gray')
    pyplot.title("Original Image")
    
    pyplot.subplot(142)
    pyplot.imshow(abs, cmap='gray')
    pyplot.title("Magnitude Layer")
    
    pyplot.subplot(143)
    pyplot.imshow(phase, cmap='gray')
    pyplot.title("Phase Layer")
    
    pyplot.subplot(144)
    pyplot.imshow(real, cmap='gray')
    pyplot.title("Real Layer")
    
    pyplot.show()
    

def main(argv=None):
    if argv is None:
        argv = sys.argv

    desc = """%prog is a tool performs the Gabor wavelet transform on an input image at a single scale."""

    parser = optparse.OptionParser(description=desc, usage='Usage: ex) %prog imageFile.png')

    (opts, args) = parser.parse_args(argv)
    args = args[1:]

    #check to see if the user provided an output directory
    if len(args) == 0:
        print "\nNo input file provided"
        parser.print_help()
        sys.exit(-1)
        
    #check to see if the file system image is provided
    if len(args) > 1:
        print "\ninvalid argument(s) %s provided" %(str(args))
        parser.print_help()
        sys.exit(-1)

    #begin transform
    filename = args[0]
    gabor(filename)


if __name__ == "__main__":
    sys.exit(main())

