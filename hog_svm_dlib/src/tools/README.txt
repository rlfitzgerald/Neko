*------------*
|   TOOLS    |
*------------*
  Here is a brief description of the tools within this directory

  * contrast_normalize.py  -- Applies contrast normalization to all images within a directory.
                              Option to conver to grayscale

  * crop_to_multiple.py    -- Resizes all jpgs and pngs to be a multiple of a given number. Useful as
                              a preprocessing step to tiling an image of negatives. For example, say
                              you have an image that does not contain your object of interest and you
                              want to make as many 64x64 sized images out of it as possible (say 
                              via imagemagick). This script will crop the image to its largest
                              multiple so that it can be tiled evenly. Use with mycrop.sh

  * extractImages.py       -- Extract images labeled with the dlib imglab tool

  * fixData.py             -- Will normalize all height and width attributes of a given xml file
                              generated via dlib's imglab tool to their average. This is useful
                              for when you are training off of data of different sizes but who
                              all have the same aspect ratio (dlib can be picky on this)


  * imglab                 -- dlib's image lab tool for labeling your data set. May need to be
                              recompiled. This can be done in the libs/dlib-18.12/tools/imglab directory

  * make_dlib_xml.py       -- Generates a dlib xml file used for HoG SVM training from all jpgs and 
                              pngs within a given directory. Make sure to specify a label if
                              applicable

  * mycrop.sh              -- Crops all images within its current directory to 64x64. Use in 
                              conjuction with crop_to_multiple.py to get tiles

  * myflipLR.sh            -- Creates a copy of a left/right flip of all images within its
                              current directory

  * myflipUD.sh            -- Creates a copy of a up/down flip of all images within its current directory

  * myresize.sh            -- Creates a resized copy of all images within its current directory

  * myrotate_rescale.sh    -- Creates a rotated copy of all images within its current directory
                              and rescales them such that there isn't any black background pixels
                              left over from the rotation

  * organize_flip_flops.sh -- A helper script that shuffles L/R and U/D flips generated from 
                              myflipLR.sh and myflipUD.sh into separate directories

  * rename_images.py       -- Renames all jpgs and pngs to img_#.jpg where # is a digit counting
                              from 1 to number of images. Options to change filename and starting
                              count. Useful to managing image datasets

  * shuffle_images.py      -- Will take all jpgs in a given directory and randomly bin them into
                              a specified number of subdirectories. Useful for creating randomized
                              data sets

