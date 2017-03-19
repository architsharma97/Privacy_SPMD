__author__= 'architsh'

#a script to generate random list of segments from (user passed) amount of ground truth paths.
#TO BE USED WITH CITY PATHS

#Argument 1: Number of paths to be broken down.
#Argument 2: File containing information about number of files from each process
#Argument 3: Directory where are all new files will be made
#Argument 4: Directory which contains city path's information

from random import randint,shuffle
import sys

#number of processes used (Dont change if you do not what you are doing)
PROCESSES=20

def main():
    global PROCESSES
    
    #to use all the processes, comment the next line and uncomment the next one
    process_list=[num for num in range(10,13)]
    # process_list=[num for num in range(1,PROCESSES+1)]
    shuffle(process_list)
    
    total_paths=int(sys.argv[1])
    
    paths_to_be_used=open(sys.argv[3]+'/paths_'+str(total_paths)+'.txt','a')

    temp=[info.split() for info in open(sys.argv[2],'r').read().splitlines()[:PROCESSES]]    
    
    #print temp
    paths_per_process=[0 for i in range(len(temp))]

    for i in range(len(paths_per_process)):
        #print temp[i][1][:-4]
        paths_per_process[int(temp[i][1][:-4])-1]=int(temp[i][0])

    for i in process_list:
        if not total_paths:
            break

        if i==process_list[len(process_list)-1]:
            rand=total_paths
        else:
            rand=randint(1,min(total_paths, paths_per_process[i-1]))
        
        city_path_list=open(sys.argv[4]+str(i)+'.txt').read().splitlines()
        total_paths-=rand
        shuffle(city_path_list)

        for path_num in range(rand):
            paths_to_be_used.write(city_path_list[path_num]+'\n')

if __name__ == '__main__':
    main()