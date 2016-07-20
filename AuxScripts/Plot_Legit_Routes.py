__author__='architsh'

from Plot_Ann_Harbor import plot_given_plot
import matplotlib.pyplot as plt
import sys

#pass the number of legit routes that need to be plotted onto the map of Ann Harbor
 
def main():
	#resolution of picture: replace parameters accordingly
	plt.xlim(0,2416)
	plt.ylim(1678,0)
	im=plt.imread('../final_img.png')
	implot=plt.imshow(im)
	plt.axis('off')

	legit_routes=open('../LegitPaths/legitimate_path_list_3000.txt','r').read().splitlines()
	
	for i in range(int(sys.argv[1])):	
		latlong=[]
		path=open('/scratch/user/architsh/PathSegments/'+legit_routes[i]+'.txt','r').read().splitlines()
		for line in path:
			latlong.append([float(entry) for entry in line.split(',')[8:10]])
		plot_given_plot(latlong,plt)
	plt.show()
	
if __name__ == '__main__':
	main()
