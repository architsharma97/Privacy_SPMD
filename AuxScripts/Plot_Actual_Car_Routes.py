__author__='architsh'

import matplotlib.pyplot as plt
import numpy as np
import sys

def main():
	origin=np.array([42.22673, -83.83701])
	end=np.array([42.33316,-83.62981])
	supp=np.array([end[0],origin[1]])

	#linear mapping
	dotmatrix=np.array([(1678/(origin[0]-end[0]),0),(0,2416/(end[1]-origin[1]))])

	#resolution of picture: replace parameters accordingly
	plt.xlim(0,2416)
	plt.ylim(1678,0)
	im=plt.imread('../final_img.png')
	implot=plt.imshow(im)
	plt.axis('off')

	flag=True
	latlong=[]
	with open('../RouteTracing/CarRoutes/'+str(sys.argv[1])+'.txt') as data_file:
		for line in data_file:
			entries=line.split(',')
			if flag:
				flag=False
				car_id=int(float(entries[0]))
				latlong.append([float(f) for f in entries[2:4]])
				prev_time=float(entries[1])
			else:		
				if not (car_id==int(float(entries[0])) and float(entries[1])-prev_time<=5 and float(entries[1])>=prev_time):
					car_id=int(float(entries[0]))
					latlong=np.array(latlong)
					coordinates=latlong-supp
					coordinates=coordinates.dot(dotmatrix)
					plt.plot(coordinates[:,1],coordinates[:,0])
					latlong=[]
				
				latlong.append([float(f) for f in entries[2:4]])
				prev_time=float(entries[1])

	latlong=np.array(latlong)
	coordinates=latlong-supp
	coordinates=coordinates.dot(dotmatrix)
	plt.plot(coordinates[:,1],coordinates[:,0])
	plt.savefig("../RouteTracing/CarRoutes/"+str(sys.argv[1]),ext='png',close=False,verbose=True,dpi=350,bbox_inches='tight',pad_inches=0)
	plt.close()

if __name__ == '__main__':
	main()
