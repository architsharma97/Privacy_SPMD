__author__='architsh'

import sys
from './AuxScripts/Plot_Ann_Arbor' import plot_on_map, plot_given_plot
import matplotlib.pyplot as plt
import numpy as np

class vertex(object):
	def __init__(self, info):
		self.idx=int(info[0])
		if int(info[1])==1:
			self.end=False
			self.outgoing=[int(i) for i in info[3].split(',')]
		else:
			self.end=True
			self.outgoing=[]

		if int(info[2])==1:
			self.start=False
			self.incoming=[int(i) for i in info[4].split(',')]
		else:
			self.start=True
			self.incoming=[]
	
	def lat_long(self):
		latlong=[]
		with open('./PathSegments/'+str(self.idx+1)+'.txt') as data_file:
			for line in data_file:
				latlong.append([float(f) for f in line.split(',')[8:10]])
		
		return latlong

	def plot_path_show(self):
		plot_on_map(self.lat_long(),'',True)
		print len(self.lat_long())

	def plot_path_save(self,location):
		plot_on_map(self.lat_long(),location)


def main():
	graph=open('./RouteTracing/graph_30_500.txt','r').read().splitlines()
	# graph=open('./RouteTracing/graph.txt','r').read().splitlines()
	
	vertices=[vertex(node.split(';')) for node in graph]
	print 'Loaded Vertices'
	
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
	
	idx=int(sys.argv[1])

	latlong=vertices[idx].lat_long()
	print len(latlong)
	latlong=np.array(latlong)
	coordinates=latlong-supp
	coordinates=coordinates.dot(dotmatrix)
	plt.plot(coordinates[:,1],coordinates[:,0])

	print len(vertices[idx].outgoing), vertices[idx].outgoing
	
	for idx_1 in vertices[idx].outgoing:

		latlong=vertices[idx_1].lat_long()

		print len(latlong)
		latlong=np.array(latlong)
		coordinates=latlong-supp
		coordinates=coordinates.dot(dotmatrix)
		plt.plot(coordinates[:,1],coordinates[:,0])
		
		print len(vertices[idx_1].outgoing), vertices[idx_1].outgoing
		
		for idx_2 in vertices[idx_1].outgoing:
			latlong=vertices[idx_2].lat_long()
			
			print len(latlong)
			latlong=np.array(latlong)
			coordinates=latlong-supp
			coordinates=coordinates.dot(dotmatrix)
			plt.plot(coordinates[:,1],coordinates[:,0])
	
	plt.show()		

if __name__ == '__main__':
	main()
