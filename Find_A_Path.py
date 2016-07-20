__author__='architsh'

#not an official script, just to test if paths can be stitched together
#pass the file name as the only argument to this script
#will be testing various stuff

from multiprocessing import Process, Queue
import sys
from geopy.distance import vincenty

#comment these two lines if using a local machine
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

PROCESSES=20
file_process=0
file_id=0
q=Queue()

def check_path_set(process_num, info):
	print 'Started Process #' + str(process_num)
	global file_process, file_id, q
	
	entries=info.split(',')
	Time=float(entries[5])/1000000-35
	Lat=float(entries[9])
	Long=float(entries[10])
	Speed=float(entries[12])
	Heading=float(entries[13])
	start_set=open('./RouteTracing/start_data_'+str(process_num)+'_april_2013_5_100.txt','r').read().splitlines()

	# print Time, Lat, Long, Speed, Heading
	for path in start_set:
		entries=path.split(',')
		if int(entries[0])==file_process and int(entries[1])==file_id:
			continue
		else:
			if vincenty((float(entries[9]),float(entries[10])),(Lat, Long)).m<=20 and float(entries[5])/1000000-35-Time<=1 and float(entries[5])/1000000-35-Time>=0 and abs(float(entries[13])-Heading)<=10 and abs(float(entries[12])-Speed)<=5:
				print 'Found: '+str(entries[0])+'_'+str(entries[1])
				print float(entries[9]),float(entries[10]), float(entries[5])/1000000-35, float(entries[12]), float(entries[11])
				
				q.put(entries[0]+'_'+entries[1])

def path_to_latlong(path_name):
	path=open('/scratch/user/architsh/PathSegmentsApril2013/'+str(path_name)+'.txt','r').read().splitlines()
	return [[float(f) for f in line.split(',')[9:11]] for line in path]

def main():
	global PROCESSES, file_id, file_process, q

	origin=np.array([42.22673, -83.83701])
	end=np.array([42.33316,-83.62981])
	supp=np.array([end[0],origin[1]])

	#linear mapping
	dotmatrix=np.array([(1678/(origin[0]-end[0]),0),(0,2416/(end[1]-origin[1]))])

	#resolution of picture: replace parameters accordingly
	plt.xlim(0,2416)
	plt.ylim(1678,0)
	im=plt.imread('./final_img.png')
	implot=plt.imshow(im)
	plt.axis('off')
	
	print sys.argv[1]
	file_process,file_id=int(sys.argv[1].split('_')[0]), int(sys.argv[1].split('_')[1])
	path_end_info=open('./RouteTracing/end_data_'+str(file_process)+'_april_2013_5_100.txt','r').read().splitlines()
	
	latlong=np.array(path_to_latlong(sys.argv[1]))
	coordinates=latlong-supp
	coordinates=coordinates.dot(dotmatrix)
	plt.plot(coordinates[:,1],coordinates[:,0])
	
	process_list=[]
	for i in range(PROCESSES):
		process_list.append(Process(target=check_path_set, args=(i+1, path_end_info[file_id-1])))
		process_list[i].start()
		process_list[i].join()

	while not q.empty():
		joinee=q.get()
		print joinee
		latlong=np.array(path_to_latlong(joinee))
		coordinates=latlong-supp
		coordinates=coordinates.dot(dotmatrix)
		plt.plot(coordinates[:,1],coordinates[:,0])

	plt.savefig('img_'+str(sys.argv[1]),ext='png',close=False,verbose=True,dpi=350,bbox_inches='tight',pad_inches=0)
	plt.close()

if __name__ == '__main__':
	main()