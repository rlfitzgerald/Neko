+------------------------+
| NON-MAXIMUM SUPRESSION |
+------------------------+

  Description:
    Non-maximum supression defines each detection by a bounding box and a score.
    The detections are then sorted by score, and greedily selects the highest
    scoreing ones while skipping detections with bounding boxes that are at least
    50% covered by a bounding box of a previously selected detection. See
    "Object Detection with Discriminatively Trained Part Based Models" by 
    Pedro F. Felzenszwalb, Ross B. Girshick, David McAllester and Deva Ramanan
    for more information


  usage: nms_cluster.py [-h] -i IMAGE -d DATA [-p PROB] [-s MINSAMPLES]
  
  optional arguments:
    -h, --help            show this help message and exit
    -i IMAGE, --image IMAGE
                          input image name
    -d DATA, --data DATA  metadata image name
    -p PROB, --prob PROB  minimum probability (default 0.7)
    -s MINSAMPLES, --minsamples MINSAMPLES (default 2)
                          NMS minimum cluster size

	Recommended Settings:
    Depending on the fidelity of the detector, it is possible to obtain multiple
    hits on a target. Set the minimum samples per cluster to some threshold
    value that decreases the number of false positives. For instance, if you
    find that your detector generates at least 4 detections per target, set the
    minimum samples to 4.

  Output:
    nms_cluster.py will output an image file called "output.jpg" with the
    clustered detections. 

  Example:
    python nms_cluster.py --image=input_image.jpg --data=input_image.dat
    python nms_cluster.py --image=input_image.jpg --data=input_image.dat -s 4



+--------+
| DBSCAN |
+------- +

  Description:
    Finds core samples of high density and expands clusters from them. Good for data
    which contains clusters of similar density.


  usage: dbscan_cluster.py [-h] -i IMAGE -d DATA [-p PROB] [-e EPS]
                           [-s MINSAMPLES]

  optional arguments:
    -h, --help            show this help message and exit
    -i IMAGE, --image IMAGE
                          input image name
    -d DATA, --data DATA  metadata image name
    -p PROB, --prob PROB  minimum probability (default 0.7)
    -e EPS, --eps EPS     DBSCAN epsilon (default 15)
    -s MINSAMPLES, --minsamples MINSAMPLES (default 2)
                          DBSCAN minimum cluster size

	Recommended Settings:
    Depending on the fidelity of the detector, it is possible to obtain multiple
    hits on a target. Set the minimum samples per cluster to some threshold
    value that decreases the number of false positives. For instance, if you
    find that your detector generates at least 4 detections per target, set the
    minimum samples to 4. DBSCAN requires an epsilon (radius) by which to
    associate hits to a given cluster. Set this to the MINIMUM of the detection
    window stride (ex. 8 pixels). 

  Output:
    dbscan_cluster.py will output an image file called "output.jpg" with the
    clustered detections. 

  Example:
    python dbscan_cluster.py --image=input_image.jpg --data=input_image.dat
    python dbscan_cluster.py --image=input_image.jpg --data=input_image.dat -s 4 -e 8




+--------+
| OPTICS |
+------- +

  Description:
		Finds density-based clusters in spatial data. Its basic idea is similar to
    DBSCAN, but it addresses one of DBSCAN's major weaknesses: the problem of
    detecting meaningful clusters in data of varying density. In order to do so, the
    points of the database are (linearly) ordered such that points which are
    spatially closest become neighbors in the ordering.  Additionally, a special
    distance is stored for each point that represents the density that needs to be
    accepted for a cluster in order to have both points belong to the same cluster.
    This is represented as a dendrogram.


  usage: optics_cluster.py [-h] -i IMAGE -d DATA [-p PROB] [-r RAD]
                         [-s MINSAMPLES]

  optional arguments:
    -h, --help            show this help message and exit
    -i IMAGE, --image IMAGE
                          input image name
    -d DATA, --data DATA  metadata image name
    -p PROB, --prob PROB  minimum probability (default 0.7)
    -r RAD, --rad RAD     OPTICS max radius (default 15)
    -s MINSAMPLES, --minsamples MINSAMPLES (default 1)
                          OPTICS minimum cluster size

	Recommended Settings:
    Depending on the fidelity of the detector, it is possible to obtain multiple
    hits on a target. Set the minimum samples per cluster to some threshold
    value that decreases the number of false positives. For instance, if you
    find that your detector generates at least 4 detections per target, set the
    minimum samples to 4. While OPTICS does not require an explicit radius to be
    set, setting the radius does improve performance as it cuts down the number
    of points it has to consider when generating clusters. A recommended value
    for this is DETECTION_WINDOW_SIZE/4 <= radius <= DETECTION_WINDOW_SIZE.

  Special Considerations:
    There seems to be a bug in the OPTICS code that makes it unable to handle
    minsamples=1. Set this value greater than or equal to 2.

  Output:
    optics_cluster.py will output an image file called "output.jpg" with the
    clustered detections. 

  Example:
    python optics_cluster.py --image=input_image.jpg --data=input_image.dat
    python optics_cluster.py --image=input_image.jpg --data=input_image.dat -s 4 -r 16
