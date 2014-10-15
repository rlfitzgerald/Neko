import cv2, sys, optparse
import pymeanshift as pms
from phasesym import *
from matplotlib import pyplot as plt

def meanShift(filename):

    img = cv2.imread(filename)
    (segmented_image, labels_image, number_regions) = pms.segment(img, spatial_radius=6, range_radius=4.5, min_density=50)
    return segmented_image

def blobDetect(img):
     #smooth image to reduce noise
    img1 = cv2.blur(img, (3,3))

    #threshold gray scale image
    (threshold, img_bw) = cv2.threshold(grayImg, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    #save black and white image (to debug)
    cv2.imwrite('Black_and_White.jpg', img_bw)

    #find contours in black and white image
    contours, hierarchy = cv2.findContours(img_bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >= 200 and area <= 2000:
            rect = cv2.minAreaRect(cnt)
            box = cv2.cv.BoxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(img1, [box], 0, (0, 0, 255), 2)

    cv2.imwrite('Boxes.jpg', img1)


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
    blobDetect(pha)

if __name__ == "__main__":
    sys.exit(main())
