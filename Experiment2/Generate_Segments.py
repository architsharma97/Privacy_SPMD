__author__='architsh'

#Argument 1: Number of path segments
#Argument 2: Directory where the path segments are stored
#Argument 3: Directory where the new data will be written
#Argument 4: Time in seconds after which every path segment will be broken

import sys
from random import randint

def main():
	path_list=open('./paths_'+sys.argv[1]+'.txt','r').read().splitlines()
	
	start_data=open(sys.argv[3]+'test_start_'+sys.argv[1]+'.txt','a')
	end_data=open(sys.argv[3]+'test_end_'+sys.argv[1]+'.txt','a')
	
	path_count=0
	start_count=0
	end_count=0
	
	for path_name in path_list:
		#comment the next few lines for the whole thing to function for the complete set of paths
		if not (path_name[:2]==str(10) or path_name[:2]==str(11) or path_name[:2]==str(12)):
			continue
		
		path_count+=1
		# print 'Found a path'
		path_info=open(sys.argv[2]+path_name+'.txt','r').read().splitlines()
		
		#a random start time is chosen from an interval of 5 minutes
		time_start=float(path_info[0].split(',')[5])/1000000-35-randint(0,3000)/10
		time_break=int(sys.argv[4])
		print 'Break time: ' +str(time_break)

		flag=True
		
		for line in path_info:
			entries=line.split(',')
			
			if flag and line==path_info[len(path_info)-1]:
				print 'Last line was skipped as a start of new path'
				continue
			
			if flag:
				entries[5]=str(float(entries[5])/1000000-35-time_start)
				print entries[5]
				new_line=''
				for i in range(len(entries)):
					if i==len(entries)-1:
						new_line+=entries[i]
						break
					new_line+=entries[i]+','

				start_data.write(new_line+'\n')
				start_count+=1
				flag=False

			elif float(entries[5])/1000000-35-time_start>=time_break:
				time_break+=int(sys.argv[4])
				flag=True
				
				entries[5]=str(float(entries[5])/1000000-35-time_start)
				print entries[5]
				print 'Break time: ' +str(time_break)

				new_line=''
				
				for i in range(len(entries)):
					if i==len(entries)-1:
						new_line+=entries[i]
						break
					new_line+=entries[i]+','

				end_data.write(new_line+'\n')
				end_count+=1

			elif line==path_info[len(path_info)-1]:
				print 'Last line'
				flag=True
				
				entries[5]=str(float(entries[5])/1000000-35-time_start)
				print entries[5]
				
				new_line=''
				
				for i in range(len(entries)):
					if i==len(entries)-1:
						new_line+=entries[i]
						break
					new_line+=entries[i]+','

				end_data.write(new_line+'\n')				
				end_count+=1

	print 'Number of paths used: ' +str(path_count)
	print 'Start: ' +str(start_count)
	print 'End: ' +str(end_count)

if __name__ == '__main__':
	main()