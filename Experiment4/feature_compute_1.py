__author__='architsh'

import sys

# Argument 1: Name of the path (without the A,B)
# Argument 2: Relative path to the folder (or the absolute)

def main():
 	file_A=open(sys.argv[2]+sys.argv[1]+'_A'+'.txt','r').read().splitlines()
 	file_B=open(sys.argv[2]+sys.argv[1]+'_B'+'.txt','r').read().splitlines()

 	# features to be computed
 	num_entries=len(file_A)
 	mean_speed_A=0
 	# along the motion
 	mean_accx_A=0
 	# perpendicular to the motion
 	mean_accy_A=0
 	mean_heading_A=0

 	# these paramaeters are computed for proximity to intersection (giving more importance to behaviour near intersection)
 	# how much time near intersection in section
 	time_near_A=60
 	time_end=float(file_A[num_entries-1].split(',')[5])/1000000-35

 	ni_mean_speed_A=0
 	ni_mean_accx_A=0
 	ni_mean_accy_A=0
 	ni_mean_heading_A=0
 	ni_entries=0

 	for entry in file_A:
 		entries=entry.split(',')
 		mean_speed_A+=float(entries[12])
 		mean_heading_A+=float(entries[13])
 		mean_accx_A+=float(entries[14])
 		mean_accy_A+=float(entries[15])
 		if abs(int(entries[5])/1000000-35-time_end)<=60:
 			ni_entries+=1
 			ni_mean_speed_A+=float(entries[12])
	 		ni_mean_heading_A+=float(entries[13])
	 		ni_mean_accx_A+=float(entries[14])
	 		ni_mean_accy_A+=float(entries[15])

	mean_speed_A/=num_entries
	mean_heading_A/=num_entries
	mean_accx_A/=num_entries
	mean_accy_A/=num_entries

	ni_mean_speed_A/=ni_entries
	ni_mean_heading_A/=ni_entries
	ni_mean_accx_A/=ni_entries
	ni_mean_accy_A/=ni_entries

	# computation of standard deviation
	std_speed_A=0
	std_heading_A=0
	std_accx_A=0
	std_accy_A=0

	# near intersection characteristics
	ni_std_speed_A=0
	ni_std_heading_A=0
	ni_std_accx_A=0
	ni_std_accy_A=0	

	for entry in file_A:
 		entries=entry.split(',')
 		std_speed_A+=(mean_speed_A-float(entries[12]))**2
 		std_heading_A+=(mean_heading_A-float(entries[13]))**2
 		std_accx_A+=(mean_accx_A-float(entries[14]))**2
 		std_accy_A+=(mean_accy_A-float(entries[15]))**2
 		if abs(int(entries[5])/1000000-35-time_end)<=60:
 			ni_std_speed_A+=(ni_mean_speed_A-float(entries[12]))**2
	 		ni_std_heading_A+=(ni_mean_heading_A-float(entries[13]))**2
	 		ni_std_accx_A+=(ni_mean_accx_A-float(entries[14]))**2
	 		ni_std_accy_A+=(ni_mean_accy_A-float(entries[15]))**2

	std_speed_A**=0.5
	std_heading_A**=0.5
	std_accx_A**=0.5
	std_accy_A**=0.5
	std_speed_A/=num_entries
	std_heading_A/=num_entries
	std_accx_A/=num_entries
	std_accy_A/=num_entries


	ni_std_speed_A**=0.5
	ni_std_heading_A**=0.5
	ni_std_accx_A**=0.5
	ni_std_accy_A**=0.5
	ni_std_speed_A/=ni_entries
	ni_std_heading_A/=ni_entries
	ni_std_accx_A/=ni_entries
	ni_std_accy_A/=ni_entries

	print "File A"
	print "Means"
	print "Mean speed: %f, Mean heading: %f" %(mean_speed_A, mean_heading_A)
	print "Mean acceleration in longitudinal direction: %f" %(mean_accx_A)
	print "Mean acceleration in lateral direction: %f" %(mean_accy_A)
	print "Standard Deviations"
	print "Standard Deviation of  speed: %f, Standard deviation of heading: %f" %(std_speed_A, std_heading_A)
	print "Standard deviation of acceleration in longitudinal direction: %f" %(std_accx_A)
	print "Standard deviation of acceleration in lateral direction: %f" %(std_accy_A)
	
	print "Same parameters near intersection under 1 minute"
	print "Means"
	print "Mean speed: %f, Mean heading: %f" %(ni_mean_speed_A, ni_mean_heading_A)
	print "Mean acceleration in longitudinal direction: %f" %(ni_mean_accx_A)
	print "Mean acceleration in lateral direction: %f" %(ni_mean_accy_A)
	print "Standard Deviations"
	print "Standard Deviation of  speed: %f, Standard deviation of heading: %f" %(ni_std_speed_A, ni_std_heading_A)
	print "Standard deviation of acceleration in longitudinal direction: %f" %(ni_std_accx_A)
	print "Standard deviation of acceleration in lateral direction: %f" %(ni_std_accy_A)

	# FILE B commences here
	# features to be computed
 	num_entries=len(file_B)
 	# print num_entries
 	mean_speed_B=0
 	# along the motion
 	mean_accx_B=0
 	# perpendicular to the motion
 	mean_accy_B=0
 	mean_heading_B=0

 	# these paramaeters are computed for proximity to intersection (giving more importance to behaviour near intersection)
 	# how much time near intersection in section
 	time_near_B=60
 	time_start=float(file_B[0].split(',')[5])/1000000-35

 	ni_mean_speed_B=0
 	ni_mean_accx_B=0
 	ni_mean_accy_B=0
 	ni_mean_heading_B=0
 	ni_entries=0

 	for entry in file_B:
 		entries=entry.split(',')
 		if len(entries)==0:
 			break
 		mean_speed_B+=float(entries[12])
 		mean_heading_B+=float(entries[13])
 		mean_accx_B+=float(entries[14])
 		mean_accy_B+=float(entries[15])
 		if abs(int(entries[5])/1000000-35-time_start)<=60:
 			ni_entries+=1
 			ni_mean_speed_B+=float(entries[12])
	 		ni_mean_heading_B+=float(entries[13])
	 		ni_mean_accx_B+=float(entries[14])
	 		ni_mean_accy_B+=float(entries[15])

	mean_speed_B/=num_entries
	mean_heading_B/=num_entries
	mean_accx_B/=num_entries
	mean_accy_B/=num_entries

	ni_mean_speed_B/=ni_entries
	ni_mean_heading_B/=ni_entries
	ni_mean_accx_B/=ni_entries
	ni_mean_accy_B/=ni_entries

	# computation of standard deviation
	std_speed_B=0
	std_heading_B=0
	std_accx_B=0
	std_accy_B=0

	# near intersection characteristics
	ni_std_speed_B=0
	ni_std_heading_B=0
	ni_std_accx_B=0
	ni_std_accy_B=0	

	for entry in file_B:
 		entries=entry.split(',')
 		if len(entries)==0:
 			break
 		std_speed_B+=(mean_speed_B-float(entries[12]))**2
 		std_heading_B+=(mean_heading_B-float(entries[13]))**2
 		std_accx_B+=(mean_accx_B-float(entries[14]))**2
 		std_accy_B+=(mean_accy_B-float(entries[15]))**2
 		if abs(int(entries[5])/1000000-35-time_start)<=60:
 			ni_std_speed_B+=(ni_mean_speed_B-float(entries[12]))**2
	 		ni_std_heading_B+=(ni_mean_heading_B-float(entries[13]))**2
	 		ni_std_accx_B+=(ni_mean_accx_B-float(entries[14]))**2
	 		ni_std_accy_B+=(ni_mean_accy_B-float(entries[15]))**2

	std_speed_B**=0.5
	std_heading_B**=0.5
	std_accx_B**=0.5
	std_accy_B**=0.5
	std_speed_B/=num_entries
	std_heading_B/=num_entries
	std_accx_B/=num_entries
	std_accy_B/=num_entries

	ni_std_speed_B**=0.5
	ni_std_heading_B**=0.5
	ni_std_accx_B**=0.5
	ni_std_accy_B**=0.5
	ni_std_speed_B/=ni_entries
	ni_std_heading_B/=ni_entries
	ni_std_accx_B/=ni_entries
	ni_std_accy_B/=ni_entries

	print "File B"
	print "Means"
	print "Mean speed: %f, Mean heading: %f" %(mean_speed_B, mean_heading_B)
	print "Mean acceleration in longitudinal direction: %f" %(mean_accx_B)
	print "Mean acceleration in lateral direction: %f" %(mean_accy_B)
	print "Standard Deviations"
	print "Standard Deviation of  speed: %f, Standard deviation of heading: %f" %(std_speed_B, std_heading_B)
	print "Standard deviation of acceleration in longitudinal direction: %f" %(std_accx_B)
	print "Standard deviation of acceleration in lateral direction: %f" %(std_accy_B)
	
	print "Same parameters near intersection under 1 minute"
	print "Means"
	print "Mean speed: %f, Mean heading: %f" %(ni_mean_speed_B, ni_mean_heading_B)
	print "Mean acceleration in longitudinal direction: %f" %(ni_mean_accx_B)
	print "Mean acceleration in lateral direction: %f" %(ni_mean_accy_B)
	print "Standard Deviations"
	print "Standard Deviation of  speed: %f, Standard deviation of heading: %f" %(ni_std_speed_B, ni_std_heading_B)
	print "Standard deviation of acceleration in longitudinal direction: %f" %(ni_std_accx_B)
	print "Standard deviation of acceleration in lateral direction: %f" %(ni_std_accy_B)

if __name__ == '__main__':
 	main()