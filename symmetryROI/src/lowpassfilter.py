#Constructs a low-pass butterworth filter
#
#Parameters:
#
#    size:      is a two element vector specifying the size of the filter
#               to construct [rows cols]
#
#    cutoff:    the cutoff frequency of the filter 0 - 0.5
#
#    n:         the order of the filter. The higher the order, the sharper
#               the transition will be.
#
#                   1
#    f = -------------------------
#                            2n
#            1.0 + (w/cutoff)
#
#
#
import numpy as np

def lowpassfilter(size, cutoff, n):

    if cutoff < 0 or cutoff > 0.5:
        print "Cutoff Frequency must be between 0 and 0.5.\n"
    elif len(size) > 2 or len(size) < 1:
        print "Illegal tuple for filter dimensionality. Filter must be two dimensional."
    elif not isinstance(n, (int, long)):
        print "N must be an integer."
    else:
        #Legal input parameters. Begin building filter

        #Build rows and columns
        if len(size) == 1:
            rows = size
            cols = size
        else:
            rows = size[0]
            cols = size[1]

        rows = np.float(rows)
        cols = np.float(cols)
        dimensions = (rows, cols)
        #Set up X and Y matrices with ranges normalized to +/- 0.5
        #The following code adjusts things appropriately for odd and even values
        #of rows and columns

        if cols % 2:
            #Odd
            xrange = np.arange(-(cols - 1)/2, (cols - 1)/2 + 1, dtype=np.float)
            xrange = np.divide(xrange, np.float(cols-1))
        else:
            xrange = np.arange(-cols/2, (cols/2-1) + 1, dtype=np.float)
            xrange = np.divide(xrange, cols)

        if rows % 2:
            yrange = np.arange(-(rows-1)/2, (rows-1)/2 + 1, dtype=np.float)
            yrange = np.divide(yrange, np.float(rows - 1))
        else:
            yrange = np.arange(-rows/2, (rows/2-1) + 1, dtype=np.float)
            yrange = np.divide(yrange, rows)

        #print str(xrange) + "\n"
        #print str(yrange) + "\n"

        xv, yv = np.meshgrid(xrange, yrange)
        #print xv
        #print yv
        radius = np.sqrt(np.square(xv) + np.square(yv))
        f = np.fft.ifftshift(np.divide(1.0, (1.0 + (np.divide(radius, cutoff))**(2*n))))

        return f