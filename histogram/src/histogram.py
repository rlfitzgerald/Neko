import sys, os
#from phasesym import *
from PhaseSymmetry.src.phasesym import *
import cv2, optparse
import numpy as np
import pymeanshift as pms
from Hist import RadAngleHist


DEBUG = False

#def getCentroids(thresh_img, original_img, AMIN, AMAX, WMIN, WMAX, HMIN, HMAX, ARATIO):
#
#    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#
#    centroids = []
#    for cnt in contours:
#        area = cv2.contourArea(cnt)
#        if area >= AMIN and area <= AMAX:
#            x,y,w,h = cv2.boundingRect(cnt)
#            if w < WMAX and h < HMAX and w > WMIN and h > HMIN:
#                aspectRatio = 0
#                if w == min(w, h):
#                    aspectRatio = float(w)/h
#                else:
#                    aspectRatio = float(h)/w
#
#                if aspectRatio > ARATIO:
#                    print "x=%d y=%d w=%d h=%d" % (x, y, w, h)
#                    rect = cv2.minAreaRect(cnt)
#                    box = cv2.cv.BoxPoints(rect)
#                    box = np.int0(box)
#
#                    #if DEBUG:
#                    #    cv2.drawContours(original_img, [box], 0, (255, 0, 0), 2)
#
#                    moments = cv2.moments(cnt)
#                    centroid_x = int(moments['m10']/moments['m00'])
#                    centroid_y = int(moments['m01']/moments['m00'])
#                    centroid = (centroid_y, centroid_x)
#                    centroids.append(centroid)
#                    if DEBUG:
#                        original_img[centroid] = [0, 0, 255]
#
#    cv2.imwrite("Boxes + centroids.jpg", original_img)
#    return centroids

def drawBox(img, contour):
    """
    INPUTS:
        img      = image to be drawn on
        contours = contour objects
    OUTPUTS:
        None 
    """
    rect = cv2.minAreaRect(contour)
    box = cv2.cv.BoxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img, [box], 0, (255, 0, 0), 2)
    

def getCentroids(contours):
    """
    INPUTS:
        contours = list of contour objects
    OUTPUTS:
        centroids = list of centroids corresponding to the input contours
    """
    centroids = []
    for cnt in contours:
        moments = cv2.moments(cnt)
        centroid_x = int(moments['m10']/moments['m00'])
        centroid_y = int(moments['m01']/moments['m00'])
        centroid = (centroid_y, centroid_x)
        centroids.append(centroid)

    return centroids

def getContours(thresh_img, AMIN, AMAX, WMIN, WMAX, HMIN, HMAX, ARATIO):
    """
    INPUTS:
        thresh_img = thresholded image (black and white)
        AMIN       = blob minimum area
        AMAX       = blob maximum area
        WMIN       = minimum contour bounding rectangle width
        WMAX       = maximum contour bounding rectangle width
        HMIN       = minimum contour bounding rectangle height
        HMAX       = maximum contour bounding rectangle height
        ARATIO     = minimum contour bounding rectangle aspect ratio
    OUTPUTS:
        filteredContours = list of contours filtered according to input params
    """
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    filteredContours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >= AMIN and area <= AMAX:
            x,y,w,h = cv2.boundingRect(cnt)
            if w < WMAX and h < HMAX and w > WMIN and h > HMIN:
                aspectRatio = 0
                if w == min(w, h):
                    aspectRatio = float(w)/h
                else:
                    aspectRatio = float(h)/w

                if aspectRatio > ARATIO:
                    #print "x=%d y=%d w=%d h=%d" % (x, y, w, h)
                    filteredContours.append(cnt)

    return filteredContours


#def getImageWindow(img,x,y,w,h):
def getImageWindow(img,y,x,h,w):
    """
    INPUTS:
        img = input image
        x,y = point in image to be the center of the returned window
        w,h = height and width of the windo
    OUTPUTS:
        window = a wxh size window containing a slice of the image
                 centered on x,y. The window will be padded with 
                 zeros for border cases
    """
    imgY,imgX,imgZ = img.shape 
    window = np.zeros((h,w,imgZ))

    winCenterX = -1
    winCenterY = -1

    #account for even/odd window sizes
    if w%2:
        winCenterX = int(np.ceil(w/float(2)))
    else:
        winCenterX = w/2

    if h%2:
        winCenterY = int(np.ceil(h/float(2)))
    else:
        winCenterY = h/2

    #get the upper and lower bounds of the image slice
    lowX = max(x-winCenterX,0)
    highX = min(imgX,x+winCenterX)
    lowY = max(y-winCenterY,0)
    highY = min(imgY,y+winCenterY)

    #get the offset X and Y distances between the centroid (x,y) and the 
    #edge of the image slice
    offsetLowX = x - lowX
    offsetLowY = y - lowY
    offsetHighX = highX - x
    offsetHighY = highY - y


    #get the window upper and lower bounds where the image
    #slice is to be placed
    XwinLow = winCenterX - offsetLowX
    YwinLow = winCenterY - offsetLowY
    XwinHigh = winCenterX + offsetHighX
    YwinHigh = winCenterY + offsetHighY

    try:
        window[YwinLow:YwinHigh-1,XwinLow:XwinHigh-1,:] = img[lowY:highY-1,lowX:highX-1,:]
    except:
        import pdb; pdb.set_trace()

    return np.uint8(window)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    desc = """%prog is a tool performs mean shift clustering and a phase symmetry transfromation\n
     on a given input image, in that order."""

    parser = optparse.OptionParser(description=desc, usage='Usage: ex) %prog imageFile.png')
    parser.add_option('--scale', help='specify number of phasesym scales', dest='NSCALE', default=4, type="int")
    parser.add_option('--ori', help='specify number of phasesym orientations', dest='NORIENT', default=6, type="int")
    parser.add_option('--mult', help='specify multiplier for phasesym', dest='MULT', default=3.0, type="float")
    parser.add_option('--sig', help='specify sigma on frequncy for phasesym', dest='SIGMAONF', default=0.55, type="float")
    parser.add_option('--k', help='specify k value for phasesym', dest='K', default=1, type="int")
    parser.add_option('--blur', help='specify blur width value N for NxN blur operation', dest='BLUR', default=3, type="int")
    parser.add_option('--srad', help='specify spatial radius for mean shift', dest='SRAD', default=5, type="int")
    parser.add_option('--rrad', help='specify radiometric radius for mean shift', dest='RRAD', default=6, type="int")
    parser.add_option('--den', help='specify pixel density value for mean shift', dest='DEN', default=10, type="int")
    parser.add_option('--amin', help='specify blob minimum area for boxing', dest='AMIN', default=5, type="int")
    parser.add_option('--amax', help='specify blob maximum area for boxing', dest='AMAX', default=400, type="int")
    parser.add_option('--wmin', help='specify box minimum width acceptance', dest='WMIN', default=3, type="int")
    parser.add_option('--wmax', help='specify box maximum width acceptance', dest='WMAX', default=35, type="int")
    parser.add_option('--hmin', help='specify box minimum height acceptance', dest='HMIN', default=2, type="int")
    parser.add_option('--hmax', help='specify box maximum height acceptance', dest='HMAX', default=55, type="int")
    parser.add_option('--arat', help='specify minimum box aspect ratio for acceptance', dest='ARATIO', default=0.25, type="float")
    parser.add_option('--edgeMin', help='specify minimum hysteresis value for edge detection', dest='EDGEMIN', default=100, type="int")
    parser.add_option('--edgeMax', help='specify maximum hysteresis value for edge detection', dest='EDGEMAX', default=200, type="int")
    parser.add_option('--ref', help='specify reference car image', dest='MASTERIMG', default="")
    parser.add_option('--win', help='specify search window size', dest='WINSZ', default=55, type="int")
    parser.add_option('--tol', help='specify shape description tolerance', dest='TOL', default=0.07, type="float")
    

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


    NSCALE = opts.NSCALE
    NORIENT = opts.NORIENT
    MULT = opts.MULT
    SIGMAONF = opts.SIGMAONF
    K = opts.K
    BLUR = (opts.BLUR, opts.BLUR)
    SRAD = opts.SRAD
    RRAD = opts.RRAD
    DEN = opts.DEN
    AMIN = opts.AMIN
    AMAX = opts.AMAX
    WMAX = opts.WMAX
    WMIN = opts.WMIN
    HMAX = opts.HMAX
    HMIN = opts.HMIN
    ARATIO = opts.ARATIO
    EDGEMIN = opts.EDGEMIN
    EDGEMAX = opts.EDGEMAX
    WINSZ = opts.WINSZ 
    TOL = opts.TOL
    masterImg = ""
    masterHist = None

    if len(opts.MASTERIMG) > 0:
        masterImg = cv2.imread(opts.MASTERIMG)

        h, w, z = masterImg.shape
        if w%2:
            x = int(np.ceil(w/float(2)))
        else:
            x = w/2
        if h%2:
            y = int(np.ceil(h/float(2)))
        else:
            y = h/2
        masterHist = RadAngleHist(masterImg, 180, y, x)
    else:
        masterImg = cv2.imread('singleCar.png')
        masterHist = RadAngleHist(masterImg, 180, 27, 29)

    #begin transform
    filename = args[0]
    basename = os.path.splitext(filename)[0]
    img = cv2.imread(filename)

    grayImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imwrite(basename+"_gray.png", grayImg)
    pha, ori, tot, T = phasesym(grayImg, nscale=NSCALE, norient=NORIENT, minWaveLength=3, mult=MULT, sigmaOnf=SIGMAONF, k=K, polarity=0)
    pha = cv2.normalize(pha, pha, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    pha = np.uint8(pha)
    cv2.imwrite(basename + "_PS" + "_%d_%d_%.2f_%.2f_%d.png" % (NSCALE, NORIENT, MULT, SIGMAONF, K), pha)
    cv2.imwrite(basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_ori.png" % (NSCALE, NORIENT, MULT, SIGMAONF, K), ori)
    np.savetxt('python_ori.txt',ori)

    pha = cv2.blur(pha, BLUR)
    cv2.imwrite(basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_B_%d_%d.png" % (NSCALE, NORIENT, MULT, SIGMAONF, K, BLUR[0], BLUR[1]), pha)
    pha = cv2.cvtColor(pha, cv2.COLOR_GRAY2RGB)
    pha = cv2.cvtColor(pha, cv2.COLOR_RGB2LUV)


    (segmented_image, labels_image, number_regions) = pms.segment(pha, spatial_radius=SRAD, range_radius=RRAD, min_density=DEN)
    segmented_image=cv2.normalize(segmented_image, segmented_image, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    segmented_image = np.uint8(segmented_image)
    segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_LUV2RGB)
    segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_RGB2GRAY)
    cv2.imwrite(basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_B_%d_%d_MS_%d_%d_%d.png" % (NSCALE, NORIENT, MULT, SIGMAONF, K, BLUR[0], BLUR[1], SRAD, RRAD, DEN), segmented_image)


    #ori = np.uint8(ori)
    #(ori, labels_image, number_regions) = pms.segment(ori, spatial_radius=SRAD, range_radius=RRAD, min_density=DEN)
    #ori=cv2.normalize(ori, ori, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    #ori = np.uint8(ori)
    #cv2.imwrite(basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_B_%d_%d_MS_%d_%d_%d_ori.png" % (NSCALE, NORIENT, MULT, SIGMAONF, K, BLUR[0], BLUR[1], SRAD, RRAD, DEN), ori)


    thresh_img = cv2.adaptiveThreshold(segmented_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 0)
    cv2.imwrite(basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_B_%d_%d_MS_%d_%d_%d_T.png" % (NSCALE, NORIENT, MULT, SIGMAONF, K, BLUR[0], BLUR[1], SRAD, RRAD, DEN), thresh_img)


    #get centroids
    contours = getContours(thresh_img, AMIN, AMAX, WMIN, WMAX, HMIN, HMAX, ARATIO)
    centroids = getCentroids(contours)
    
    #cv2.imwrite(basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_B_%d_%d_MS_%d_%d_%d_A_%d_%d_W_%d_%d_H_%d_%d_R_%.2f.png" % (NSCALE, NORIENT, MULT, SIGMAONF, K, BLUR[0], BLUR[1], SRAD, RRAD, DEN, AMIN, AMAX, WMIN, WMAX, HMIN, HMAX, ARATIO), img)

    histograms = []


    dirName = 'windowTiles'
    if not (os.path.isdir(dirName)):
        #create subdirectory if it does not already exist
        os.mkdir(dirName)

    outputImg = img.copy()
    #ori = np.loadtxt('matlab_ori.txt',delimiter=',')

    for cen,cnt in zip(centroids,contours):
        #print cen
        #win = getImageWindow(img, cen[0],cen[1],26,52)

        #import pdb; pdb.set_trace()
        #win = getImageWindow(img, cen[0],cen[1],55,55)   #correct
        win = getImageWindow(img, cen[0],cen[1],WINSZ,WINSZ)   #correct


        #win = getImageWindow(img, cen[0],cen[1],51,51)
        filename = "win_%d_%d.jpg" % (cen[0], cen[1])
        cv2.imwrite(os.path.join(dirName, filename), win)
        histogram = RadAngleHist(win, 90+ori[cen[0], cen[1]],cen[0],cen[1])
        #print ori[cen[0], cen[1]]
        print masterHist.compare(histogram)
#        if masterHist.compare(histogram, dist=60) == 0:
#            histograms.append(histogram)
        #if masterHist.compare(histogram) < 0.07:
        if masterHist.compare(histogram) < TOL:
            drawBox(outputImg, cnt)
            # boxedImg = img.copy()
            # drawBox(boxedImg,cnt)
            # filename = "win_box_%d_%d.jpg" % (cen[0], cen[1])
            # cv2.imwrite(os.path.join(dirName, filename), boxedImg)
    dirName = ""
    filename = "Boxes_+_Centroids.jpg"
    cv2.imwrite(os.path.join(dirName, filename), outputImg)


if __name__ == "__main__":
    sys.exit(main())
