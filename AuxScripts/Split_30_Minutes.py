__author__='architsh'

import math

directory='../TrafficFlow'

def main():
	for i in range(1,49):
	 	output=open(directory+'/'+ str(i) +'.csv','w')
	 	output.write('latitude,longitude\n')
	 	print "File started: " + str(i) + ".csv\n" 
	
	time = 292550400.00
	with open('/scratch/user/architsh/Data/April9_2013.txt','r') as data_file:
		for line in data_file:
			entries=line.split()
			file_count=math.floor((float(entries[3])-time)/1800) + 1
			print file_count
			output=open(directory+'/'+ str(int(file_count)) +'.csv','a')
			output.write(entries[7]+','+entries[8]+'\n')
	
if __name__== '__main__':
	main()
			
