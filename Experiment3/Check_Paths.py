__author__='architsh'

from Plot_Ann_Arbor import plot_given_plot
import matplotlib.pyplot as plt
import sys

# Argument 1: The file containing the list of path names
# Argument 2: The location where all the paths are stored
# Argument 3: All the images are going to be stored

def main():
	plt.figure(0)
	plt.xlim(0,2416)
	plt.ylim(1678,0)
	im=plt.imread('../final_img.png')
	implot=plt.imshow(im)
	plt.axis('off')

	path_list=open(sys.argv[1],'r').read().splitlines()
	i=0
	# add '.txt' if needed
	for path in path_list:
		latlong=[[float(f) for f in line.split(',')[9:11]] for line in open(sys.argv[2]+path).read().splitlines()]
		
		# common plots for all the paths
		plt.figure(0)
		plot_given_plot(latlong,plt)
		
		# different plots for all the paths
		i=i+1
		plt.figure(i)
		plt.xlim(0,2416)
		plt.ylim(1678,0)
		im=plt.imread('../final_img.png')
		implot=plt.imshow(im)
		plt.axis('off')
		plot_given_plot(latlong,plt)
		plt.savefig(sys.argv[3]+str(i),ext='png',close=False,verbose=True,dpi=350,bbox_inches='tight',pad_inches=0)
	
	plt.figure(0)
	plt.savefig(sys.argv[3]+'all',ext='png',close=False,verbose=True,dpi=350,bbox_inches='tight',pad_inches=0)

if __name__ == '__main__':
	main()