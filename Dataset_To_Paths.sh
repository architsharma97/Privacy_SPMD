#!/bin/bash

#update the location of csv file
file_april_2013=/scratch/user/architsh/Data/april_BsmP1.csv
file_october_2012=/scratch/user/architsh/Data/october_BsmP1.csv


#time in seconds after which two tags would be considered belonging to different trips
time_diff=5

#distance in metres after which two tags would be considered belonging to different trips
max_dist=100

#directories where files will be stored
directory_april_2013=/scratch/group/sshakkot/PathSegmentsApril2013/
directory_october_2012=/scratch/group/sshakkot/PathSegmentsOctober2012/

echo 'Breaking April 2013 File into Path Segments'
python ./Break_Into_Path_Segment_Multiprocessing.py $file_april_2013 $time_diff $max_dist april 2013 $directory_april_2013
echo 'Done Breaking April 2013 File'
echo 'Breaking October 2013 File into Path Segments'
python ./Break_Into_Path_Segment_Multiprocessing.py $file_october_2012 $time_diff $max_dist october 2012 $directory_october_2012
echo 'Done Breaking October 2012'
echo 'Script DONE'
