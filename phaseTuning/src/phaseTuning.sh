#!/bin/bash

python phaseTuning.py structure.jpg 3 4 6 7 30 & 
python phaseTuning.py structure.jpg 4 5 6 7 30 & 
python phaseTuning.py structure.jpg 5 6 6 7 30 & 
python phaseTuning.py structure.jpg 6 7 6 7 30 & 
#python phaseTuning.py structure.jpg 7 8 7 16 30 & 
#python phaseTuning.py structure.jpg 8 9 7 16 30 & 
#python phaseTuning.py structure.jpg 9 10 7 16 30 &
wait

echo All processes finished successfully.
