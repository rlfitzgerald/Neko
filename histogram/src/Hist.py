

class Hist():

    def __init__(self, img):
        """Default constructor. Must be overloaded in order to properly handle the histogramming methodology used.
        The size and dimensionality of the class member 'hist' will vary based on the histogram method employed in your
        implementation of this class."""
        self._img = img
        self._hist = None
        self._calculate(img)

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




