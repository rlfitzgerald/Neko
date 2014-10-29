#!/usr/bin/env bash

find ./images/positive/ -type f -name '*.png' > positives.dat
find ./images/negative/ -type f -name '*.png' > negatives.dat

[ -f collection.dat ] && rm -f collection.dat

# get width and height of each image, output to collection.dat file
for f in $(cat positives.dat); do
    dim=$(identify "$f" | cut -d ' ' -f 3 | tr 'x' ' ')
    echo "$f 1 0 0 $dim"
done > collection.dat

#NUMPOS=$(wc -l collection.dat)
NUMPOS=$(wc -l < collection.dat)
NUMNEG=$(wc -l < negatives.dat)

[ -f samples.vec ] && rm -f samples.vec

# create samples.vec file needed by classifier
opencv_createsamples -info collection.dat -bgcolor 0 -bgthresh 0 -vec samples.vec -num $NUMPOS -w 20 -h 20

# train classifier to detect positive images
# for precalculation you can set the amount of memory to use
# set sample size of positive images, 20 x 20 seems to work well
opencv_traincascade -data classifier -featureType HAAR -vec samples.vec -bg negatives.dat -numPos $NUMPOS -numNeg $NUMNEG -numStages 20 -precalcValBufSize 6000 -precalcIdxBufSize 6000 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -mode ALL -w 20 -h 20
