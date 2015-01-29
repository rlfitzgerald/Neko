import os
import cv2
import cv2.cv as cv
import numpy as np
import logging
import phasesymLogger
import collections



class Hist(object):

    def __init__(self, img):
        """Default constructor. Must be overloaded in order to properly handle the histogramming methodology used.
        The size and dimensionality of the class member 'hist' will vary based on the histogram method employed in your
        implementation of this class."""
        if len(img.shape) > 2:
            self._img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            self._img = img
        self._shapeHist = None

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


class RadAngleHist(Hist):


    def __init__(self, img, orientation,yCentroid,xCentroid,blurVal,canny_low=90,canny_high=200,outDir=""):
        super(RadAngleHist, self).__init__(img)
        self._MAX_VAL = 255

        #Centroid calculation. Assumes passed image window is centered on centroid of blob.
        #w, h = self._img.shape
        h, w = self._img.shape
        self._rmin=2
        self._rmax=0
        if w%2:
            x = int(np.ceil(w/float(2)))
            self._rmax=int(np.ceil(w/float(2)))
        else:
            x = w/2
            self._rmax = w/2

        if h%2:
            y = int(np.ceil(h/float(2)))
        else:
            y = h/2

        self._centroid = (y, x)
        self._orientation = orientation
        self._origCentroidX = xCentroid
        self._origCentroidY = yCentroid
        self._origCentroid = (yCentroid,xCentroid)
        self._blurVal = blurVal
        self.logger = logging.getLogger("LOCAL_PHASE_SYM")
        self._outDir=outDir
        self._edgeImg=None
        self._canny_low=canny_low
        self._canny_high=canny_high

        self._calculate()


    def _calculate(self):
        """X is rows, Y is columns here."""
        # apply adaptive histogram equalization to image patch 

        #clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        #img = clahe.apply(self._img)

        img = self._img.copy()

        #img = cv2.blur(img, self._blurVal)
        img = cv2.bilateralFilter(img, 6,50,50)
        #img = cv2.equalizeHist(img)
        #img = cv2.Canny(img,90,250)
        img = cv2.Canny(img,self._canny_low,self._canny_high)
        self._edgeImg = img.copy()

        
        filename = "win_%d_%d_edge_o_%d.jpg" % (self._origCentroidY, self._origCentroidX,self._orientation)
        cv2.imwrite(os.path.join(self._outDir, filename), img)

        # Radiometric histogram calculation begins
        # Measure from centroid outward to edge of blob
        rVals = []
        thetaVals = []

        xarr = np.arange(-self._centroid[1], self._centroid[1] + 1, 1)
        yarr = np.arange(self._centroid[0], -self._centroid[0] - 1, -1)

        xg, yg = np.meshgrid(xarr, yarr)

        for x in range(img.shape[1]):
            for y in range(img.shape[0]):
                xCoordinate = xg[y][x]
                yCoordinate = yg[y][x]
                pixel = img[y][x]
                if not((xCoordinate == 0) and (yCoordinate == 0)) and pixel > 10:
                    # Calculate distance and angle from centroid
                    rad = np.sqrt(np.square(xCoordinate) + np.square(yCoordinate))
                    theta = np.arctan2(yCoordinate, xCoordinate)
                    if theta < 0:
                        theta = theta + 2*np.pi
                    rVals.append(rad)
                    thetaVals.append(theta)

        radiusBins = np.logspace(np.log10(self._rmin),np.log10(self._rmax * np.sqrt(2)),6)
        thetaBins = np.arange(0,2*np.pi+0.001, np.pi/6)
        H, xe, ye = np.histogram2d(rVals, thetaVals, bins=[radiusBins, thetaBins],normed=True)
        self._shapeHist = H
        self._xe = xe
        self._ye = ye

        rot = int(self._orientation/30)
        self._shapeHist = np.roll(self._shapeHist,-rot)

        eigVals, eigVec = np.linalg.eig(self._img)
        self._eigVals = eigVals
        self._eigVec = eigVec
        self._idx = eigVals.argsort()[::-1]


    def _calcHistDist(self, otherHist, rowIdx=[]):
        if len(rowIdx) == 0:
            return np.linalg.norm(self._shapeHist-otherHist.getShapeHist())
        else:
            return np.linalg.norm(self._shapeHist[rowIdx]-otherHist.getShapeHist()[rowIdx])

    def _calcMinHistDist(self, otherHist, rowIdx=[]):
        minDist = 9999999
        h = otherHist.getShapeHist()
        for i in range(h.shape[1]):
            rotHist = np.roll(h,i)
            dist = self._calcHistDist(otherHist,rowIdx=rowIdx)
            if dist < minDist:
                minDist = dist
        dist = minDist
        return dist

    def _calcHistEMD(self, otherHist, hist1weights = [], hist2weights = [], rowIdx=[]):
        hist1 = None
        hist2 = None

        if len(rowIdx) == 0:
            hist1 = self.getShapeHist()
            hist2 = otherHist.getShapeHist()
        else:
            hist1 = self.getShapeHist()[rowIdx]
            hist2 = otherHist.getShapeHist()[rowIdx]
            

        if not len(hist1weights):
            hist1weights = np.ones(hist1.shape)

        if not len(hist2weights):
            hist2weights = np.ones(hist1.shape)

        a64 = cv.fromarray(np.dstack((hist1weights, hist1))[0].copy())
        a32 = cv.CreateMat(a64.rows, a64.cols, cv.CV_32FC1)
        cv.Convert(a64, a32)
         
        b64 = cv.fromarray(np.dstack((hist2weights, hist2))[0].copy())
        b32 = cv.CreateMat(b64.rows, b64.cols, cv.CV_32FC1)
        cv.Convert(b64, b32)
        return cv.CalcEMD2(a32,b32,cv.CV_DIST_L2) 
            


    def _test_histogramDistance(self, otherHist, **kwargs):
        """
        Compares this histogram to the passed histogram using a Euclidian distance metric.
        Euclidian distance is also known as 'ordinary ' distance. In general, n-dimensional
        Euclidian distance is defined as follows:

                    d(p, q) = sqrt((p1 - q1)^2 + (p2 - q2)^2 + (p3 - q3)^2 + ... + (pn - qn)^2)

        Each point in this histogram is defined as a bin value. In this case, our histogram is 5 by 12
        bins in size
        :param:
            otherHist:  the other histogram to compare 'this' histogram against.
            tol:        the distance tolerance to allow. Default is no tolerance. If a tolerance is provided,
                        the return value will be 0 if the distance lies within the tolerance. Any value outside
                        the tolerance will return dist - <calcuated distance>.
            bestFit:    if True, the otherHist histogram will be shifted over all ranges of theta in order to 
                        come up with the orientation with the smallest euclidian distance

        :return: Returns the 'distance' the histograms are from each other. Positive value if valid, negative value
                 if the histograms do not match in size, and 'None' if the provided argument is not a histogram.
        """
        tol=0
        bestFit=False
        dist = 9999999
        distMetric = ""
        rowIdx = self.getMostImpShapeHistRows()[:3]

        if 'distMetric' in kwargs:
            distMetric = kwargs['distMetric']

        if 'tol' in kwargs:
            tol = kwargs['tol']

        if 'bestFit' in kwargs:
            bestFit = kwargs['bestFit']


        if distMetric == "DIST_EUCLIDIAN":
            if not bestFit:
                dist = self._calcHistDist(otherHist,rowIdx=rowIdx)
            else:
                dist = self._calcMinHistDist(otherHist,rowIdx=rowIdx)

        if distMetric == "DIST_EMD":
            dist = self._calcHistEMD(otherHist,rowIdx=[1,2,3,4])

        self.logger.debug("shapeDist=%.4f\n"%(dist))

        if dist < tol:
            return (True, dist)
        return (False, dist)

    def _test_edgeHist(self, otherHist):
        return False

    def _test_variance(self, otherHist):
        # Do zero mean and unit variance normalization
        rawImg_norm = self.calcZeroMeanUnitVarImg()
        rawImgOther_norm = otherHist.calcZeroMeanUnitVarImg()
        self.logger.debug("var=%.4f  refVar=%.4f\n"%(rawImgOther_norm.var(),rawImg_norm.var()))

        # This number 0.0005 was chosen empirically from a sample of 10 noise images
        #if rawImgOther_norm.var()/rawImg_norm.var() > 2.5:
        if rawImgOther_norm.var() > 0.0005:
            return False
        else:
            return True

    def _test_eigenVector(self, otherHist):
        #eigDotProd = np.abs(self._eigVec[:,0].dot(self._eigVec[:,1]))
        #eigDotProd = self._eigVec[:,0].dot(self._eigVec[:,1])
        #angle = np.arccos(np.clip(np.dot(self._eigVec[:,0], self._eigVec[:,1]),-1,1))
        angle = np.angle(np.arccos(np.clip(np.vdot(self._eigVec[:,0], self._eigVec[:,1]),-1,1)))


        #eigDotProdOtherHist = np.abs(otherHist._eigVec[:,0].dot(otherHist._eigVec[:,1]))
        #eigDotProdOtherHist = otherHist._eigVec[:,0].dot(otherHist._eigVec[:,1])
        #angleOtherHist = np.arccos(np.clip(np.dot(otherHist._eigVec[:,0], otherHist._eigVec[:,1]),-1,1))
        angleOtherHist = np.angle(np.arccos(np.clip(np.vdot(otherHist._eigVec[:,0], otherHist._eigVec[:,1]),-1,1)))

        #eigDist = np.sqrt(np.square(eigDotProd - eigDotProdOtherHist))
        #eigDist = np.sqrt(np.square(angle-angleOtherHist))
        eigDist = np.linalg.norm(angle-angleOtherHist)
        print angle, angleOtherHist
        return None



    #def compare(self, otherHist, **kwargs):
    #    if self._test_histogramDistance(otherHist, **kwargs):
    #    #if self._test_histogramDistance(otherHist, **kwargs) and self._test_variance(otherHist):
    #        return True
    #    return False


    def compare(self, otherHist, **kwargs):

        # Using namedtuple for future expansion of return values that we might want
        compareResult = collections.namedtuple('histResult',['result','shapeDist'])

        shapeRes,shapeDist = self._test_histogramDistance(otherHist, **kwargs)

         # TODO: if have multiple tests, have a mechanism to get majority vote
        result = shapeRes

        r = compareResult(result,shapeDist)
        return r


    def getShapeHist(self):
        """
        :return: Returns a copy of this histogram
        """
        return self._shapeHist

    def getShapeHistSum(self):
        histSum = self._shapeHist.sum()
        histSum=self._edgeImg.sum()/255
        return histSum
    
    def getRawImage(self):
        return self._img

    def getEdgeImage(self):
        return self._edgeImg

    def getMostImpShapeHistRows(self):
        return  np.argsort(self._shapeHist.sum(axis=1))[::-1]

    def calcZeroMeanUnitVarImg(self):
        img_norm = (self._img - self._img.mean())/self._img.var()
        return img_norm

    def tolist(self):
        return self._shapeHist.tolist()


    def __str__(self):
        histStr = str(self._origCentroid) + "\n"+ str(self._shapeHist) + "\n" + str(self._xe) + "\n" + str(self._ye)
        return str(histStr)

        










