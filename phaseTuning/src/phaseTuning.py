import cv2, time
import numpy as np
from phasesym import *
import pymeanshift as pms


def meanShift(img, sradius=6, rradius=4.5, mdensity=50):

    (segmented_image, labels_image, number_regions) = pms.segment(img, sradius, rradius, mdensity)
    return segmented_image


def phaseTuning(filename, scaleMin=5, scaleMax=10, orientationMin=6,orientationMax=16, kMax=30):

    #Performs phase symmetry transformation on a give for a given range across all parameters
    img = cv2.imread(filename)
    #img = meanShift(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    sigmaMult = [(0.85, 1.3),
                (0.75, 1.6),
                (0.65, 2.1),
                (0.55, 3),
                (0.45, 3.4)]

    #so ugly
    startTime = time.time()
    for scale in range(scaleMin, scaleMax):
        #scales loop
        for orient in range(orientationMin, orientationMax):
            #orientations loop
            for thisTuple in sigmaMult:
                sigOnF = thisTuple[0]
                mul = thisTuple[1]
                for kVal in range(1, kMax):
                    #k loop
                    itStartTime = time.time()
                    print "scale:" + str(scale) + " orient:" + str(orient) + " mult:" + str(mul) + \
                          " sigmaOnF:" + str(sigOnF) + " k:" + str(kVal)
                    
                    pha, ori, tot, T = phasesym(img, nscale=scale, norient=orient, mult=mul, sigmaOnf=sigOnF, k=kVal)

                    cv2.normalize(pha, pha, 0, 255, cv2.NORM_MINMAX)
                    pha = np.uint8(pha)
                    cv2.imwrite(filename + "_phase_symmetry_nscale:" + str(scale) + "_norient:" + str(orient)
                                + "_mult:" + str(mul) +"_sigmaOnF:" + str(sigOnF) + "_k:" + str(kVal) + "_.png", pha)
                    itEndTime = time.time()
                    print "Loop Time: " + str(itEndTime - itStartTime)

    endTime = time.time()
    print "Finished. \nTotal runtime: " + str(endTime - startTime)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    desc = """%prog is a tool that generates phase symmetyr transformations with the intent of
            determining the rpoper tuning for a dataset."""
    parser = optparse.OptionParser(description=desc, usage='Usage: ex) %prog imageFile.png')
    (opts, args) = parser.parse_args(argv)
    args = args[1:]

    #check to see if the user provided an output directory
    if len(args) == 0:
        print "\nNo input file provided"
        parser.print_help()
        sys.exit(-1)

    #check to see if the file system image is provided
    if len(args) > 6 or len(args) < 6:
        print "\ninvalid argument(s) %s provided" %(str(args))
        parser.print_help()
        sys.exit(-1)

    #begin transform
    filename = argv[1]
    scaleMi = int(argv[2])
    scaleMa = int(argv[3])
    orientMi = int(argv[4])
    orientMa = int(argv[5])
    k = int(argv[6])

    #find and box proper blobs
    phaseTuning(filename, scaleMin=scaleMi, scaleMax=scaleMa, orientationMin=orientMi, orientationMax=orientMa, kMax=k)


if __name__ == "__main__":
    sys.exit(main())





