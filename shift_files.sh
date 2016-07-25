#!/bin/bash
file_dir='/scratch/user/architsh/PathSegmentsApril2013/'
ref_dir='/home/architsh/Privacy_SPMD/CityPaths/April2013/'

file_1=$ref_dir'10.txt'
file_2=$ref_dir'11.txt'
file_3=$ref_dir'12.txt'

final_dir='/scratch/user/architsh/subset/'

# test_file='legitimate_path_list_500.txt'

count=0
for file in $file_1 $file_2 $file_3
do 
	for line in $(cat $file) 
	do
		count=$((count+1))
		file_to_open=$file_dir$line'.txt'
		echo $file_to_open
		cp $file_to_open $final_dir
	done  
done

echo $count