
-All source code is contained in the folder "src"

-Dependenices for all provided python code is listed in "tools"

-Code from which some of our python is ported, along with the appropriate papers which
 provide the relevent theory are provided in the folder "refrences" 


DESCRIPTION:

lowpassfilter.py is a port of some MATLAB code provided by Peter Kovesi of the Univeristy
of Western Austrailia's department of Computer Science. This code is used for the overall
phase symmetry calculation. The original MATLAB source code is provided in the "refrences"
folder, along with the paper in which the MATLAB source was refrenced and the phase 
symmetry calculation is explained.   


The directory "phaseTuning" (located within "src") contains a tool developed to discover 
the optimal parameter configuartion tuning for the phase symmetry transformation tool. 


To use this module, set the PYTHONPATH as follows
export PYTHONPATH=$PYTHONPATH:$PATH_TO/Neko/PhaseSymmetry:$PATH_TO/Neko/PhaseSymmetry/src

