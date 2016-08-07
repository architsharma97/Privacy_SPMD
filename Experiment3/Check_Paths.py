__author__='architsh'

from Plot_Ann_Arbor import plot_given_plot
import matplotlib.pyplot as plt

def main():
	plt.xlim(0,2416)
	plt.ylim(1678,0)
	im=plt.imread('../final_img.png')
	implot=plt.imshow(im)
	plt.axis('off')

	path_list=open('./PathAllocation/1_test.txt','r').read().splitlines()[:20]

	for path in path_list:
		latlong=[[float(f) for f in line.split(',')[9:11]] for line in open('../TestPaths/'+path+'.txt').read().splitlines()]
		plot_given_plot(latlong,plt)
	
	plt.savefig('intersection_check',ext='png',close=False,verbose=True,dpi=350,bbox_inches='tight',pad_inches=0)

if __name__ == '__main__':
	main()