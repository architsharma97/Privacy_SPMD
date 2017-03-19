__author__='Reza'

import sys
from random import shuffle
from geopy.distance import vincenty

#Argument 1: Data Points

points=[]

#constructs the graph
def search(idx):
    global points
    
    for i in range(idx+1,len(points)):
        if points[i].startTime-points[idx].startTime>1:
            end_idx=i
            break
        else:
            end_idx=i
    
    start_idx=idx+1

    for i in range(start_idx, end_idx+1):
        if abs(points[i].startTime-points[idx].startTime)<=1 and vincenty((points[i].startLat,points[i].startLong),(points[idx].startLat,points[idx].startLong)).m<=(point[idx].startSpeed*0.2) and abs(points[i].startHeading-points[idx].startHeading) <=5:
            points[idx].next.append(i)
            points[i].begin=False
            points[idx].finish=False
            

class path_segment(object):
    def __init__(self,start):
        self.start=start.split(',')

        self.startLat=float(self.start[9])
        self.startLong=float(self.start[10])
        self.startTime=float(self.start[5])
        self.startSpeed=float(self.start[11])
        self.startHeading=float(self.start[12])
        self.process=int(self.start[0])
        self.id=int(self.start[1])
        self.startTxDevice=int(self.start[4])

        self.begin=True
        self.finish=True

        self.next=[]
        self.prev=[]

def main():
    global points
    data_points=open(sys.argv[1],'r').read().splitlines()

    for i in range(len(data_points)):
        points.append(path_segment(data_points[i]))

    #start algorithm after shuffling
    shuffle(points)

    points.sort(key=lambda x: x.startTime)
    
    print len(points)

    for i in range(len(points)):
        search(i)
        next_id=-1
        min_score=1000000000000
        if len(points[i].next):
            for nxt in points[i].next:
                #the best fit choice should be 0.1 second apart, speed*0.1 metre away, similar speed and heading. All other points should be penalized
                #RMS error is being used to penalize, which is scaled appropriately to make it dimensionless
                score=(vincenty((points[nxt].startLat,points[nxt].startLong),(points[i].startLat,points[i].startLong)).m/(point[i].startSpeed*0.1))**2
                score+=((points[nxt].startTime-points[i].strartTime)/0.1)**2
                score+=((points[nxt].startHeading-points[i].startHeading)/(points[i].startHeading))**2
                score+=((points[nxt].startSpeed-points[i].startSpeed)/(points[i].startSpeed))**2
                
                if score < min_score:
                    min_score=score
                    next_id=nxt
        
        points[i].next=next_id
        points[next_id].prev=i

    correct_joins=0
    not_joined=0
    false_joins=0
    sum_choices=0
    # for i in range(len(points)):
    #     flag=False
    #     sum_choices+=len(points[i].next)
    #     for nxt in points[i].next:
    #         if points[nxt].process==points[i].process and points[nxt].id==points[i].id and (points[i].startTxDevice+1)%128==points[nxt].startTxDevice:
    #             flag=True

    #     if len(points[i].next)==0:
    #         not_joined+=1
    #     elif flag:
    #         correct_joins+=1
    #     else:
    #         false_joins+=1

    for i in range(len(points)):
        if points[i].next!=-1:
            if points[i].process==points[points[i].next].process and points[i].id==points[points[i].next].id and (points[i].startTxDevice+1)%128==points[points[i].next].startTxDevice:
                correct_joins+=1
            else:
                false_joins+=1
        else:
            not_joined+=1
    # print 'Average choice: '+str(float(sum_choices)/len(points))
    print 'Correct joins: '+str(correct_joins)
    print 'False joins: '+str(false_joins)
    print 'Not joined: '+str(not_joined)
    print 'Success rate: '+str(100.0-(float(false_joins)/len(points))*100)+'%'

if __name__ == '__main__':
    main()
