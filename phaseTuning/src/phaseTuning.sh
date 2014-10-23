#!/bin/bash

python phaseTuning.py structure.jpg 5 6 16 30 & 
python phaseTuning.py structure.jpg 6 7 16 30 & 
python phaseTuning.py structure.jpg 7 8 16 30 & 
python phaseTuning.py structure.jpg 8 9 16 30 & 
python phaseTuning.py structure.jpg 9 10 16 30 &
wait

echo All processes finished successfully.
