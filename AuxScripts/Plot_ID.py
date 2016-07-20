__author__= 'architsh'
#when you run the script, pass car id(s) as the argument(s)
#plots route separately

import matplotlib.pyplot as plt
import numpy as np
from math import sin,cos,pi
import sys

def main():
	origin=np.array([42.22673, -83.83701])
	end=np.array([42.33316,-83.62981])
	supp=np.array([end[0],origin[1]])
	
	#linear mapping
	dotmatrix=np.array([(1678/(origin[0]-end[0]),0),(0,2416/(end[1]-origin[1]))])
	
	for i in range(1,len(sys.argv)):
		car_data=open('../IDWise/'+ str(sys.argv[i]) + '.csv','r').read().splitlines()
		
		#get a latitude longitude array
		latlong=[]
		for entry in car_data[1:]:
			split=entry.split(',')
			if float(split[1])<=end[0] and float(split[1])>=origin[0] and float(split[2])<=end[1] and float(split[2])>=origin[1]:
				latlong.append([float(f) for f in split[1:3]])
		#print latlong

		#Wikipedia: Actual Distances, Not possible to scale onto map
		#x_per_degree=111412.84*cos(origin[0]*pi/180)-93.5*cos(3*origin[0]*pi/180)-0.118*cos(5*origin[0]*pi/180)
		#y_per_degree=111132.92-559.82*cos(2*origin[0]*pi/180)+1.175*cos(4*origin[0]*pi/180)-0.0023*cos(6*origin[0]*pi/180)
		
		#print x_per_degree,y_per_degree
		
		latlong=np.array(latlong)
		coordinates=latlong-supp
		coordinates=coordinates.dot(dotmatrix)

		#resolution of picture: replace parameters accordingly
		plt.xlim(0,2416)
		plt.ylim(1678,0)
		im=plt.imread('../final_img.png')
		implot=plt.imshow(im)
		plt.axis('off')
		plt.plot(coordinates[:,1],coordinates[:,0])
		plt.savefig("../IDWise/"+str(sys.argv[i]),ext='png',close=False,verbose=True,dpi=350,bbox_inches='tight',pad_inches=0)
		plt.close()
	# plt.show()
	# plt.savefig("./Multiple",ext='png',close=False,verbose=True,dpi=350,bbox_inches='tight',pad_inches=0)

if __name__ == '__main__':
	main()
