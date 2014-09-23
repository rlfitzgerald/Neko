#!/usr/bin/python

#Copyright (c) 2014, The Aerospace Corporation. 
#convert.py is licensed under the GPL (v 3.0).
#A copy of this license can be found in LICENSE file in the top level directory.

import optparse
import sys
import os
import subprocess
from nitf import *
import logging


DEBUG=False

def extract_image(subheader, index, imageReader, outDir=None, baseName=None):
    window = SubWindow()
    window.numRows = subheader['numRows'].intValue()
    window.numCols = subheader['numCols'].intValue()
    window.bandList = range(subheader.getBandCount())
    nbpp = subheader['numBitsPerPixel'].intValue()
    bandData = imageReader.read(window)
   
    if not outDir: outDir = os.getcwd()
    if not baseName: baseName = os.path.basename(os.tempnam())
   
    outNames = []
    for band, data in enumerate(bandData):
        outName = '%s_%d__%d_x_%d_%d_band_%d.pgm' % (
             baseName, index, window.numRows, window.numCols, nbpp, band)
        outName = os.path.join(outDir, outName)
        f = open(outName, 'wb')
        f.write('P5\n%d %d\n255\n'%(window.numCols, window.numRows))
        f.write(data)
        f.close()
        outNames.append(outName)
        logging.info('Wrote band data to file %s' % outName)
    return outNames



def extract_images(fileName, outDir=None):
    if not outDir: outDir = os.getcwd()
    if not os.path.exists(outDir): os.makedirs(outDir)
   
    handle = IOHandle(fileName)
    reader = Reader()
    record = reader.read(handle)
    logging.info('Dumping file: %s' % fileName)
   
    for i, segment in enumerate(record.getImages()):
        logging.info('--- Image [%d] ---' % i)
        imReader = reader.newImageReader(i)
        extract_image(segment.subheader, i, imReader, outDir, os.path.basename(fileName))
    handle.close()


def main(argv=None):

    if argv is None:
        argv = sys.argv

    desc = """%prog is a tool that converts .ntf images to .pgm images."""

    parser = optparse.OptionParser(description=desc, usage='Usage: ex) %prog --hpcc=hpccoutf_desktop_medium_1353034748.txt out\n           %prog --hpcc_compare=file1.txt,file2.txt,file3.txt out') 
    
    (opts, args) = parser.parse_args(argv)
    args = args[1:]

    if DEBUG:
        print "args: " + str(args)
        print "options:  "+ str(opts) 


    #make sure that the necessary arguments and options are given
    mandatory_options = []

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
        
    extract_images(args[0])
    
    

if __name__ == "__main__":
    sys.exit(main())
