__author__='architsh'

#utility to plot on the ann harbor map
import matplotlib.pyplot as plt
import numpy as np
import sys

# supply a list containing elements which look like [latitude, longitude] along with the location they are going to be saved to
# if dont want to save and just show the plot, pass third parameter as True
def plot_on_map(latlong,location,show=False):
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

	latlong=np.array(latlong)
	coordinates=latlong-supp
	coordinates=coordinates.dot(dotmatrix)
	plt.plot(coordinates[:,1],coordinates[:,0])
	
	if not show:
		plt.savefig(location,ext='png',close=False,verbose=True,dpi=350,bbox_inches='tight',pad_inches=0)
		plt.close()
	else:
		plt.show()
		plt.close()

def plot_given_plot(latlong, plt):
	origin=np.array([42.22673, -83.83701])
	end=np.array([42.33316,-83.62981])
	supp=np.array([end[0],origin[1]])

	#linear mapping
	dotmatrix=np.array([(1678/(origin[0]-end[0]),0),(0,2416/(end[1]-origin[1]))])

	latlong=np.array(latlong)
	coordinates=latlong-supp
	coordinates=coordinates.dot(dotmatrix)
	plt.plot(coordinates[:,1],coordinates[:,0])
