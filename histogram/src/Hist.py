
import cv2
class Hist(object):

    def __init__(self, img):
        """Default constructor. Must be overloaded in order to properly handle the histogramming methodology used.
        The size and dimensionality of the class member 'hist' will vary based on the histogram method employed in your
        implementation of this class."""
        self._img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        self._hist = None

    def _calculate(self):
        """Calculates the histogram value on the given input image. This value is stored in the class member 'hist'"""
        return None

    def compare(self, otherHist, dist):
        """return True is the other histogram is within some distance metric of this histogram.
        INPUTS:
            otherHist       the histogram to be compared to
            dist            the distance metric to define what is 'near' this histogram. Choose default value.
        OUTPUTS:
            True if other histogram is within the given dist of similarity, False otherwise."""
        return None

    def __str__(self):
        """return a formatted output string for this histogram"""
        return " Overload me. "


import numpy as np
np.seterr(all='raise')
class RadAngleHist(Hist):


    def __init__(self, img, orientation):
        super(RadAngleHist, self).__init__(img)
        self._MAX_VAL = 255

        #Centroid calculation. Assumes passed image window is centered on centroid of blob.
        w, h = self._img.shape
        if w%2:
            x = int(np.ceil(w/float(2)))
        else:
            x = w/2

        if h%2:
            y = int(np.ceil(h/float(2)))
        else:
            y = h/2

        self._centroid = (x, y)
        self._orientation = orientation
        self._calculate()

    def _calculate(self):
        """X is rows, Y is columns here."""

        # Rotate image
        M = cv2.getRotationMatrix2D(self._centroid, 360 - self._orientation, 1)
        img = cv2.warpAffine(self._img, M, self._img.shape)
        M = cv2.getRotationMatrix2D(self._centroid, 90, 1)
        img = cv2.warpAffine(img, M, img.shape)


        # Canny edge detection

        blurImg = cv2.blur(img, (3,3))
        edge = cv2.Canny(blurImg, 90, 250)

        # Radiometric histogram calculation begins
        # Measure from centroid outward to edge of blob
        rVals = []
        thetaVals = []

        xarr = np.arange(-self._centroid[0], self._centroid[0] + 1, 1)
        yarr = np.arange(self._centroid[1], -self._centroid[1] + 1, -1)

        xg, yg = np.meshgrid(xarr, yarr)

        for x in range(self._img.shape[0]):
            for y in range(self._img.shape[1]):
                xCoordinate = xg[x][y]
                yCoordinate = yg[x][y]
                pixel = edge[xCoordinate][yCoordinate]
                if not((xCoordinate == 0) and (yCoordinate == 0)) and pixel == self._MAX_VAL:
                    # Calculate distance and angle from centroid
                    logr = np.log(np.sqrt(np.square(xCoordinate) + np.square(yCoordinate)))
                    theta = np.arctan2(xCoordinate, yCoordinate)
                    rVals.append(logr)
                    thetaVals.append(theta)

        H, xe, ye = np.histogram2d(thetaVals, rVals, bins=[5, 12])
        self._hist = H
        print "Histogram:\n" + str(self._hist) + "\nxEdges: " + str(xe) + "\nyEdges: " + str(ye) + "\nCentroid: " + str(self._centroid) + "\n\n"

    def compare(self, otherHist, dist):

        return None

    def __str__(self):

        return str(self._hist)
