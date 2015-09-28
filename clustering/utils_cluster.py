from matplotlib import pyplot as plt
from collections import defaultdict
import cv2
import numpy as np

def sortColors(colors, modN=10):
    colors_reordered = []
    dict = defaultdict(list)

    for i in range(len(colors)):
        dict[i%modN].append(colors[i])
    
    for key in dict:
        colors_reordered.extend(dict[key])
    return colors_reordered

def getClusterColors(numClusters):
    """
    INPUT:
        numClusters     The number of clusters to define unique colors for
    OUTPUT:
        RGB_tuples      A list of distinct colors for each cluster in RGB color space
    """
    cm = plt.get_cmap('jet')
    cgen = (cm(1.*i/numClusters) for i in range(numClusters))
    RGB_tuples = []
    for c in cgen:
        RGB_tuples.append([int(255*x) for x in c])
    RGB_tuples = sortColors(RGB_tuples,7)
    return RGB_tuples


def drawClusterColorsDBSCAN(img, data, dbResult):
    """
    INPUT:
        img             A copy of the original input image
        data            A list of list of clustered tuples
                        [[(X1,Y1),(X2,Y2)],[(X3,Y3),...]]
        dbResult        Resulting clusters from DBSCAN
    """

    #set up a dictionary for cluster member collection
    dict = defaultdict(list)

    labels = dbResult.labels_
    core_samples_mask = np.zeros_like(dbResult.labels_, dtype=bool)
    core_samples_mask[dbResult.core_sample_indices_] = True
    unique_labels = set(labels)
    unique_labels.remove(-1)
    colors = getClusterColors(len(unique_labels))

    for k in unique_labels:
        class_member_mask = (labels == k)
        for i in range(len(class_member_mask)):
            member = class_member_mask[i]
            if member:
                dict[k].append(data[i])

    for i, color in zip(dict, colors):
        entry = dict[i]
        for j in entry:
            tempCentroid = (int(j[0]), int(j[1]))
            cv2.circle(img, tempCentroid, 4, color, thickness=-1)
        (x,y),radius = cv2.minEnclosingCircle(np.int0(entry))
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(img,center,radius,color,2)

    print "Num Cars = " + str(len(unique_labels))


def drawClusterColorsOptics(img, data):
    """
    INPUT:
        img             A copy of the original input image
        data            A list of list of clustered tuples
                        [[(X1,Y1),(X2,Y2)],[(X3,Y3),...]]
    """

    colors = getClusterColors(len(data))


    for i, color in enumerate(colors):
        cluster = data[i]
        for j in cluster.points:
            tempCentroid = (int(j.latitude), int(j.longitude))
            cv2.circle(img, tempCentroid, 4, color, thickness=-1)
        centroid, radius= cluster.region()
        cv2.circle(img, (int(centroid.latitude),int(centroid.longitude)), int(radius), color, thickness=2)

    print "Num Cars = " + str(len(data))


def drawClusterColorsNMS(img, data):
    """
    INPUT:
        img             A copy of the original input image
        data            A list of list of clustered tuples
                        [[(X1,Y1),(X2,Y2)],[(X3,Y3),...]]
    """

    
    colors = getClusterColors(len(data))
    for i, color in enumerate(colors):
        x1 = data[i][0]
        y1 = data[i][1]
        x2 = data[i][2]
        y2 = data[i][3]
        cv2.rectangle(img, (x1,y1),(x2,y2), color, 2)

    print "Num Cars = %d"%(len(data))


