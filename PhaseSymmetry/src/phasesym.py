import optparse
import sys
import os
import numpy as np
from lowpassfilter import *

DEBUG=False



def phasesym(im, nscale=5, norient=6, minWaveLength=3, mult=2.1, sigmaOnf = 0.55, k=2.0, polarity=0):
    """  Arguments:
                   Default values      Description
     
         nscale           5    - Number of wavelet scales, try values 3-6
         norient          6    - Number of filter orientations.
         minWaveLength    3    - Wavelength of smallest scale filter.
         mult             2.1  - Scaling factor between successive filters.
         sigmaOnf         0.55 - Ratio of the standard deviation of the Gaussian 
                                 describing the log Gabor filter's transfer function 
                                 in the frequency domain to the filter center frequency.
         k                2.0  - No of standard deviations of the noise energy beyond
                                 the mean at which we set the noise threshold point.
                                 You may want to vary this up to a value of 10 or
                                 20 for noisy images 
         polarity         0    - Controls 'polarity' of symmetry features to find.
                                  1 - just return 'bright' points
                                 -1 - just return 'dark' points
                                  0 - return bright and dark points.
         noiseMethod      -1   - Parameter specifies method used to determine
                                 noise statistics. 
                                   -1 use median of smallest scale filter responses
                                   -2 use mode of smallest scale filter responses
                                    0+ use noiseMethod value as the fixed noise threshold.
     
      Return values:
         phaseSym              - Phase symmetry image (values between 0 and 1).
         orientation           - Orientation image. Orientation in which local
                                 symmetry energy is a maximum, in degrees
                                 (0-180), angles positive anti-clockwise. Note
                                 the orientation info is quantized by the number
                                 of orientations
         totalEnergy           - Un-normalised raw symmetry energy which may be
                                 more to your liking.
         T                     - Calculated noise threshold (can be useful for
                                 diagnosing noise characteristics of images).  Once you know
                                 this you can then specify fixed thresholds and save some
                                 computation time.
     
      Notes on specifying parameters:
      
      The parameters can be specified as a full list eg.
       >> phaseSym = phasesym(im, 5, 6, 3, 2.5, 0.55, 2.0, 0);
     
      or as a partial list with unspecified parameters taking on default values
       >> phaseSym = phasesym(im, 5, 6, 3);
     
      or as a partial list of parameters followed by some parameters specified via a
      keyword-value pair, remaining parameters are set to defaults, for example:
       >> phaseSym = phasesym(im, 5, 6, 3, 'polarity',-1, 'k', 2.5);
      
      The convolutions are done via the FFT.  Many of the parameters relate to the
      specification of the filters in the frequency plane.  The values do not seem
      to be very critical and the defaults are usually fine.  You may want to
      experiment with the values of 'nscales' and 'k', the noise compensation factor.
     
      Notes on filter settings to obtain even coverage of the spectrum
      sigmaOnf       .85   mult 1.3
      sigmaOnf       .75   mult 1.6     (filter bandwidth ~1 octave)
      sigmaOnf       .65   mult 2.1  
      sigmaOnf       .55   mult 3       (filter bandwidth ~2 octaves)
     
      For maximum speed the input image should have dimensions that correspond to
      powers of 2, but the code will operate on images of arbitrary size.
     
      See Also:  PHASECONG, PHASECONG2, GABORCONVOLVE, PLOTGABORFILTERS
    
      References:
          Peter Kovesi, "Symmetry and Asymmetry From Local Phase" AI'97, Tenth
          Australian Joint Conference on Artificial Intelligence. 2 - 4 December
          1997. http://www.cs.uwa.edu.au/pub/robvis/papers/pk/ai97.ps.gz.
     
          Peter Kovesi, "Image Features From Phase Congruency". Videre: A
          Journal of Computer Vision Research. MIT Press. Volume 1, Number 3,
          Summer 1999 http://mitpress.mit.edu/e-journals/Videre/001/v13.html
    """
    
    

    epsilon = 1e-4                      # Used to prevent division by zero
    rows, cols = im.shape
    imagefft = np.fft.fft(im)               # Fourier transform of image
    zero = np.zeros((rows, cols))

    totalEnergy = zero.copy()           # ndarray for accumulating weighted phase 
                                        # congruency values (energy)
    totalSumAn = zero.copy()            # ndarray for accumulating filter response
                                        # amplitude values
    orientation = zero.copy()           # ndarray storing orientation with greatest
                                        # energy for each pixel

    # Pre-compute some stuff to speed up filter construction
    #
    # Set up X and Y ndarrays with ranges normalized to +/- 0.5
    # The following code adjusts things appropriately for odd and even values
    # of rows and columns.


    if cols % 2:
        x_range = np.arange(-(cols - 1)/2, (cols - 1)/2 + 1, dtype=np.float)
        x_range = np.divide(x_range, np.float(cols-1))
    else:
        x_range = np.arange(-cols/2, (cols/2-1) + 1, dtype=np.float)
        x_range = np.divide(x_range, cols)

    if rows % 2:
        y_range = np.arange(-(rows-1)/2, (rows-1)/2 + 1, dtype=np.float)
        y_range = np.divide(y_range, np.float(rows - 1))
    else:
        y_range = np.arange(-rows/2, (rows/2-1) + 1, dtype=np.float)
        y_range = np.divide(y_range, rows)

    x, y = np.meshgrid(x_range, y_range)


    radius = np.sqrt(np.square(x) + np.square(y))           # ndarray values contain *normalized* radius from center
    theta = np.arctan2(-y,x)                                  # ndarray values contain polar angle
                                                            # (note negative y is used to give positive
                                                            # anti-clockwise angles)

    radius = np.fft.ifftshift(radius)                       # Quadrant shift radius and theta so that filters
    theta =  np.fft.ifftshift(theta)                        # are constructed wtih 0 frequency at the corners.
    radius[0][0] = 1                                        # Get rid of the 0 radius value at the 0
                                                            # frequency point (now at top-left corner)
                                                            # so that taking the log of the radius will
                                                            # not cause trouble

    sintheta = np.sin(theta)
    costheta = np.cos(theta)


    #print sintheta
    #print
    #print costheta
    #print
    
    #Filters are constructed in terms of two components.
    # 1) The radial component, which controls the frequency band that the filter
    #    responds to
    # 2) The angular component, which controls the orientation that the filter
    #    responds to.
    # The two components are multiplied together to construct the overall filter.

    # Construct the radial filter components...
    # First construct a low-pass filter that is as large as possible, yet falls
    # away to zero at the boundaries.  All log Gabor filters are multiplied by
    # this to ensure no extra frequencies at the 'corners' of the FFT are
    # incorporated as this seems to upset the normalisation process when
    # calculating phase congrunecy.
    
    lp = lowpassfilter((rows,cols), 0.4, 10)        #Radius 0.4, 'sharpness' 10
    logGabor = []
    
    for s in range(nscale):
        wavelength = minWaveLength * (mult**(s))  
        fo = 1.0/np.float(wavelength)               #Center frequency filter
        thisFilterTop = np.divide(radius, fo)
        thisFilterTop = np.log10(thisFilterTop)
        thisFilterTop = -(np.square(thisFilterTop))
        thisFilterBot = np.log10(sigmaOnf)
        thisFilterBot = np.square(thisFilterBot)
        thisFilterBot = thisFilterBot * 2
        thisFilter = np.divide(thisFilterTop, thisFilterBot)
        thisFilter = np.exp(thisFilter) 
        thisFilter = np.multiply(thisFilter, lp)    #Apply low pass filter
        thisFilter[0][0] = 0                        #Set the value at the 0 frequency point of the filter
        logGabor.append(thisFilter)
        
    
    #works until here !!!!!!!!!!!!!!!!
    #print loop ofo rtesting purposes
    
    return logGabor
    
    #The main loop...
    
    

    
    
