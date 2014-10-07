import cv2
import pymeanshift as pms


#input arguments
def meanShift(filename):

    img = cv2.imread(filename)
    (segmented_image, labels_image, number_regions) = pms.segment(img, spatial_radius=6, range_radius=4.5, min_density=50)
    cv2.imwrite('segmented_%s' % filename, segmented_image)
