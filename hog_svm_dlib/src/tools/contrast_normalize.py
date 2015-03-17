import sys, os
import optparse
import glob
import cv2
import numpy as np





def main(argv=None):
    if argv is None:
        argv = sys.argv

    desc = """%prog contrast normalizes all images within a directory"""

    parser = optparse.OptionParser(description=desc, usage='Usage: ex) %prog --prefix=norm')
    parser.add_option("--gray", action="store_true", dest="gray", default=False, help="Convert to grayscale")
    parser.add_option('--prefix', help='specify a prefix string', dest='prefix', default="norm", type="string")


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
        if opts.gray and len(temp.shape)>2:
            temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        temp = cv2.normalize(temp, temp, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
        cv2.imwrite(os.path.join(dirName,"%s_%s"%(opts.prefix,baseImgName)),temp)



if __name__ == "__main__":
    sys.exit(main())
