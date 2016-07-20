__author__='architsh'

def main():
	max_lat=-10000.000
	min_lat=10000.000
	max_long=-10000.000
	min_long=10000.000
	with open('/scratch/user/architsh/Data/April9_2013.txt','r') as data_file:
		for line in data_file:
			entries=line.split()
			latitude=float(entries[7])
			longitude=float(entries[8])
			if latitude < min_lat and latitude > 35.0:
				min_lat=latitude
				print "Min Lat: " + str(latitude)
			
			if latitude > max_lat :
				max_lat=latitude
				print "Max Lat: " + str(latitude)

			if longitude < min_long :
				min_long=longitude
				print "Min Long: " + str(longitude)
			
			if longitude > max_long :
				max_long=longitude
				print "Max Long" + str(longitude)
	
	print min_lat, max_lat, min_long, max_long
	#40.939522 43.193489 -87.32235 -82.476669

if __name__ == '__main__':
	main()
