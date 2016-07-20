__author__='architsh'

#plots the trips distinctly on the map, uncomment stuff to get the time size of a trip
#PACKET LOSSES: Certain trips would be distinctly colored, even if they might be part of the same trip
#Check the data 
import matplotlib.pyplot as plt
import numpy as np
import sys

def main():
	origin=np.array([42.22673, -83.83701])
	end=np.array([42.33316,-83.62981])
	supp=np.array([end[0],origin[1]])

	#linear mapping
	dotmatrix=np.array([(1678/(origin[0]-end[0]),0),(0,2416/(end[1]-origin[1]))])
	
	for i in range(1,len(sys.argv)):
		car_data=open('../IDWise/'+str(sys.argv[i])+'.csv','r').read().splitlines()
		
		prev_time=0
		latlong=[]

		#resolution of picture: replace parameters accordingly
		plt.xlim(0,2416)
		plt.ylim(1678,0)
		im=plt.imread('../final_img.png')
		implot=plt.imshow(im)
		plt.axis('off')
		start_time=0
		for entry in car_data[1:]:
			split=entry.split(',')
			if prev_time==0:
				start_time=float(split[0])
				print 'Start time: ' + str(start_time)
			if not (prev_time==0 or float(split[0])-prev_time<=50):
				latlong=np.array(latlong)
				coordinates=latlong-supp
				coordinates=coordinates.dot(dotmatrix)
				plt.plot(coordinates[:,1],coordinates[:,0])
				latlong=[]
				
				print (prev_time-start_time)/60
				start_time=float(split[0])
				print 'Start time: ' + str(start_time) 
			
			latlong.append([float(f) for f in split[1:3]])
			prev_time=float(split[0])
			
		print (prev_time-start_time)/60

		latlong=np.array(latlong)
		coordinates=latlong-supp
		coordinates=coordinates.dot(dotmatrix)
		plt.plot(coordinates[:,1],coordinates[:,0])
		plt.savefig("../IDWise/"+str(sys.argv[i])+'_trips',ext='png',close=False,verbose=True,dpi=350,bbox_inches='tight',pad_inches=0)
		plt.close()

if __name__ == '__main__':
	main()
