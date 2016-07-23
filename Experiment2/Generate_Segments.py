__author__='architsh'

#Argument 1: Number of path segments
#Argument 2: Directory where the path segments are stored
#Argument 3: Directory where the new data will be written
#Argument 4: Time in seconds after which every path segment will be broken

import sys
from random import randint

def main():
	path_list=open('./paths_'+sys.argv[1]+'.txt','r').read().splitlines()
	
	start_data=open(sys.argv[3]+'start_'+sys.argv[1]+'.txt','a')
	end_data=open(sys.argv[3]+'end_'+sys.argv[1]+'.txt','a')
	
	for path_name in path_list:
		path_info=open(sys.argv[2]+path_name+'.txt','r').read().splitlines()
		
		#a random start time is chosen from an interval of 5 minutes
		time_start=float(path_info[0].split(',')[5])/1000000-35-randint(0,3000)/10
		time_break=int(sys.argv[4])

		flag=True
		
		for line in path_info:
			entries=line.split(',')
			
			if flag:
				entries[5]=str(float(entries[5])/1000000-35-time_start)
				new_line=''
				for i in len(entries):
					if i==len(entries)-1:
						new_line+=entries[i]
						break
					new_line+=entries[i]+','

				start_data.write(new_line+'\n')
				flag=False

			else if float(entries[5])/1000000-35-time_start>=time_break:
				time_break+=int(sys.argv[4])
				flag=True
				
				entries[5]=str(float(entries[5])/1000000-35-time_start)
				new_line=''
				for i in len(entries):
					if i==len(entries)-1:
						new_line+=entries[i]
						break
					
					new_line+=entries[i]+','
				end_data.write(new_line+'\n')	

if __name__ == '__main__':
	main()