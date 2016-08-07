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

intersections=[ [float(f) for f in line.split(',')] for line in open(sys.argv[2],'r').read().splitlines()[:]]

path_by_intersection=Queue()

def allocate_to_intersections(process_num, intersections, path_by_intersection):
	global PROCESSES
	# print 'Started Process #' +str(process_num)
	path_list=open(sys.argv[1]+str(process_num)+'.txt','r').read().splitlines()
	
	# flag=False
	# count=0
	for path in path_list:
		# print 'Checking path '+path+' in process #'+str(process_num)
		latlong=[[float(f) for f in line.split(',')[9:11]] for line in open(sys.argv[4]+path+'.txt','r').read().splitlines()]

		for i in range(len(intersections)):
			for location in latlong:
				if vincenty(intersections[i],location).m<=50:
					# print 'Checking path '+path+' in process #'+str(process_num)
					# print 'Found one!'
					# count+=1
					path_by_intersection.put(str(i+1)+':'+path)
					# if count>=10:
					# 	flag=True
					break
		# if flag:
		# 	print 'Breaking'
		# 	break

def main():
	global PROCESSES, intersections, path_by_intersection
	process_list=[]
	
	# test=oipen(sys.argv[3]+'test.txt','a')
	file_for_intersections=[]
	for i in range(len(intersections)):
		file_for_intersections.append(open(sys.argv[3]+str(i+1)+'.txt','a'))

	for i in range(PROCESSES):
		process_list.append(Process(target=allocate_to_intersections,args=(i+1, intersections, path_by_intersection)))
		process_list[i].start()

	for i in range(PROCESSES):
		process_list[i].join()
	
	while not path_by_intersection.empty():
		file_num, path_id=path_by_intersection.get().split(':')
		# print file_num, path_id
		# test.write(file_num+':'+path_id+'\n')
		file_for_intersections[int(file_num)-1].write(path_id+'\n')

if __name__ == '__main__':
	main()