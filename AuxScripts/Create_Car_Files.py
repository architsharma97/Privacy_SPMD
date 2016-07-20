__author__='architsh'

#Pretty stupid idea
directory='./RouteTracing/CarRoutes/'

def main():
	files_guide=open('../RouteTracing/final.txt','r').read().splitlines()
	inc=1
	line_count=0
	entries=files_guide[inc].split(',')
	start_line=int(entries[0])
	end_line=int(entries[1])
	with open('/scratch/user/architsh/Data/April9_2013.txt','r') as data_file:
		for line in data_file:
			line_count+=1
			if line_count>end_line:
				inc+=1
				entries=files_guide[inc].split(',')
				start_line=int(entries[0])
				end_line=int(entries[1])
			
			line_entries=line.split()

			for i in range(2,len(entries)):
				open_file=open(directory+entries[i]+'.txt','a')
				# ID, time, latitude, longitude, speed
				open_file.write(line_entries[0]+','+line_entries[3]+','+line_entries[7]+','+line_entries[8]+','+line_entries[10]+'\n')
				open_file.close()

if __name__ == '__main__':
	main()
