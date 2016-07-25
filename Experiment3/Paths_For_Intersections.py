__author__='architsh'

#parallel processing code to arrange paths by intersections
from multiprocessing import Process, Queue
import sys
from geopy.distance import vincenty

#Argument 1: Directory for the list of paths for every process
#Argument 2: List of intersections
#Argument 3: Directory where the details will be written in the text
#Argument 4: Directory where the paths are present

#keep it fixed, unless number of processes used to generate path segments from the main dataset is different
PROCESSES=20

intersections=[ [float(f) for f in line.split(',')] for line in open(sys.argv[2],'r').read().splitlines()]

path_by_intersection=Queue()

def allocate_to_intersections(process_num, intersections):
	path_list=open(sys.argv[1]+str(process_num)+'.txt','r')
	for path in path_list:
		
		latlong=[[float(f) for f in line.split(',')[9:11]] for line in open(sys.argv[4]+path+'.txt','r')]
		
		for i in len(intersections):
			for location in latlong:
				if vincenty(intersections[i],location).m<=50:
					path_by_intersection.put(str(i+1)+':'+path)
					continue

def main():
	global PROCESSES, intersections, path_by_intersection
	process_list=[]
	
	file_for_intersections=[]
	for i in len(intersections);
		file_for_intersections.append(open(sys.argv[3]+str(i+1)+'.txt','a'))

	for i in len(PROCESSES):
		process_list.append(Process(target=allocate_to_intersections,args=(i+1, intersections)))
		process_list[i].start()

	for i in len(PROCESSES):
		process_list[i].join()

	while not path_by_intersection.empty():
		file_num, path_id=path_by_intersection.get().split(':')
		file_for_intersections[file_num-1].write(path_id+'\n')

if __name__ == '__main__':
	main()