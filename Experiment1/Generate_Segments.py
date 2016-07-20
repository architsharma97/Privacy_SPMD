__author__='architsh'

import sys
from random import shuffle, randint
#Argument 1: Number of paths
#Argument 2: Directory where paths exist

#script preserves a bare minimum number of points in all broken segments (500) and takes the start and end of all segments to appropriate files 
def main():
	pathset=open('./paths_'+sys.argv[1]+'.txt','r').read().splitlines()
	start_data=open('./start_data_'+sys.argv[1]+'.txt','a')
	end_data=open('./end_data_'+sys.argv[1]+'.txt','a')
	count=1
	for path in pathset:
		print count
		count+=1
		path_file=open(sys.argv[2]+'/'+path+'.txt','r').read().splitlines()
		present_line=1
		while present_line<=len(path_file):
			start_data.write(path_file[present_line-1]+'\n')
			end_line=randint(present_line+499,len(path_file))
			if len(path_file)-end_line<500:
				end_line=len(path_file)
			end_data.write(path_file[end_line-1]+'\n')
			present_line=end_line+1

if __name__ == '__main__':
	main()