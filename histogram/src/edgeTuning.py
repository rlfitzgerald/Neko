import cv2, sys, os
from optparse import OptionParser

def edgeTuning(filename):

    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blurImg = cv2.blur(img, (3,3))
    GImg = cv2.GaussianBlur(img, (3,3), 0)
    MImg = cv2.medianBlur(img, 3)

    low = range(20, 260, 10)
    high = range(250, 10, -10)

    dirName = 'outputImagesBlur'
    if not (os.path.isdir(dirName)):
        #create subdirectory if it does not already exist
        os.mkdir(dirName)

    for i in high:
        for j in low:
            if j < i:
                edge = cv2.Canny(blurImg, j, i)
                edgeName = filename + "_edges_low:%d_high:%d_.jpg" % (j, i)
                cv2.imwrite(os.path.join(dirName, edgeName), edge)

    dirName = 'outputImagesGaussian'
    if not (os.path.isdir(dirName)):
        #create subdirectory if it does not already exist
        os.mkdir(dirName)

    for i in high:
        for j in low:
            if j < i:
                edge = cv2.Canny(GImg, j, i)
                edgeName = filename + "_edges_low:%d_high:%d_.jpg" % (j, i)
                cv2.imwrite(os.path.join(dirName, edgeName), edge)

    dirName = 'outputImagesMedian'
    if not (os.path.isdir(dirName)):
        #create subdirectory if it does not already exist
        os.mkdir(dirName)

    for i in high:
        for j in low:
            if j < i:
                edge = cv2.Canny(MImg, j, i)
                edgeName = filename + "_edges_low:%d_high:%d_.jpg" % (j, i)
                cv2.imwrite(os.path.join(dirName, edgeName), edge)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    desc = """%prog is a tool that performs Canny edge detection on an input image with incremental changes in\n
     threshold value in an effort to find an appropriate set of threshold values for a given input image."""

    parser = OptionParser()
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

    filename = args[0]
    edgeTuning(filename)

if __name__ == "__main__":
    sys.exit(main())

