__author__= 'architsh'

#SCRIPT NEEDED: MODIFY
#Argument #1:Location of the CSV file
#Argument #2: Time Difference
#Argument #3: Maximum distance
#Argument #4: Month of data
#argument #5: Year of data

from geopy.distance import vincenty
import sys

#First attempt at retracing the route of the car from the dataset. IDs are present but switch at some predefined rate.
def main():
	flag=True

	#each item will be [id,time,latitude,longitude,speed,line # in original file]
	start,end,aux=[],[],[]
	
	#ID, gentime (integer), time since ignition is on, latitude, longitude, speed, heading, Ax, Ay, Az	
	idxs=[0,3,6,7,8,10,11,12,13,14]
	integers=[0,3,6]
	floats=[7,8,10,11,12,13,14]
	count=0
	
	#seconds after which the trips would be considered distinct for the same ID
	time_diff=int(sys.argv[2])
	#metres after which the trips would be considered distinct for the same ID
	min_dist=int(sys.argv[3])

	#this block gets the start and the end entries of all the trips into distinct lists
	#most print statements are to check whether trips are split appropriately
	with open(sys.argv[1],'r') as data_file:
		for line in data_file:
			count+=1
			if flag:
				flag=False
				entries=line.split(',')
				for i in integers:
					#Converting Gentime to Epoch time
					if i==3:
						aux.append(float(entries[i])/1000000-35+1072933200)
					else:
						aux.append(int(entries[i]))
				for i in floats:
					aux.append(float(entries[i]))
			
				aux.append(count)
				start.append(aux)
				
				print 'Start'
				print start[len(start)-1]
			else:
				entries=line.split(',')
				dist=vincenty((aux[3],aux[4]),(float(entries[7]),float(entries[8]))).km*1000
				
				#condition under which the tag would be considered as part of the same trip
				if int(entries[0])==aux[0] and abs(float(entries[3])/1000000-35+1072933200-aux[1])<=time_diff and dist<=min_dist:
					aux=[]
					for i in integers:
						#Converting Gentime to Epoch time
						if i==3:
							aux.append(float(entries[i])/1000000-35+1072933200)
						else:
							aux.append(int(entries[i]))
					for i in floats:
						aux.append(float(entries[i]))
					aux.append(count)
				else:
					end.append(aux)
					aux=[]
					
					for i in integers:
						#Converting Gentime to Epoch time
						if i==3:
							aux.append(float(entries[i])/1000000-35+1072933200)
						else:
							aux.append(int(entries[i]))
					for i in floats:
						aux.append(float(entries[i]))
					aux.append(count)
					start.append(aux)
					
					print 'End'
					print end[len(end)-1]
					
					#to print the distance between the end point of previous trip and the start point of the next trip
					print dist
					print 'Start'
					print start[len(start)-1]
		
		end.append(aux)
		print 'Lengths of arrays: ',
		print len(start),len(end)
	
	print 'Writing Start Files'
	start_file=open('./RouteTracing/start_data_'+sys.argv[4]+'_'+sys.argv[5]+'_'+sys.argv[2]+'_'+sys.argv[3]+'.txt','a')
	for element in start:
		for entry in element[:len(element)-1]:
			start_file.write(str(entry)+',')
		start_file.write(str(element[len(element)-1])+'\n')
	print 'Start files written'
	
	print 'Writing End Files'
	end_file=open('./RouteTracing/end_data_'+sys.argv[4]+'_'+sys.argv[5]+'_'+sys.argv[2]+'_'+sys.argv[3]+'.txt','a')
	for element in end:
		for entry in element[:len(element)-1]:
			end_file.write(str(entry)+',')
		end_file.write(str(element[len(element)-1])+'\n')
	print 'End Files Written'
	
	start_file.close()
	end_file.close()

if __name__ == '__main__':
	main()
