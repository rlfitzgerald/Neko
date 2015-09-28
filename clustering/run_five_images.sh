#!/usr/bin/env sh
SRC_DIR=five_images
DEST_DIR=five_images
RESULT_FILE=$DEST_DIR/five_images_results.txt
touch $RESULT_FILE
filearray=( cars_4 cars_5 cars_6 cars_7 cars_9 )


for FILE in "${filearray[@]}"
do
	echo "$FILE.jpg Results" >> $RESULT_FILE
	echo "------------------" >> $RESULT_FILE
	echo -n "NMS: " >> $RESULT_FILE
	python nms_cluster.py --image=$SRC_DIR/$FILE.jpg --data=$SRC_DIR/$FILE.dat >> $RESULT_FILE
	mv output.jpg $DEST_DIR/five_images_${FILE}_nms_cluster.jpg
	echo -n "DBSCAN: " >> $RESULT_FILE
	python dbscan_cluster.py --image=$SRC_DIR/$FILE.jpg --data=$SRC_DIR/$FILE.dat >> $RESULT_FILE
	mv output.jpg $DEST_DIR/five_images_${FILE}_dbscan_cluster.jpg
	echo -n "OPTICS: " >> $RESULT_FILE
	python optics_cluster.py --image=$SRC_DIR/$FILE.jpg --data=$SRC_DIR/$FILE.dat >> $RESULT_FILE
	mv output.jpg $DEST_DIR/five_images_${FILE}_optics_cluster.jpg
	echo "" >> $RESULT_FILE
done
