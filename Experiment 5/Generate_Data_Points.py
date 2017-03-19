__author__='Reza'

#Argument 1: Number of path segments
#Argument 2: Directory where the path segments are stored
#Argument 3: Directory where the new data will be written
###-Not Needed-->Argument 4: Time in seconds after which every path segment will be broken

import sys
from random import randint

def main():
    
    path_list=open('./paths_'+sys.argv[1]+'.txt','r').read().splitlines()
    
    data_points=open(sys.argv[3]+'data_points_'+sys.argv[1]+'.txt','a')
    
    path_count=0
    data_points_count=0
    
    for path_name in path_list:
        
        path_count+=1
        # print 'Found a path'
        path_info=open(sys.argv[2]+path_name+'.txt','r').read().splitlines()
        
        #a random start time is chosen from an interval of 5 minutes
        time_start=float(path_info[0].split(',')[5])/1000000-35-randint(0,3000)/10


        flag=True
        
        for line in path_info:
            entries=line.split(',')
            
            if flag:
                entries[5]=str(float(entries[5])/1000000-35-time_start)
                print entries[5]
                new_line=''
                for i in range(len(entries)):
                    if i==len(entries)-1:
                        new_line+=entries[i]
                        break
                    new_line+=entries[i]+','

                data_points.write(new_line+'\n')
                data_points_count+=1

    print 'Number of paths used: ' +str(path_count)
    print 'Number of data points: ' +str(data_points_count)

if __name__ == '__main__':
    main()
