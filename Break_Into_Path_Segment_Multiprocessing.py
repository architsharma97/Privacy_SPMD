__author__='architsh'

import sys
from multiprocessing import Pool, Process, Queue
from geopy.distance import vincenty
import os

#Argument #1: Location of the file 
#Argument #2: Time Difference
#Argument #3: Maximum distance
#Argument #4: Month of Dataset
#Argument #5: Year of Dataset
#Argument #6: Directory where new files should be written

PROCESSES=20
FILE_SIZE=os.path.getsize(sys.argv[1])
print FILE_SIZE
CHUNK_SIZE=FILE_SIZE/PROCESSES
print CHUNK_SIZE
time_diff=int(sys.argv[2])
max_dist=int(sys.argv[3])

def break_into_paths(chunk_num, q):
	global PROCESSES, FILE_SIZE, CHUNK_SIZE, time_diff, max_dist

	data_file=open(sys.argv[1],'r')
	seekpoint_original=chunk_num*CHUNK_SIZE

	print 'Seeking in process #'+str(chunk_num+1)
	data_file.seek(seekpoint_original)
	seekpoint=seekpoint_original
	
	#synchronizes the seekpoint to the appropriate character (beginning of a new data entry)
	
	print 'Synchronizing process #'+str(chunk_num+1) 
	if chunk_num:
		seekpoint-=1
		data_file.seek(seekpoint)
		c=data_file.read(1)
		while not c=='\n':
			seekpoint-=2
			data_file.seek(seekpoint)
			c=data_file.read(1)
		seekpoint+=1

	data_file.seek(seekpoint)

	# print 'Reading in process #'+str(chunk_num+1)
	# if chunk_num==PROCESSES-1:
	# 	data=data_file.read().splitlines()
	# else:
	# 	data=data_file.read(CHUNK_SIZE+abs(seekpoint_original-seekpoint)).splitlines()

	# last_line=data[len(data)-1]
	# if last_line[len(last_line)-1]=='\n':
	# 	num_lines=len(data)
	# else:
	# 	num_lines=len(data)-1
	
	print 'Opening start and end files for Process #'+str(chunk_num+1)
	start_file=open('./RouteTracing/start_data_'+str(chunk_num+1)+'_'+sys.argv[4]+'_'+sys.argv[5]+'_'+sys.argv[2]+'_'+sys.argv[3]+'.txt','a')
	end_file=open('./RouteTracing/end_data_'+str(chunk_num+1)+'_'+sys.argv[4]+'_'+sys.argv[5]+'_'+sys.argv[2]+'_'+sys.argv[3]+'.txt','a')
	
	file_num=1

	paths_dir=sys.argv[6]

	#print 'Opening path segment file:'+str(chunk_num+1)+'_'+str(file_num)
	path_file=open(paths_dir+str(chunk_num+1)+'_'+str(file_num)+'.txt','a')
	
	# prev_line=data[0]
	
	flag=True

	# start_file.write(str(chunk_num+1)+','+str(file_num)+','+data[0]+'\n')
	# path_file.write(str(chunk_num+1)+','+str(file_num)+','+data[0]+'\n')
	
	# entries=data[0].split(',')

	# ID_prev=int(entries[0])
	# Lat_prev=float(entries[7])
	# Long_prev=float(entries[8])
	# time_prev=float(entries[3])/1000000-35

	read_bytes=0
	for line in data_file:
		
		if not chunk_num==PROCESSES-1:
			read_bytes+=len(line)
			if read_bytes > CHUNK_SIZE+abs(seekpoint_original-seekpoint):
				break

		if flag:
			flag=False
			start_file.write(str(chunk_num+1)+','+str(file_num)+','+line)
			path_file.write(str(chunk_num+1)+','+str(file_num)+','+line)
			
			# if line[len(line)-1]=='\n':
			# 	print 'Yes'
			# else:
			# 	print 'No'
			
			entries=line.split(',')

			ID_prev=int(entries[0])
			Lat_prev=float(entries[7])
			Long_prev=float(entries[8])
			time_prev=float(entries[3])/1000000-35
			prev_line=line
		
		else:
			entries=line.split(',')
			
			ID=int(entries[0])
			Lat=float(entries[7])
			Long=float(entries[8])
			time=float(entries[3])/1000000-35

			if not (ID==ID_prev and time-time_prev>=0 and time-time_prev<=time_diff and vincenty((Lat,Long),(Lat_prev,Long_prev)).m<=max_dist):
				end_file.write(str(chunk_num+1)+','+str(file_num)+','+prev_line)
				file_num+=1
				path_file.close()
				
				#print 'Opening path segment file:'+str(chunk_num+1)+'_'+str(file_num)
				path_file=open(paths_dir+str(chunk_num+1)+'_'+str(file_num)+'.txt','a')
				start_file.write(str(chunk_num+1)+','+str(file_num)+','+line)

			path_file.write(str(chunk_num+1)+','+str(file_num)+','+line)

			prev_line=line
			ID_prev=ID
			Lat_prev=Lat
			Long_prev=Long
			time_prev=time

	end_file.write(str(chunk_num+1)+','+str(file_num)+','+prev_line)
	
	q.put(str(chunk_num)+':'+str(file_num))
	print 'Closing Process #'+str(chunk_num+1)

def main():
	global PROCESSES, FILE_SIZE, CHUNK_SIZE, time_diff, max_dist

	#pool=Pool(processes=PROCESSES)
	#files_counts=pool.map(break_into_paths, range(PROCESSES))
	#pool.join()
	
	q=Queue()
	process_list=[]
	for i in range(PROCESSES):
		process_list.append(Process(target=break_into_paths,args=(i,q)))
		process_list[i].start()
	
	for i in range(PROCESSES):	
		process_list[i].join()
	
	#print files_counts
	path_files_counts=open('./RouteTracing/path_files_counts_'+sys.argv[4]+'_'+sys.argv[5]+'_'+sys.argv[2]+'_'+sys.argv[3]+'.txt','a')
	for count in range(PROCESSES):
		path_files_counts.write(str(q.get())+'\n')

if __name__ == '__main__':
	main()
