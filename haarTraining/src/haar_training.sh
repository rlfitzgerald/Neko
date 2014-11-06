#!/usr/bin/env bash

find ./images/positive/ -type f -name '*.png' > positives.dat
find ./images/negative/ -type f -name '*.png' > negatives.dat

NUMPOS=$(wc -l < collection.dat)
NUMNEG=$(wc -l < negatives.dat)

[ -d samples ] && rm -r samples
mkdir samples

# create samples.vec file needed by classifier
perl createtestsamples.pl positives.dat negatives.dat samples 1500 "opencv_createsamples -bgcolor 0 -bgthresh 0 -maxxangle 1.1 -maxyangle 1.1 -maxzangle 0.5 -maxidev 40 -w 20 -h 20"
find ./samples -name '*.vec' > samples.txt
./mergevec samples.txt samples.vec


[ -d classifier ] && rm -r classifier
mkdir classifier

# train classifier to detect positive images
# for precalculation you can set the amount of memory to use
# set sample size of positive images, 20 x 20 seems to work well
#opencv_traincascade -data classifier -featureType HAAR -vec samples.vec -bg negatives.dat -numPos $NUMPOS -numNeg $NUMNEG -numStages 20 -precalcValBufSize 6000 -precalcIdxBufSize 6000 -minHitRate 0.7 -maxFalseAlarmRate 0.5 -mode ALL -w 20 -h 20
#opencv_traincascade -data classifier -vec samples.vec -bg negatives.dat -numStages 20 -precalcValBufSize 6000 -precalcIdxBufSize 6000 -minHitRate 0.7 -maxFalseAlarmRate 0.5 -mode ALL -w 20 -h 20
opencv_traincascade -data classifier -featureType HAAR -vec samples.vec -bg negatives.dat -numStages 20 -minHitRate 0.8 -maxFalseAlarmRate 0.5 -numPos 700 -numNeg 1549 -w 20 -h 20 -mode ALL -precalcValBufSize 1024 -precalcIdxBufSize 1024
