import cv2, sys, optparse
import os
import pymeanshift as pms
from phasesym import *
from matplotlib import pyplot as plt
import optparse

def meanShift(filename):

    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2LUV)

   # (segmented_image, labels_image, number_regions) = pms.segment(img, spatial_radius=6, range_radius=4.5, min_density=50)
    (segmented_image, labels_image, number_regions) = pms.segment(img, spatial_radius=3, range_radius=11, min_density=10)
    return segmented_image

def blobDetect(img):
    #smooth image to reduce noise
    img1 = cv2.blur(img, (3,3))

    #threshold grayscale image
    (threshold, img_bw) = cv2.threshold(img1, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    #save black and white image (to debug)
    cv2.imwrite('Black_and_White.jpg', img_bw)

    #find contours in black and white image
    contours, hierarchy = cv2.findContours(img_bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    #convert to color for debugging purposes
    colorImg = cv2.cvtColor(img1, cv2.COLOR_GRAY2RGB)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >= 200 and area <= 2000:
            rect = cv2.minAreaRect(cnt)
            box = cv2.cv.BoxPoints(rect)
            box = np.int0(box)
            print box
            cv2.drawContours(colorImg, [box], 0, (0, 0, 255), 2)

    cv2.imwrite('Boxes.jpg', colorImg)


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


    NSCALE =opts.NSCALE
    NORIENT =opts.NORIENT
    MULT =opts.MULT
    SIGMAONF =opts.SIGMAONF
    K =opts.K
    BLUR =(opts.BLUR,opts.BLUR)
    SRAD =opts.SRAD
    RRAD =opts.RRAD
    DEN =opts.DEN
    AMIN =opts.AMIN
    AMAX =opts.AMAX
    WMAX =opts.WMAX
    WMIN =opts.WMIN
    HMAX =opts.HMAX
    HMIN =opts.HMIN
    ARATIO =opts.ARATIO 

    THRESH=0

    #begin transform
    filename = args[0]
    basename = os.path.splitext(filename)[0]
    img = cv2.imread(filename)
    #img = cv2.cvtColor(img, cv2.COLOR_RGB2LUV)
    #(segmented_image, labels_image, number_regions) = pms.segment(img, spatial_radius=3, range_radius=11, min_density=10)
    #img = cv2.cvtColor(img, cv2.COLOR_LUV2RGB)
    #cv2.imwrite("MS_" + basename+".png", img)
    #img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #pha, ori, tot, T = phasesym(img, nscale=5, norient=6, minWaveLength=3, mult=3.4, sigmaOnf = 0.45, k=29)
 
    #pha=cv2.normalize(pha,pha,0,255,cv2.NORM_MINMAX,cv2.CV_8UC1)
    #pha = np.uint8(pha)
    #cv2.imwrite("MSPS_Serial_" + basename + ".png", pha)
    #blobDetect(pha)


    #NSCALE = 4
    #NORIENT = 6
    #MULT = 3
    #SIGMAONF = 0.55
    #K = 1
    #BLUR = (3,3)
    #SRAD = 5
    #RRAD = 6
    #DEN = 10
    #THRESH = 127
    #AMIN = 5
    #AMAX = 400
    #WMAX = 35
    #WMIN = 3
    #HMAX = 55
    #HMIN = 2
    #ARATIO = 0.25

    grayImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imwrite(basename+"_gray.png", grayImg)
    #pha, ori, tot, T = phasesym(grayImg, nscale=5, norient=6, minWaveLength=3, mult=3.4, sigmaOnf = 0.45, k=29)
    #pha, ori, tot, T = phasesym(grayImg, nscale=6, norient=6, minWaveLength=3, mult=3, sigmaOnf = 0.55, k=1, polarity=0)
    pha, ori, tot, T = phasesym(grayImg, nscale=NSCALE, norient=NORIENT, minWaveLength=3, mult=MULT, sigmaOnf =SIGMAONF, k=K, polarity=0)
    pha=cv2.normalize(pha,pha,0,255,cv2.NORM_MINMAX,cv2.CV_8UC1)
    pha = np.uint8(pha)
    cv2.imwrite(basename + "_PS" + "_%d_%d_%.2f_%.2f_%d.png"%(NSCALE,NORIENT,MULT,SIGMAONF,K), pha)


    pha = cv2.blur(pha, BLUR)
    cv2.imwrite(basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_B_%d_%d.png"%(NSCALE,NORIENT,MULT,SIGMAONF,K,BLUR[0],BLUR[1]), pha)
    pha = cv2.cvtColor(pha, cv2.COLOR_GRAY2RGB)
    pha = cv2.cvtColor(pha, cv2.COLOR_RGB2LUV)


    #(segmented_image, labels_image, number_regions) = pms.segment(pha, spatial_radius=3, range_radius=11, min_density=10)
    #(segmented_image, labels_image, number_regions) = pms.segment(pha, spatial_radius=15, range_radius=11, min_density=10)
    (segmented_image, labels_image, number_regions) = pms.segment(pha, spatial_radius=SRAD, range_radius=RRAD, min_density=DEN)
    segmented_image=cv2.normalize(segmented_image,segmented_image,0,255,cv2.NORM_MINMAX,cv2.CV_8UC1)
    segmented_image = np.uint8(segmented_image)
    segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_LUV2RGB)
    segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_RGB2GRAY)
    cv2.imwrite(basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_B_%d_%d_MS_%d_%d_%d.png"%(NSCALE,NORIENT,MULT,SIGMAONF,K,BLUR[0],BLUR[1],SRAD,RRAD,DEN), segmented_image)




    #ret,thresh_img = cv2.threshold(segmented_image,THRESH,255, cv2.THRESH_BINARY| cv2.THRESH_OTSU)
    thresh_img = cv2.adaptiveThreshold(segmented_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,7,0)
    cv2.imwrite(basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_B_%d_%d_MS_%d_%d_%d_T_%d.png"%(NSCALE,NORIENT,MULT,SIGMAONF,K,BLUR[0],BLUR[1],SRAD,RRAD,DEN,THRESH), thresh_img)


    #find contours in black and white image
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours: 
        area = cv2.contourArea(cnt)
        #if area >= 200 and area <= 2000:
        #if area >= 10 and area <= 1200:
        if area >= AMIN and area <= AMAX:
            x,y,w,h = cv2.boundingRect(cnt)
            #if w < WMAX and h < HMAX and w > 3 and h > 2:
            if w < WMAX and h < HMAX and w > WMIN and h > HMIN:
                aspectRatio = 0
                if w == min(w,h):
                    aspectRatio = float(w)/h
                else:
                    aspectRatio = float(h)/w

                if aspectRatio > ARATIO:
                    print "x=%d y=%d w=%d h=%d"%(x,y,w,h)
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.cv.BoxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(img, [box], 0, (255, 0, 0), 2)
    
    #cv2.imwrite('Boxes.jpg', img) 
    cv2.imwrite(basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_B_%d_%d_MS_%d_%d_%d_T_%d_A_%d_%d_W_%d_%d_H_%d_%d_R_%.2f.png"%(NSCALE,NORIENT,MULT,SIGMAONF,K,BLUR[0],BLUR[1],SRAD,RRAD,DEN,THRESH,AMIN,AMAX,WMIN,WMAX,HMIN,HMAX,ARATIO), img)



if __name__ == "__main__":
    sys.exit(main())
