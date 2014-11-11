import cv2, sys, optparse
import os
import datetime
import pymeanshift as pms
from PhaseSymmetry.src.phasesym import *
from matplotlib import pyplot as plt

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
    basename = os.path.splitext(filename)[0]
    img = cv2.imread(filename)



    NSCALE = 4
    NORIENT = 6
    MULT = 3.4
    SIGMAONF = 0.45
    K = 11

    NSCALE_1 = 4
    NORIENT_1 = 6
    MULT_1 = 3.4
    SIGMAONF_1 = 0.45
    K_1 = 11

    NSCALE_2 = 3
    NORIENT_2 = 6
    MULT_2 = 2.1
    SIGMAONF_2 = 0.65
    K_2 = 1


    NSCALE_3 = 3
    NORIENT_3 = 6
    MULT_3 = 3
    SIGMAONF_3 = 0.55
    K_3 = 1

    BLUR = (3,3)
    SRAD = 8
    RRAD = 3
    DEN = 10
    THRESH = 1
    AMIN = 5
    AMAX = 400
    WMAX = 35
    WMIN = 3
    HMAX = 55
    HMIN = 2
    #ARATIO = 0.25
    ARATIO = 0.10

    
    timePrefix = datetime.datetime.now().strftime("__%Y-%m-%d_%I:%M")

    grayImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imwrite(basename+"_gray.png", grayImg)
    pha1, ori1, tot1, T1 = phasesym(grayImg, nscale=NSCALE_1, norient=NORIENT_1, minWaveLength=3, mult=MULT_1, sigmaOnf =SIGMAONF_1, k=K_1, polarity=0)
    pha2, ori2, tot2, T2 = phasesym(grayImg, nscale=NSCALE_2, norient=NORIENT_2, minWaveLength=3, mult=MULT_2, sigmaOnf =SIGMAONF_2, k=K_2, polarity=0)
    pha3, ori3, tot3, T3 = phasesym(grayImg, nscale=NSCALE_3, norient=NORIENT_3, minWaveLength=3, mult=MULT_3, sigmaOnf =SIGMAONF_3, k=K_3, polarity=0)


    pha = pha1 + pha2 + pha3

    pha1=cv2.normalize(pha1,pha1,0,255,cv2.NORM_MINMAX,cv2.CV_8UC1)
    pha1 = np.uint8(pha1)
    cv2.imwrite(basename + timePrefix + "_PS" + "_%d_%d_%.2f_%.2f_%d.png"%(NSCALE_1,NORIENT_1,MULT_1,SIGMAONF_1,K_1), pha1)

    pha2=cv2.normalize(pha2,pha2,0,255,cv2.NORM_MINMAX,cv2.CV_8UC1)
    pha2 = np.uint8(pha2)
    cv2.imwrite(basename + timePrefix + "_PS" + "_%d_%d_%.2f_%.2f_%d.png"%(NSCALE_2,NORIENT_2,MULT_2,SIGMAONF_2,K_2), pha2)

    pha3=cv2.normalize(pha3,pha3,0,255,cv2.NORM_MINMAX,cv2.CV_8UC1)
    pha3 = np.uint8(pha3)
    cv2.imwrite(basename + timePrefix + "_PS" + "_%d_%d_%.2f_%.2f_%d.png"%(NSCALE_3,NORIENT_3,MULT_3,SIGMAONF_3,K_3), pha3)

    pha=cv2.normalize(pha,pha,0,255,cv2.NORM_MINMAX,cv2.CV_8UC1)
    pha = np.uint8(pha)
    cv2.imwrite(basename + timePrefix + "_PS" + "_sum.png", pha)


    pha = cv2.blur(pha, BLUR)
    cv2.imwrite(basename + timePrefix + "_PS" + "_sum_B_%d_%d.png"%(BLUR[0],BLUR[1]), pha)
    #pha = cv2.medianBlur(pha, 5)
    #cv2.imwrite(basename + timePrefix + "_PS" + "_sum_B_%d_%d.png"%(BLUR[0],BLUR[1]), pha)
    pha = cv2.cvtColor(pha, cv2.COLOR_GRAY2RGB)
    pha = cv2.cvtColor(pha, cv2.COLOR_RGB2LUV)


    #(segmented_image, labels_image, number_regions) = pms.segment(pha, spatial_radius=3, range_radius=11, min_density=10)
    #(segmented_image, labels_image, number_regions) = pms.segment(pha, spatial_radius=15, range_radius=11, min_density=10)
    (segmented_image, labels_image, number_regions) = pms.segment(pha, spatial_radius=SRAD, range_radius=RRAD, min_density=DEN)
    segmented_image=cv2.normalize(segmented_image,segmented_image,0,255,cv2.NORM_MINMAX,cv2.CV_8UC1)
    segmented_image = np.uint8(segmented_image)
    segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_LUV2RGB)
    segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_RGB2GRAY)
    cv2.imwrite(basename +  timePrefix +"_PS" + "_sum_B_%d_%d_MS_%d_%d_%d.png"%(BLUR[0],BLUR[1],SRAD,RRAD,DEN), segmented_image)




    #ret,thresh_img = cv2.threshold(segmented_image,THRESH,255, cv2.THRESH_BINARY| cv2.THRESH_OTSU)
    thresh_img = cv2.adaptiveThreshold(segmented_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,7,0)
    cv2.imwrite(basename +  timePrefix +"_PS" + "_sum_B_%d_%d_MS_%d_%d_%d_T_%d.png"%(BLUR[0],BLUR[1],SRAD,RRAD,DEN,THRESH), thresh_img)


    #find contours in black and white image
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours: 
        area = cv2.contourArea(cnt)
        if area >= AMIN and area <= AMAX:
            x,y,w,h = cv2.boundingRect(cnt)
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
    
    cv2.imwrite(basename +  timePrefix +"_PS" + "_sum_B_%d_%d_MS_%d_%d_%d_T_%d_A_%d_%d_W_%d_%d_H_%d_%d_R_%.2f.png"%(BLUR[0],BLUR[1],SRAD,RRAD,DEN,THRESH,AMIN,AMAX,WMIN,WMAX,HMIN,HMAX,ARATIO), img)



if __name__ == "__main__":
    sys.exit(main())
