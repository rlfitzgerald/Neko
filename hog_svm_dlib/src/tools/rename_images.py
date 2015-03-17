import sys, os
import optparse
import glob
import cv2
import numpy as np





def main(argv=None):
    if argv is None:
        argv = sys.argv

    desc = """%prog renames all jpgs and pngs to img_#.jpg where # is a digit counting from 1 to number of images."""

    parser = optparse.OptionParser(description=desc, usage='Usage: ex) %prog --start=4')
    parser.add_option('--start', help='specify a starting number', dest='start', default=1, type="int")
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
        temp = cv2.imread(f)
        cv2.imwrite(os.path.join(dirName,"%s_%d.jpg"%(opts.prefix,opts.start+idx)),temp)



if __name__ == "__main__":
    sys.exit(main())
