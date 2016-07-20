__author__='architsh'
#beware of redundancy in the dataset

from geopy.distance import vincenty
import sys
import Queue

incoming,connected,end_truth,start_truth,aux,start,end=[],[],[],[],[],[],[]
count_start=0
count_end=0
files_to_be_written_to=[]
q_bfs=Queue.Queue()

def propagate(idx, file_number):
	global connected, end_truth, start_truth, aux, start, end, count_start, count_end, files_to_be_written_to, q_bfs
	
	q_bfs.put(idx)

	while not q_bfs.empty():
		front=q_bfs.get()
		for i in connected[front]:
			if file_number not in files_to_be_written_to[i]:
				files_to_be_written_to[i].add(file_number)
				q_bfs.put(i)

def main():
	global connected, end_truth, start_truth, aux, start, end, count_start, count_end, files_to_be_written_to, q_bfs

	start_file=open('./RouteTracing/start_data_2.txt','r').read().splitlines()
	
	#seconds after which the trips would be considered distinct for the same ID
	time_diff=30
	#metres after which the trips would be considered distinct for the same ID
	min_dist=500
	
	for line in start_file[1:]:
		entries=line.split(',')
		aux=[]
		for i in range(len(entries)):
			if i==0 or i==5:
				aux.append(int(entries[i]))
			else:
				aux.append(float(entries[i]))
		start.append(aux)
	
	end_file=open('./RouteTracing/end_data_2.txt','r').read().splitlines()
	
	for line in end_file[1:]:
		entries=line.split(',')
		aux=[]
		for i in range(len(entries)):
			if i==0 or i==5:
				aux.append(int(entries[i]))
			else:
				aux.append(float(entries[i]))
		end.append(aux)

	for i in range(len(start)):
		start_truth.append(True)
		end_truth.append(True)
		connected.append([])
		incoming.append([])

	print 'Connecting...'
	#constructs the graph (directed)
	for i in range(len(end)):
		for j in range(len(start)):
			if j!=i and start[j][1]-end[i][1]>=0 and start[j][1]-end[i][1]<=time_diff and vincenty((start[j][2],start[j][3]),(end[i][2],end[i][3])).km*1000<=min_dist:
				# print 'Connecting '+str(j)+' and ' + str(i)
				# print 'Time Diff: ' + str(start[j][1]-end[i][1])
				# print 'Distance: ' +str(vincenty((start[j][2],start[j][3]),(end[i][2],end[i][3])).km*1000)
				connected[i].append(j)
				incoming[j].append(i)
				start_truth[j]=False
				end_truth[i]=False 

	print 'Starting to write...'
	file_open=open('./RouteTracing/graph_'+str(time_diff)+'_'+str(min_dist)+'.txt','a')			

	#node number; boolean(0 if no outgoing edges);boolean(0 if no incoming edges);outgoing edges; incoming edges
	for i in range(len(start)):
		if start_truth[i]:
			dummy_1=str(0)
		else:
			dummy_1=str(1)

		if end_truth[i]:
			dummy_2=str(0)
		else:
			dummy_2=str(1)

		dummy_3=''
		for entry in connected[i][:len(connected[i])-1]:
			dummy_3+=str(entry)+','
		if not end_truth[i]:
			dummy_3+=str(connected[i][len(connected[i])-1])
		
		dummy_4=''
		for entry in incoming[i][:len(incoming[i])-1]:
			dummy_4+=str(entry)+','
		if not start_truth[i]:
			dummy_4+=str(incoming[i][len(incoming[i])-1])

		file_open.write(str(i)+';'+dummy_2+';'+dummy_1+';'+dummy_3+';'+dummy_4+'\n')

	for i in range(len(start)):
		start[i].append(i)
		if start_truth[i]==True:
			count_start+=1
			files_to_be_written_to.append(set([count_start]))
		else:
			files_to_be_written_to.append(set([]))
		if end_truth[i]==True:
			count_end+=1

	print count_start, count_end
	
	# # Using files start_data_1,end_data_1 at the settings of time_diff=600 and min_dist=500, 'xx' entries were found
	# # 									  at the settings of time_diff=5 and min_dist=100, 4286 distinct trips were found
	# # Using files start_data_2 and end_data_2,at the setting of time_diff=5 and min_dist=100, 3509 distinct starts were found along with 3609 exits
	
	# count=0
	# for i in range(len(start)):
	# 	if start_truth[i]==True:
	# 		count+=1
	# 		print 'About to propagate file #'+str(count)
	# 		propagate(i,count)
	# 		print 'Propagated'

	# final=open('./RouteTracing/final.txt','a')
	# final.write(str(count_start)+'\n')
	
	# for i in range(len(start)):
	# 	file_list=''
	# 	while len(files_to_be_written_to[i])>1:
	# 		file_list+=str(files_to_be_written_to[i].pop())+','
		
	# 	if(len(files_to_be_written_to[i])==1):
	# 		file_list+=str(files_to_be_written_to[i].pop())
		
	# 	final.write(str(start[i][5])+','+str(end[i][5])+','+file_list+'\n')

if __name__ == '__main__':
	main()	