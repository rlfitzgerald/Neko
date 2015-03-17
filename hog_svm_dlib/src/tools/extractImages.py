import sys
import optparse
import xml.etree.ElementTree as ET
import numpy as np
import cv2

DEBUG = False

def main(argv=None):
    if argv is None:
        argv = sys.argv

    desc = """%prog will normalize all height and width attributes of a given xml file to their average"""

    parser = optparse.OptionParser(description=desc,usage="Usage: %prog -r --thresh=3.5 file.xml")
    parser.add_option("-r","--replace", action="store_true", dest="replace", default=False, help="Auto ignore outlier boxes")
    parser.add_option("--norm", action="store_true", dest="norm", default=False, help="Contrast normalize image")
    parser.add_option("--thresh", dest="thresh", default=3.5, type='float', help="Outlier detection threshhold")
    parser.add_option("-v","--verbose", action="store_true", dest="verbose", default=False, help="verbose output")
    parser.add_option('--start', help='specify a starting number', dest='start', default=1, type="int")
    parser.add_option('--prefix', help='specify a prefix string', dest='prefix', default="img", type="string")
    parser.add_option('--size', help='specify the dimensions to resize image Ex) 64x64', dest='size', default="64x64", type="string")

    (opts,args) = parser.parse_args(argv)
    args = args[1:]
    
    if opts.verbose:
        print "options: ", opts 
        print "Files: ", args



    #make sure at least one file has been provided
    if len(args) < 1:
        print "No xml file specified"
        sys.exit(-1)

    #make sure all files are .xml
    for file in args:
        ext = file.split('.')
        if len(ext) != 2:
            print "Error: %s is an invalid file" %(file)
            sys.exit(-1)
        elif ext[1] != 'xml':
            print "Error: %s is not an xml file" %(file)
            sys.exit(-1)

    currDir = os.path.split(file)[0]

    if opts.replace:
        print "Replace flag (-r, --replace) set, boxes outside bound will be automatically ignored"

    outfile = open("extractImages_log.txt","w")

    for file in args:
        if opts.verbose:
            print "File: ", file
        dataArr = []
        tree = ET.parse(file)
        root = tree.getroot()

        #search xml tree for images element
        for element in root:
            if element.tag == 'images':
                imageList = element


        for image in imageList:        
            if len(image) == 0:
                outfile.write("%s contains no boxes. Ignoring\n\n"%(image.attrib['file']))
                if opts.verbose:
                    print "%s contains no boxes. Ignoring\n\n"%(image.attrib['file'])
                continue
            
            if opts.verbose:
                print "Image: %s" %(image.attrib['file'])
                print "Image: %s" %(os.path.join(currDir,image.attrib['file']))

            sys.exit()

            for box in image:
                if 'ignore' not in box.attrib:
                    #xml attributes are always string, cast height & width to int
                    h = int(box.attrib['height'])
                    w = int(box.attrib['width'])
                    avg = (h+w) / 2
                    dataArr.append(avg)
                    if opts.verbose:
                        print "Height: %i    Width: %i" %(h,w)
                        print "Setting side length to %i" %(avg)

                    # xml gets cranky trying to read int, cast back to string
                    if h != w:
                        box.attrib['height'] = str(avg)
                        box.attrib['width'] = str(avg)
            
        if opts.verbose:
            print "Side lengths: ", dataArr
            dataArr_ndarr = np.array(dataArr)
            print "Number of Images = %d"%(len(dataArr))
            print "Avg: %0.2f  Var: %0.2f  Std: %0.2f  Min: %0.2f  Max: %0.2f"%(dataArr_ndarr.mean(), dataArr_ndarr.var(), dataArr_ndarr.std(), dataArr_ndarr.min(), dataArr_ndarr.max())


            
        for image in imageList:
            if len(image) > 0: 
                outfile.write("Scanning boxes in %s\n"%(image.attrib['file']))
                outfile.write("---------------------------\n")
                for box in image:
                    if 'ignore' not in box.attrib:
                        h = int(box.attrib['height'])
                        if is_outlier(h, dataArr, opts.thresh):
                            outfile.write("Outlier found at top: %s, left: %s. Height and width are %s\n" %(box.attrib['top'],box.attrib['left'],box.attrib['height']))
                            if opts.replace:
                                box.attrib['ignore'] = '1'
            outfile.write("\n\n\n")
        
        
        tree.write(ext[0]+'_fixed.xml')



def is_outlier(p,points, thresh=3.5):
    """
    Returns a boolean array with True if points are outliers and False 
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor. 
    """
    points = np.array(points)
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    diff_p = (p-median)**2
    diff_p = np.sqrt(diff_p)

    modified_z_score = 0.6745 * diff_p / med_abs_deviation
    

    return modified_z_score[0] > thresh


    
            

if __name__ == '__main__':
    sys.exit(main())
