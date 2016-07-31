__author__='architsh'

import sys
from random import shuffle
from geopy.distance import vincenty

#Argument 1: Start data
#Argument 2: End data
#Argument 3: Number of original segments
#Argument 4: Time in seconds after which segments are cut

segments=[]
break_indices=[0]

#constructs the graph
def search(idx):
	global segments, break_indices
	
	required_time=segments[idx].endTime+0.1
	
	start_idx=break_indices[int(required_time/int(sys.argv[4]))]
	end_idx=break_indices[int(required_time/int(sys.argv[4]))+1]

	for i in range(start_idx, end_idx+1):
		if abs(segments[idx].endTime-segments[i].startTime)<=1 and vincenty((segments[i].startLat,segments[i].startLong),(segments[idx].endLat,segments[idx].endLong)).m<=20:
			print 'Found for '+str(idx)
			segments[idx].next.append(i)
			segments[i].prev.append(idx)
			segments[i].start=False
			segments[idx].finish=False

class path_segment(object):
	def __init__(self,start,end):
		self.start=start.split(',')
		self.end=end.split(',')

		self.startLat=float(self.start[9])
		self.endLat=float(self.end[9])
		self.startLong=float(self.start[10])
		self.endLong=float(self.end[10])
		self.startTime=float(self.start[5])
		self.endTime=float(self.end[5])
		self.startSpeed=float(self.start[11])
		self.startHeading=float(self.start[12])
		self.endSpeed=float(self.end[11])
		self.endHeading=float(self.end[12])
		self.process=int(self.start[0])
		self.id=int(self.start[1])
		self.startMessage=int(self.start[7])
		self.endMessage=int(self.end[7])

		self.begin=True
		self.finish=True

		self.next=[]
		self.prev=[]

def main():
	global segments, break_indices
	start_data=open(sys.argv[1],'r').read().splitlines()
	end_data=open(sys.argv[2],'r').read().splitlines()

	for i in range(len(start_data)):
		segments.append(path_segment(start_data[i],end_data[i]))
		# print segments[i].startTime, segments[i].endTime

	#start algorithm after shuffling
	shuffle(segments)

	segments.sort(key=lambda x: x.startTime)

	break_time=int(sys.argv[4])

	for i in range(len(segments)):
		while segments[i].startTime > break_time:
			# print segments[i].startTime, break_time
			break_time+=int(sys.argv[4])
			break_indices.append(i)
	break_indices.append(len(segments)-1)
	
	print len(segments)
	print break_indices

	for i in range(len(segments)):
		search(i)

	correct_joins=0
	not_joined=0
	false_joins=0
	sum_choices=0
	for i in range(len(segments)):
		flag=False
		sum_choices+=len(segments[i].next)
		for nxt in segments[i].next:
			if segments[nxt].process==segments[i].process and segments[nxt].id==segments[i].id and (segments[i].endMessage+1)%128==segments[nxt].startMessage:
				flag=True

		if len(segments[i].next)==0:
			not_joined+=1
		elif flag:
			correct_joins+=1
		else:
			false_joins+=1
	print 'Average choice: '+str(float(sum_choices)/len(segments))
	print 'Correct joins: '+str(correct_joins)
	print 'False joins: '+str(false_joins)
	print 'Not joined: '+str(not_joined)

if __name__ == '__main__':
	main()