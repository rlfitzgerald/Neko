import sys, cv2, bob, optparse, os
import numpy as np
from matplotlib import pyplot

def gabor(filename):
    #read image
    imArray = cv2.imread(filename)
    imArray = cv2.cvtColor(imArray, cv2.COLOR_RGB2GRAY)
    
    #compute transform
    gwt = bob.ip.GaborWaveletTransform()
    gwtResult = gwt.perform_gwt(imArray)
    
    return gwtResult, gwt

def gaborPlot(filename):
    
    gwtResult, gwt = gabor(filename)
    wavelets_image = np.zeros(gwtResult[0].shape, np.float)
    for kernel in gwtResult:
        wavelets_image += kernel
    
    imageName = os.path.splitext(filename)[0]
    wavelets_image *= 255/np.max(np.max(wavelets_image))    
    cv2.imwrite("%s_wavelet_superposition.pgm" %(str(imageName)), wavelets_image)
    
    #create figure
    pyplot.figure(figsize=(20,15))
    pyplot.subplot(121)
    pyplot.imshow(wavelets_image, cmap='gray')
    pyplot.title("Gabor Wavelet Superposition")
    
    #pyplot.show()    
    #plot the results of the transform for some wavelets
    for scale in (0,2,4):
        for direction in (0,2,4):
            pyplot.subplot(3, 6, 4+scale*3+direction/2)
            pyplot.imshow(np.real(gwtResult[scale*gwt.number_of_directions+direction]),  cmap='gray')
            newName = os.path.splitext(filename)[0]
            tempImage = np.real(gwtResult[scale*gwt.number_of_directions+direction])
            #tempImage *= 255/(np.max(np.max(tempImage)))
            cv2.imwrite("%s_scale_%d_direction_%d.pgm" %(str(newName), scale, direction), tempImage)
            pyplot.title("Scale %d, direction %d" %(scale, direction))
            #pyplot.gca().invert_yaxis()
    
    pyplot.tight_layout()
    pyplot.show()
    sumImage = np.zeros(gwtResult[0].shape, np.float)
    for dir in range(8):
        sumImage += np.real(gwtResult[dir])
    sumImage *= 255/(np.max(np.max(sumImage)))
    cv2.imwrite("scale0.pgm", sumImage)
    
    
def waveletSums(filename):
    
    gwtResult, gwt = gabor(filename)
    
    #epsilon to prevent zero division
    epsilon = 1e-4
    
    #initialize variables
    scaleReals = np.zeros((gwt.number_of_scales,) + gwtResult[0].shape, np.float)
    scaleImaginary = np.zeros((gwt.number_of_scales,) + gwtResult[0].shape, np.float)
    symNTop = np.zeros(gwtResult[0].shape, np.float)
    symNBot = np.zeros(gwtResult[0].shape, np.float)

    totalSumAn = np.zeros(gwtResult[0].shape, np.float)
    totalEnergy = np.zeros(gwtResult[0].shape, np.float)
    tau = -1
    totalTau = -1
    mult = 2.0
    k = 2
    T = 0
    #sum all directions for each scale
    for direction in range(gwt.number_of_directions):
        Energy_ThisOrient = np.zeros(gwtResult[0].shape, np.float)
        sumAn_ThisOrient = np.zeros(gwtResult[0].shape, np.float)

        for scale in range(gwt.number_of_scales):
            index = scale * gwt.number_of_directions + direction
            modIndex = index / gwt.number_of_directions

            An = np.abs(gwtResult[index])
            sumAn_ThisOrient = sumAn_ThisOrient + An
            Energy_ThisOrient = Energy_ThisOrient + np.abs(np.real(gwtResult[index])) - np.abs(np.imag(gwtResult[index]))

            if scale == 0:
                tau = np.median(sumAn_ThisOrient)/np.sqrt(np.log(4))

            Energy_ThisOrient = Energy_ThisOrient + np.abs(np.real(gwtResult[index])) - np.abs(np.imag(gwtResult[index]))

        
        totalTau = tau * (1 - np.power((1/mult),gwt.number_of_scales))/(1 - (1/mult))
        EstNoiseEnergyMean = totalTau*np.sqrt(np.pi/2)
        EstNoiseEnergySigma = totalTau*np.sqrt((4-np.pi)/2)
        T = np.max(EstNoiseEnergyMean + k*EstNoiseEnergySigma, epsilon)
        Energy_ThisOrient = Energy_ThisOrient-T

        totalSumAn += sumAn_ThisOrient
        totalEnergy += Energy_ThisOrient
    
    phaseSym = np.divide(np.maximum(totalEnergy,np.zeros(gwtResult[0].shape, np.float)), (totalSumAn + epsilon))
    
    phaseSym = phaseSym * 255/(np.max(phaseSym))
    cv2.imwrite("SymSymSalabim.pgm", phaseSym)
    pyplot.imshow(phaseSym,  cmap='gray')
    pyplot.show()        
    
    
    
    ##initialize variables
    #scaleReals = np.zeros((gwt.number_of_scales,) + gwtResult[0].shape, np.float)
    #scaleImaginary = np.zeros((gwt.number_of_scales,) + gwtResult[0].shape, np.float)
    #symNTop = np.zeros(gwtResult[0].shape, np.float)
    #symNBot = np.zeros(gwtResult[0].shape, np.float)
    #aN = np.zeros((gwt.number_of_scales,) + gwtResult[0].shape, np.float)
    
    #for scale in range(gwt.number_of_scales):
    #    for direction in range(gwt.number_of_directions):
    #        index = scale * gwt.number_of_directions + direction
    #        modIndex = index / gwt.number_of_directions
    #        
    #        scaleReals[modIndex] += np.real(gwtResult[index])
    #        scaleImaginary[modIndex] += np.imag(gwtResult[index])
    #        
    #    evenSq = np.square(scaleReals[scale])
    #    oddSq = np.square(scaleImaginary[scale])
    #    aN[scale] = np.sqrt(evenSq + oddSq)
    #
    #for scale in range(gwt.number_of_scales):    
    #    symNTop += (np.floor(np.abs(scaleReals[scale]) - np.abs(scaleImaginary[scale])))
    #    symNBot += aN[scale] 
    # 
    # Sym = (symNTop / (symNBot + epsilon)) + 0.5
    # print Sym
    
    #Sym = Sym * 255 / np.max(np.max(Sym))
#    cv2.imwrite("SymSymSalabim.pgm", Sym)
#    pyplot.imshow(Sym,  cmap='gray')
#    pyplot.show()        
    #write summed images out
    #for i in range(len(scaleReals)):
    #    scaleReals[i] *= 255/(np.max(np.max(scaleReals[i])))
    #    scaleImaginary[i] *=  255/(np.max(np.max(scaleImaginary[i])))
    #    cv2.imwrite("Scale_%d_Real_part.pgm" %(i), scaleReals[i])
    #    cv2.imwrite("Scale_%d_Imaginary_part.pgm" %(i), scaleImaginary[i])
    # 
    #pyplot.imshow(scaleReals[0], cmap='gray')
    #pyplot.show()
    
    
        
            
def main(argv=None):
    if argv is None:
        argv = sys.argv

    desc = """%prog is a tool performs the Gabor wavelet transform on an input image(5 scales, 8 orientations)."""
    parser = optparse.OptionParser(description=desc, usage='Usage: ex) %prog imageFile.png')
    (opts, args) = parser.parse_args(argv)
    args = args[1:]

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

    #begin transform
    filename = argv[1]
    
    #Take gabor transform, plot results(only plot real part)
    #gaborPlot(filename)
    waveletSums(filename)


if __name__ == "__main__":
    sys.exit(main())
