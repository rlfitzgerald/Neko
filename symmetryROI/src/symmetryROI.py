import sys, os
from phasesym import *
import cv2, optparse
import numpy as np
import pymeanshift as pms
from collections import defaultdict
import logging
import phasesymLogger
np.set_printoptions(precision=3)
np.set_printoptions(linewidth=200)


DEBUG = False
logger = None


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
                    filteredContours.append(cnt)

    return filteredContours


def drawCentroids(img, centroids):
    for cen in centroids:
        cv2.circle(img,(cen[1],cen[0]),1,(0,0,255),-1)


def checkopts(parser, opts):
    if not opts.WINSZ%2 and opts.WINSZ >= 3:
        logger.debug("Invalid user specified window size. --win=%d"%(opts.WINSZ))
        parser.error("option --win must be an odd integer greater than or equal to 3")

    if opts.BLUR == -1:
        if opts.WINSZ >= 35:
            opts.BLUR = 3
        else:
            opts.BLUR = 1
    else:
        if not opts.BLUR%2 and opts.BLUR >= 1:
            logger.debug("Invalid user specified blur size. --blur=%d"%(opts.BLUR))
            parser.error("option --blur must be an odd integer greater than or equal to 1")

    if opts.SRAD == -1:
        opts.SRAD = int(np.maximum(3,np.floor(np.sqrt(opts.WINSZ))))
    if opts.DEN == -1:
        opts.DEN = int(np.maximum(2,np.floor(np.sqrt(opts.WINSZ))))

    if opts.TRAD == -1:
        opts.TRAD = int(np.maximum(3,opts.WINSZ/2))

        # must be odd
        if opts.TRAD % 2 == 0:
            opts.TRAD = opts.TRAD+1

    if opts.WMIN == -1:
        #opts.WMIN = int(np.maximum(3,np.floor((opts.WINSZ*0.65*0.06))))
        opts.WMIN = 1
    if opts.HMIN == -1:
        #opts.HMIN = int(np.maximum(3,np.floor(opts.WINSZ *0.06)))
        opts.HMIN = 1
    if opts.WMAX == -1:
        #opts.WMAX = int(np.maximum(opts.WMIN,np.floor(opts.WINSZ*0.65)))
        opts.WMAX = opts.WINSZ
    if opts.HMAX == -1:
        opts.HMAX = opts.WINSZ
    if opts.AMIN == -1:
        opts.AMIN = opts.WMIN*opts.HMIN
    if opts.AMAX == -1:
        opts.AMAX = opts.WMAX*opts.HMAX

    return    




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
    parser.add_option('--blur', help='specify blur width value N for NxN blur operation', dest='BLUR', default=-1, type="int")          
    parser.add_option('--srad', help='specify spatial radius for mean shift', dest='SRAD', default=-1, type="int")                      
    parser.add_option('--rrad', help='specify radiometric radius for mean shift', dest='RRAD', default=6, type="int")
    parser.add_option('--den', help='specify pixel density value for mean shift', dest='DEN', default=-1, type="int")                    
    parser.add_option('--trad', help='specify the pixel neighborhood for thresholding', dest='TRAD', default=-1, type="int")            
    parser.add_option('--amin', help='specify blob minimum area for boxing', dest='AMIN', default=-1, type="int")                       
    parser.add_option('--amax', help='specify blob maximum area for boxing', dest='AMAX', default=-1, type="int")                       
    parser.add_option('--wmin', help='specify box minimum width acceptance', dest='WMIN', default=-1, type="int")                       
    parser.add_option('--wmax', help='specify box maximum width acceptance', dest='WMAX', default=-1, type="int")                       
    parser.add_option('--hmin', help='specify box minimum height acceptance', dest='HMIN', default=-1, type="int")                      
    parser.add_option('--hmax', help='specify box maximum height acceptance', dest='HMAX', default=-1, type="int")                      
    parser.add_option('--arat', help='specify minimum box aspect ratio for acceptance', dest='ARATIO', default=0.25, type="float")
    parser.add_option('--win', help='specify search window size, default matches reference image size', dest='WINSZ', default=-1, type="int")
    parser.add_option('--resize', help='specify the dimensions to resize image Ex) 64x64', dest='RESIZE', default="", type="string")


    (opts, args) = parser.parse_args(argv)
    args = args[1:]

    # Check to see if the user provided an input image
    if len(args) == 0:
        parser.print_help()
        parser.error("No input file provided")

    # Check to see if the file system image is provided
    if len(args) > 1:
        parser.print_help()
        parser.error("More than one image input argument provided")


    filename = args[0]
    basename = os.path.splitext(filename)[0]

    global logger
    logger = phasesymLogger.setupLogger("LOCAL_PHASE_SYM","%s.log"%(basename))
    logger.debug(" ".join(sys.argv))


    if opts.WINSZ == -1:
        parser.error("option --win must be specified")
        
    RESIZE_WIDTH = -1
    RESIZE_HEIGHT = -1
    if opts.RESIZE:
        dims = opts.RESIZE.split('x')
        if len(dims) != 2:
            parser.error("option --resize must be of the form INTxINT (i.e. 64x64)")
        try:
            dims = [int(x) for x in dims]
        except ValueError:
            parser.error("option --resize must be of the form INTxINT (i.e. 64x64)")
        RESIZE_WIDTH = dims[0]
        RESIZE_HEIGHT = dims[1]

            

    checkopts(parser,opts)

    
    NSCALE = opts.NSCALE
    NORIENT = opts.NORIENT
    MULT = opts.MULT
    SIGMAONF = opts.SIGMAONF
    K = opts.K
    BLUR = (opts.BLUR, opts.BLUR)
    SRAD = opts.SRAD
    RRAD = opts.RRAD
    DEN = opts.DEN
    TRAD = opts.TRAD
    AMIN = opts.AMIN
    AMAX = opts.AMAX
    WMAX = opts.WMAX
    WMIN = opts.WMIN
    HMAX = opts.HMAX
    HMIN = opts.HMIN
    ARATIO = opts.ARATIO
    WINSZ = opts.WINSZ 

    logger.debug("NSCALE=%d"%(NSCALE))
    logger.debug("NORIENT=%d"%(NORIENT))
    logger.debug("MULT=%.2f"%(MULT))
    logger.debug("SIGMAONF=%.2f"%(SIGMAONF))
    logger.debug("K=%d"%(K))
    logger.debug("BLUR=%s"%(str(BLUR)))
    logger.debug("SRAD=%d"%(SRAD))
    logger.debug("RRAD=%d"%(RRAD))
    logger.debug("DEN=%d"%(DEN))
    logger.debug("TRAD=%d"%(TRAD))
    logger.debug("AMIN=%d"%(AMIN))
    logger.debug("AMAX=%d"%(AMAX))
    logger.debug("WMAX=%d"%(WMAX))
    logger.debug("WMIN=%d"%(WMIN))
    logger.debug("HMAX=%d"%(HMAX))
    logger.debug("HMIN=%d"%(HMIN))
    logger.debug("ARATIO=%.2f"%(ARATIO))
    logger.debug("WINSZ=%d"%(WINSZ))
    logger.debug("RESIZE_WIDTH=%d"%(RESIZE_WIDTH))
    logger.debug("RESIZE_HEIGHT=%d"%(RESIZE_HEIGHT))




    #create subdirectory if it does not already exist
    tileDir = basename + '_windowTiles'
    if not (os.path.isdir(tileDir)):
        os.mkdir(tileDir)

    metaDir = basename + '_metadata'
    if not (os.path.isdir(metaDir)):
        os.mkdir(metaDir)



    img_orig = cv2.imread(filename)
    img = img_orig.copy()
    grayImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imwrite(os.path.join(metaDir, basename+"_gray.png"), grayImg)


    # calculate Phase Symmetry
    logger.info("Stage 1: Phase Symmetry")
    pha, ori, tot, T = phasesym(grayImg, nscale=NSCALE, norient=NORIENT, minWaveLength=3, mult=MULT, sigmaOnf=SIGMAONF, k=K, polarity=0)
    pha = cv2.normalize(pha, pha, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    pha = np.uint8(pha)
    cv2.imwrite(os.path.join(metaDir,basename + "_PS" + "_%d_%d_%.2f_%.2f_%d.png" % (NSCALE, NORIENT, MULT, SIGMAONF, K)), pha)
    cv2.imwrite(os.path.join(metaDir,basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_ori.png" % (NSCALE, NORIENT, MULT, SIGMAONF, K)), ori)
    np.savetxt(os.path.join(metaDir,'python_ori.txt'),ori)


    # blurring the image helps disperse the energy enough for mean-shift to pick up hotspots
    pha = cv2.blur(pha, BLUR)
    cv2.imwrite(os.path.join(metaDir,basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_B_%d_%d.png" % (NSCALE, NORIENT, MULT, SIGMAONF, K, BLUR[0], BLUR[1])), pha)
    pha = cv2.cvtColor(pha, cv2.COLOR_GRAY2RGB)
    pha = cv2.cvtColor(pha, cv2.COLOR_RGB2LUV)
    logger.info("Stage 1: Phase Symmetry -- Complete")

    # calculate mean-shift in LUV colorspace and convert back to RBB
    logger.info("Stage 2: Mean-Shift")
    (segmented_image, labels_image, number_regions) = pms.segment(pha, spatial_radius=SRAD, range_radius=RRAD, min_density=DEN)
    segmented_image=cv2.normalize(segmented_image, segmented_image, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    segmented_image = np.uint8(segmented_image)
    segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_LUV2RGB)
    segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_RGB2GRAY)
    cv2.imwrite(os.path.join(metaDir,basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_B_%d_%d_MS_%d_%d_%d.png" % (NSCALE, NORIENT, MULT, SIGMAONF, K, BLUR[0], BLUR[1], SRAD, RRAD, DEN)), segmented_image)

    # threshold to obtain symmetry blobs
    thresh_img = cv2.adaptiveThreshold(segmented_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, WINSZ, 4)
    cv2.imwrite(os.path.join(metaDir,basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_B_%d_%d_MS_%d_%d_%d_T.png" % (NSCALE, NORIENT, MULT, SIGMAONF, K, BLUR[0], BLUR[1], SRAD, RRAD, DEN)), thresh_img)
    logger.info("Stage 2: Mean-Shift -- Complete")

    #get centroids
    contours = getContours(thresh_img, AMIN, AMAX, WMIN, WMAX, HMIN, HMAX, ARATIO)
    centroids = getCentroids(contours)
    

    centroidsImg = img.copy()
    drawCentroids(centroidsImg,centroids)
    cv2.imwrite(os.path.join(tileDir, "Centroids.jpg"), centroidsImg) 

    for cen,cnt in zip(centroids,contours):
        win = cv2.getRectSubPix(img,(WINSZ,WINSZ),(cen[1],cen[0]))

        filename = "win_%d_%d.jpg" % (cen[0], cen[1])

        if opts.RESIZE:
            win = cv2.resize(win, (RESIZE_WIDTH, RESIZE_HEIGHT))

        cv2.imwrite(os.path.join(tileDir, filename), win)



    f = open(os.path.join(tileDir,"centroids.txt"),"w")
    for cen in centroids:
        f.write("%d, %d\n"%(cen[0],cen[1]))
    f.close()

    logging.shutdown()


if __name__ == "__main__":
    sys.exit(main())
