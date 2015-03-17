import os
import sys
import glob
import optparse
import xml.etree.ElementTree as ET
import numpy as np
import cv2
from xml.dom import minidom

DEBUG = False

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8',method="xml")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i


def main(argv=None):
    if argv is None:
        argv = sys.argv

    desc = """%prog will generate a dlib xml file used for HoG SVM training"""

    parser = optparse.OptionParser(description=desc,usage="Usage: %prog --label=car path/to/image/dir")
    parser.add_option("-v","--verbose", action="store_true", dest="verbose", default=False, help="verbose output")
    parser.add_option("-l","--label", help='specify a label string', dest='label', default="None", type="string")

    (opts,args) = parser.parse_args(argv)
    args = args[1:]
    
    if opts.verbose:
        print "options: ", opts 
        print "Files: ", args


    if len(args) != 1:
        parser.print_help()
        parser.error("Invalid arguments provided")


    dirName = args[0]
    if not (os.path.isdir(dirName)):
        parser.error("Directory %s does not exist"%(dirName))

    imageList = []
    imageList.extend(glob.glob(os.path.join(dirName,"*.png")))
    imageList.extend(glob.glob(os.path.join(dirName,"*.jpg")))


    root = ET.Element("dataset")
    ET.SubElement(root,"name").text = "imglab dataset"
    ET.SubElement(root,"comment").text = "created by Aerospace"
    images = ET.SubElement(root,"images")

    for imgName in imageList:
        baseImgName = os.path.basename(imgName) 
        imgEntry = ET.SubElement(images,"image",file=baseImgName)
        img = cv2.imread(imgName)
        if "pos" in baseImgName.lower():
            w,h,z = img.shape
            box = ET.SubElement(imgEntry,"box",top="0",left="0",width=str(w),height=str(h))
            ET.SubElement(box,"label").text = opts.label
    

    indent(root)
    tree = ET.ElementTree(root)    
    tree.write("output.xml", xml_declaration=True, encoding='utf-8', method="xml")



            

if __name__ == '__main__':
    sys.exit(main())
