__author__='architsh'

directory='../IDWise/'

def main():
	car_id=-1
	with open('/scratch/user/architsh/Data/April9_2013.txt','r') as data_file:
		for line in data_file:
			entries=line.split()
			if car_id!=int(float(entries[0])):
				car_id=int(float(entries[0]))
				output=open(directory+str(int(float(entries[0])))+'.csv','a')
				output.write('time,latitude,longitude,speed\n')
			print car_id
			output.write(entries[3]+','+entries[7]+','+entries[8]+','+entries[10]+'\n')

if __name__ == '__main__':
	main()
