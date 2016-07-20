__author__='architsh'

#script to filter legit paths inside ann arbor city 
center_ann_arbor=(42.2808,-83.7430)

#Argument 1: Distance from centre of ann arbor under which it would be considered inside the city. 
#Argument 2: Folder containing lists of legit paths
#Argument 3: Folder of path segments
#Argument 4: Folder to which the lists of city paths will be written

import sys
from geopy.distance import vincenty
from multiprocessing import Process

#keep it same as the number of processes in previous scripts used to break data/filter legit paths
PROCESSES=20
radius=int(sys.argv[1])

def filter_city_paths(process_num):
	global PROCESSES, radius
	print 'Starting process #'+str(process_num)
	legit_list=open(sys.argv[2]+'/'+str(process_num)+'.txt','r').read().splitlines()
	city_paths_list=open(sys.argv[4]+'/'+str(process_num)+'.txt','a')
	for entry in legit_list:
		print 'In '+str(entry)
		path=open(sys.argv[3]+'/'+entry+'.txt','r')
		for line in path:
			entries=line.split(',')
			Lat=float(entries[9])
			Long=float(entries[10])
			if vincenty(center_ann_arbor,(Lat,Long)).m<=radius:
				print 'Process #' + str(process_num) +' found city path '+str(entry) 
				city_paths_list.write(str(entry)+'\n')
				break
		path.close()
	print 'Process #' + str(process_num) +' done!'

def main():
	global PROCESSES, radius
	process_list=[]
	for i in range(PROCESSES):
		process_list.append(Process(target=filter_city_paths, args=(i+1,)))
		process_list[i].start()
	
	for i in range(PROCESSES):
		process_list[i].join()

if __name__ == '__main__':
	main()
