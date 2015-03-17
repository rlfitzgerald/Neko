#!/usr/bin/python

import optparse
import sys, os
import glob
import shutil
from random import shuffle

DEBUG = False

def main(argv=None):
    
    if argv is None:
        argv=sys.argv

    desc = """%prog will take all jpgs in a given directory and randomly bin them into a specified number of subdirectories"""

    parser = optparse.OptionParser(description=desc, usage="Usage: %prog -n 5 directory_name")
    parser.add_option('-n', help="Specify number of bins", type='int', dest="binCount", default=1)

    (opts,args) = parser.parse_args(argv)
    args = args[1:]
    
    if DEBUG:
        print "opts: " + str(opts)
        print "args: " + str(args)

    
    if len(args) != 1: 
        print "Please provide a single directory as an argument"
        sys.exit(-1)
    
    dir = os.path.abspath(args[0])

    if DEBUG:
        print "dir: " + dir

    if not os.path.exists(dir):
        print "Invalid input directory"
        sys.exit(-1)


    imgList = glob.glob(os.path.join(dir,"*.jpg"))

    if DEBUG:
        for img in imgList:
            if ".jpg" not in os.path.basename(img):
                print "%s is a bad catch!" %(img)
        print "ImageList: ", imgList

    shuffle(imgList)

    if DEBUG:
        print "Randomized imageList: ", imgList

    for i in range(opts.binCount):
        try:
            os.mkdir(os.path.join(dir,"bin"+str(i+1)))
        except OSError as e:
            print e
            sys.exit(-1)

    for idx, img in enumerate(imgList):
        bin = "bin" + str(idx%opts.binCount+1)
        
        if DEBUG:
            print os.path.basename(img) +  bin 
        
        shutil.copyfile(img,os.path.join(dir,bin,os.path.basename(img)))

    print "Please don't gut me like a fish!"    
    


if __name__ == "__main__":
    sys.exit(main())
