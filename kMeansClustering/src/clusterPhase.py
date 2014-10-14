import cv2, sys, optparse
import pymeanshift as pms
from phasesym import *
from matplotlib import pyplot as plt

def meanShift(filename):

    img = cv2.imread(filename)
    (segmented_image, labels_image, number_regions) = pms.segment(img, spatial_radius=6, range_radius=4.5, min_density=50)
    return segmented_image

def main(argv=None):
    if argv is None:
        argv = sys.argv

    desc = """%prog is a tool performs mean shift clustering and a phase symmetry transfromation\n
     on a given input image, in that order."""

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
        print "\n invalid argument(s) %s provided" % (str(args))
        parser.print_help()
        sys.exit(-1)

    #begin transform
    filename = args[0]
    img = meanShift(filename)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    pha, ori, tot, T = phasesym(img)
    pha *= 255/(np.max(np.max(pha)))
    cv2.imwrite("MSPS_Serial_" + filename, pha)

if __name__ == "__main__":
    sys.exit(main())
