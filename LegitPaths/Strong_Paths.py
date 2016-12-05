__author__='architsh'
# strong paths are defined as the paths which have at least x tags or lines,
# x is provided by the user

import os
import sys
from multiprocessing import Process, Pool

# Argument 1: Number of tags/lines after which the path segment would be considered strong
# Argument 2: Directory in which the Path segments are present
# Argument 3: File which contains the information about number of path segments and the processes responsible for creating the path segment
# Argument 4: Directory in which the legit path information should be written

# average size 
size_of_line=144
min_points=int(sys.argv[1])
# keep it same as the number of processes used to break down the original file
PROCESSES=20

def legit(process_num, num_files):
	global size_of_line,min_points
	print 'In process #'+str(process_num)
	write_file=open(sys.argv[4]+'/'+str(process_num)+'.txt','a')
	for i in range(1,num_files+1):
		if float(os.path.getsize(sys.argv[2]+'/'+str(process_num)+'_'+str(i)+'.txt'))/size_of_line >=min_points:
			write_file.write(str(process_num)+'_'+str(i)+'\n')
	print 'Process #'+str(process_num)+' done!'

def main():
	path_count_file=open(sys.argv[3],'r').read().splitlines()
	process_list=[]
	for i in range(PROCESSES):
		process_list.append(Process(target=legit,args=(i+1,int(path_count_file[i]))))
		process_list[i].start()

	for i in range(PROCESSES):
		process_list[i].join()
		
if __name__ == '__main__':
	main()
