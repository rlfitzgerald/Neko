import cv2, sys, optparse
import numpy as np


def findBlobs(filename):    
    #read image
    img1 = cv2.imread(filename)

    #smooth image to reduce noise
    img1 = cv2.blur(img1, (3,3))
    
    #convert to grayscale
    grayImg = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        
    #threshold grayscale image
    (threshold, img_bw) = cv2.threshold(grayImg, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    #save black and white image (to debug)
    cv2.imwrite('Black_and_White.jpg', img_bw)
    
    #find contours in black and white image
    contours, hierarchy = cv2.findContours(img_bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours: 
        area = cv2.contourArea(cnt)
        #if area >= 200 and area <= 2000:
        if area >= 100 and area <= 2000:
            rect = cv2.minAreaRect(cnt)
            box = cv2.cv.BoxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(img1, [box], 0, (0, 0, 255), 2)
    
    cv2.imwrite('Boxes.jpg', img1) 
    print('Finished')
    
def main(argv=None):
    if argv is None:
        argv = sys.argv

    desc = """%prog is a tool that finds all blobs in an image within a certain size band."""
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
    filename = argv[1]
    
    #find and box proper blobs
    findBlobs(filename)


if __name__ == "__main__":
    sys.exit(main())


    
