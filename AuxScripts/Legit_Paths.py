__author__='architsh'

#Argument #1: Location of path segments
#Argument #2: Minimum number of points after which the path segment is considered legitimate
#Argument #3: Total number of path segements in the folder for which location is passed
#Argument #4: Name of the file to which it should be written;File name example: legit_path_list_april_3000.txt
import sys
def main():
	#minimum number of points before which a path will be considered a legitimate path segment
	min_points=int(sys.argv[2])
	legit_files=[]
	for i in range(int(sys.argv[3]):
		path=open(sys.argv[1]+str(i+1)+'.txt','r').read().splitlines()
		if len(path)>=min_points:
			legit_files.append(i+1)
	
	print len(legit_files) 
	
	legit=open('../LegitPaths/'+sys.argv[4],'a')
	
	for i in legit_files:
		legit.write(str(i)+'\n')

if __name__ == '__main__':
	main()
