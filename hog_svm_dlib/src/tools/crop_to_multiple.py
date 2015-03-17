import sys, os
import optparse
import glob
import cv2
import numpy as np





def main(argv=None):
    if argv is None:
        argv = sys.argv

    desc = """%prog resizes all jpgs and pngs to be a multiple of a given number"""

    parser = optparse.OptionParser(description=desc, usage='Usage: ex) %prog --start=4')
    parser.add_option('--mult', help='specify a multiple', dest='mult', default=64, type="int")
    parser.add_option('--prefix', help='specify a prefix string', dest='prefix', default="img", type="string")


    (opts, args) = parser.parse_args(argv)
    args = args[1:]


    # Check to see if the file system image is provided
    if len(args) > 1:
        parser.print_help()
        parser.error("Invalid arguments provided")


    dirName = args[0]
    if not (os.path.isdir(dirName)):
        parser.error("Directory %s does not exist"%(dirName))
    #basename = os.path.splitext(filename)[0]
    
    files = []
    files.extend(glob.glob(os.path.join(dirName,"*.png")))
    files.extend(glob.glob(os.path.join(dirName,"*.jpg")))
    
    for idx,f in enumerate(files):
        baseImgName = os.path.basename(f)
        temp = cv2.imread(f)
        w,h,z = temp.shape
        resizeWidth = int(w/opts.mult)*opts.mult
        resizeHeight = int(h/opts.mult)*opts.mult
        print "%s:   %d, %d --> %d, %d"%(f,w,h,resizeWidth,resizeHeight)
        temp=temp[0:resizeWidth,0:resizeHeight]
        cv2.imwrite(os.path.join(dirName,"resized_%s"%(baseImgName)),temp)



if __name__ == "__main__":
    sys.exit(main())
