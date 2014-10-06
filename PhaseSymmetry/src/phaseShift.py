import cv2
import pymeanshift as pms


#input arguments
def phaseShift(img):

    #img = cv2.imread(im)

    (segmented_image, labels_image, number_regions) = pms.segment(img, spatial_radius=6, range_radius=4.5, min_density=50)
    (segmented_image1, labels_image1, number_regions1) = pms.segment(img, spatial_radius=5, range_radius=4.5, min_density=50)
    (segmented_image2, labels_image2, number_regions2) = pms.segment(img, spatial_radius=3, range_radius=3.5, min_density=50)
    cv2.imshow('image',segmented_image)
    cv2.imshow('image1',segmented_image1)
    cv2.imshow('image2',segmented_image2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
