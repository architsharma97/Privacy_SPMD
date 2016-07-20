__author__='architsh'

import sys
#Argument 1: Time Difference
#Argument 2: Maximum Distance
#Argument 3: Month of Data
#Argument 4: Year of Data
#Argument 5: Location of Original Data File
#Argument 6: Location of Path Segments

def main():
	start=open('./RouteTracing/start_data_'+sys.argv[3]+'_'+sys.argv[4]+'_'+sys.argv[1]+'_'+sys.argv[2]+'.txt','r').read().splitlines()
	end=open('./RouteTracing/end_data_'+sys.argv[3]+'_'+sys.argv[4]+'_'+sys.argv[1]+'_'+sys.argv[2]+'.txt','r').read().splitlines()

	line_count=0
	inc=1
	start_line=long(start[0].split(',')[10])
	end_line=long(end[0].split(',')[10])
	print 'Started File #1'
	file_open=open(sys.argv[6]+'/1.txt','a')

	with open(sys.argv[5],'r') as data_file:
		for line in data_file:
			
			line_count+=1
			entries=line.split()

			if line_count>end_line:
				inc+=1
				print 'New file started:' +str(inc)
				start_line=long(start[inc].split(',')[10])
				end_line=long(end[inc].split(',')[10])
				file_open=open(sys.argv[6]+'/'+str(inc)+'.txt','a')

			data_point=''
			for entry in entries[:len(entries)-1]:
				data_point+=entry+','
			data_point+=entries[len(entries)-1]
			file_open.write(str(inc)+','+data_point+'\n')

	print 'Total Files:' + str(inc)

if __name__ == '__main__':
	main()
