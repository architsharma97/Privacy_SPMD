__author__='architsh'

import sys
from geopy.distance import vincenty

#Argument 1: Start Data
#Argument 2: End data
#Argument 3: Number of path segments
segments=[]
total_edges=0

#pass the idx of the segment for which the next segment is supposed 
def search(idx):
	global segments, total_edges
	lo,hi=0,len(segments)-1
	mid=(lo+hi)/2
	
	#the next segment might not be precisely at 0.1 segment of the next one
	required_time=segments[idx].endTime+0.0988
	
	while (not (segments[mid].startTime-required_time>=-0.02 and segments[mid].startTime-required_time<=0.01)) and hi>lo:
		# print 'I am here!'
		if segments[mid].startTime > required_time:
			hi=mid-1
		else:
			lo=mid+1
		mid=(hi+lo)/2

	print 'Required time: '+str(required_time)+ ' Time found: ' + str(segments[mid].startTime)
	# print vincenty((segments[idx].endLat,segments[idx].endLong),(segments[mid].startLat,segments[mid].startLong)).m
	
	flag=False
	check=mid
	while check<len(segments) and abs(segments[check].startTime-required_time)<=5:
		if vincenty((segments[idx].endLat,segments[idx].endLong),(segments[check].startLat,segments[check].startLong)).m<=10:
			flag=True
			total_edges+=1
			segments[idx].next.append(check)
			segments[check].prev.append(idx)
			segments[check].begin=False
		check+=1

	if flag:
		# print check
		return segments[idx].next[0]
	else:
		# print -1
		return -1

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

		self.begin=True
		self.finish=True

		self.next=[]
		self.prev=[]

def main():
	global segments, total_edges
	
	start_data=open(sys.argv[1],'r').read().splitlines()
	end_data=open(sys.argv[2],'r').read().splitlines()
	print len(start_data), len(end_data)

	for i in range(len(start_data)):
		segments.append(path_segment(start_data[i],end_data[i]))

	print 'Segments created: ' + str(len(start_data))
	
	# to ensure reconstuction algorithm does not operate on any ordering bias
	shuffle(segments)

	segments.sort(key=lambda x:x.startTime)
	print 'Segments sorted'

	for i in range(len(segments)):
		idx_found=search(i)
		# segments[i].next=idx_found 
		if idx_found !=-1:
			segments[i].finish=False
			# segments[idx_found].prev=i
			# segments[idx_found].begin=False

	count_begin=0
	count_finish=0

	for i in range(len(segments)):
		if segments[i].begin:
			count_begin+=1
		if segments[i].finish:
			count_finish+=1

	avg_choices_next=0
	avg_choices_prev=0
	for i in range(len(segments)):
		avg_choices_next+=len(segments[i].next)
		avg_choices_prev+=len(segments[i].prev)

	print 'Number of distinct begins: '+str(count_begin)
	print 'Number of distinct finishes '+str(count_finish)

	correct_joins=0
	
	# if the file number does not match
	false_joins_1=0
	#if the file number matches, however, the the connection is wrong
	false_joins_2=0
	
	not_joined=0

	for i in range(len(segments)):
		if not len(segments[i].next) == 0:
			print len(segments[i].next)
			for nxt in segments[i].next:	
				if int(segments[i].start[0])==int(segments[nxt].start[0]) and int(segments[i].start[1])==int(segments[nxt].start[1]):
					# print str(i)+': '+segments[i].end[7]+' '+segments[segments[i].next[0]].start[7]
					if (int(segments[i].end[7])+1)%128==int(segments[nxt].start[7]):
						correct_joins+=1
					else:
						false_joins_2+=1
				else:
					false_joins_1+=1
		else:
			not_joined+=1

	print 'Segments created: ' + str(len(start_data))
	print 'Total connections made: '+str(total_edges)
	print 'Correct connections: '+str(correct_joins)
	print 'False connections: '+str(false_joins_1+false_joins_2)
	print 'False connection but right file: '+str(false_joins_2)
	print 'Not joined: '+str(not_joined)
	print 'Unmade connections: '+str(not_joined-int(sys.argv[3])) #str(len(segments)-int(sys.argv[3])-correct_joins-false_joins_1-false_joins_2)

	#success is measured as the number of edges made correctly (or not made at all)
	print 'Success rate: '+str(float(correct_joins+min(not_joined, int(sys.argv[3])))/len(start_data)*100)+'%'

	print 'Max possible success rate: ' +str(float(correct_joins+int(sys.argv[3]))/len(segments)*100)+'%'
	print 'Average choices for next segment: '+str(float(avg_choices_next)/len(segments))
	print 'Average choices for prev segment: '+str(float(avg_choices_prev)/len(segments))

if __name__ == '__main__':
	main()