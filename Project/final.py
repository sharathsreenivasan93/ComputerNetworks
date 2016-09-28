import numpy
import math
#from operator import itemgetter
from collections import OrderedDict
from random import randint

lamda = 100
frameslot = 50 #microsec
td1 = 80 #microsec
td2 = 8
pd = 10 #microsec
tot_delay1 = td1 + pd
tot_delay2 = td2 + pd
CLOCK = 0
SIM_TIME = 30000 # secs
GEN_TIME = [0.0, 0.0, 0.0, 0.0]
PKT_LIST = []
LINK_PKT_LISTS = [[] for i in range (6)]
PKT_SIZE = 1000
maxbackoff = 3
count_track = [0, 0, 0, 0, 0, 0, 0, 0]
tbackoff = 50
backoff_dict = {}
clockcheck = 0
next_hop_matrix = OrderedDict()

next_hop_matrix[0] = {0: 0, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None}
next_hop_matrix[1] = {0: None, 1: 1, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None}
next_hop_matrix[2] = {0: None, 1: None, 2: 2, 3: None, 4: None, 5: None, 6: None, 7: None}
next_hop_matrix[3] = {0: None, 1: None, 2: None, 3: 3, 4: None, 5: None, 6: None, 7: None}
next_hop_matrix[4] = {0: None, 1: None, 2: None, 3: None, 4: 4, 5: None, 6: None, 7: None}
next_hop_matrix[5] = {0: None, 1: None, 2: None, 3: None, 4: None, 5: 5, 6: None, 7: None}
next_hop_matrix[6] = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: 6, 7: None}
next_hop_matrix[7] = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: 7}
k = 0

link_contents = [[0, 1, 4, 5],
                 [2, 3, 6, 7],
                 [4, 6], 
                 [4, 7],
                 [5, 6],
                 [5, 7]
                ]

class Graph(object):
   def __init__(self):
       self.nodes = set()
       self.edges = {}
       self.distances = {}

   def add_node(self, value):
       self.nodes.add(value)

   def add_edge(self, from_node, to_node, distance):
       self._add_edge(from_node, to_node, distance)
       self._add_edge(to_node, from_node, distance)

   def _add_edge(self, from_node, to_node, distance):
       self.edges.setdefault(from_node, [])
       self.edges[from_node].append(to_node)
       self.distances[(from_node, to_node)] = distance

def dijkstra(graph, initial_node):
    visited = {initial_node: 0}
    #current_node = initial_node
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node

        if min_node is None:
            break

        nodes.remove(min_node)
        cur_wt = visited[min_node]

        for edge in graph.edges[min_node]:
            wt = cur_wt + graph.distances[(min_node, edge)]
            if edge not in visited or wt < visited[edge]:
                visited[edge] = wt
                path[edge] = min_node

    return visited, path

def route(graph, x, y):
    distances, paths = dijkstra(graph, x)
    route = [y]

    while y != x:
        route.append(paths[y])
        y = paths[y]

    route.reverse()
    return route

def evaluate_nexthop(graph, x, y):
    global next_hop_matrix
    global node_dict
    r = route(graph, x, y)
    last = r[-1]
    count = 1
    if len(r) == 2:
        next_hop_matrix[r[0]][r[1]]=r[1]
    else:    
        for i in r:
            next_hop_matrix[i][last]= r[count]
            count = count + 1
            if count == len(r)-1:
                break


def calculate_nexthop():
    g = Graph()
    list = [0,1,2,3,4,5,6,7]
    g.nodes = set(list)
    cost1 = 2000 * numpy.random.random_integers(1,10)
    cost2 = 2000 * numpy.random.random_integers(1,10)
    cost3 = 2000 * numpy.random.random_integers(1,10)
    cost4 = 2000 * numpy.random.random_integers(1,10)
    cost5 = 2000 * numpy.random.random_integers(1,10)
    cost6 = 2000 * numpy.random.random_integers(1,10)
    g.add_edge(0, 1, cost1)
    g.add_edge(0, 4, cost1)
    g.add_edge(0, 5, cost1)
    
    g.add_edge(1, 4, cost1)
    g.add_edge(1, 5, cost1)
    
    g.add_edge(4, 5, cost1)
    g.add_edge(4, 7, cost4)
    g.add_edge(4, 6, cost3)
    
    g.add_edge(5, 6, cost5)
    g.add_edge(5, 7, cost6)
    
    g.add_edge(6, 2, cost2)
    g.add_edge(6, 3, cost2)
    g.add_edge(6, 7, cost2)
    
    g.add_edge(7, 2, cost2)
    g.add_edge(7, 3, cost2)
    
    g.add_edge(2, 3, cost2)
    for i in range (0,8):
        for j in range(0,8):
            if i != j:
                evaluate_nexthop(g,i,j)

class Packet():
    def __init__(self, time, src, dst, txtime, rectime, prev_ref_time, collision, int_src, int_dst):
        self.create_time = time
        self.src = src
        self.dst = dst
        self.txtime = txtime
        self.rectime = rectime
        self.prev_ref_time = prev_ref_time
        self.collision = collision
        self.int_src = src
        self.int_dst = dst
    
    def display(self):
        print "src: {}, dest: {}, create_time: {}, trans_time: {}, rec_time: {}, prev_ref_time: {}, collisions: {}".\
            format(self.src, self.dst, self.create_time, self.txtime, self.rectime, self.prev_ref_time, self.collision)

class Node():
    def __init__(self, n_id, sent_count, recd_count):
        self.n_id = n_id
        self.sent_count = sent_count
        self.recd_count = recd_count

    def display(self):
        print "node_id: {}, sent_count: {}, received_count: {}".\
            format(self.n_id, self.sent_count, self.recd_count)

def update_clock():
    global CLOCK
    global PKT_LIST
    global LINK_PKT_LISTS
    global clockcheck    
    PKT_LIST.sort(key=lambda x: x.prev_ref_time, reverse=False)
    for i in LINK_PKT_LISTS:
        i.sort(key=lambda x: x.prev_ref_time, reverse=False)
    CLOCK = PKT_LIST[0].prev_ref_time
    if (CLOCK - clockcheck) >= 2000:
        calculate_nexthop()
        clockcheck = CLOCK
    

def create_packet(node_id):     
    global lamda  
    global PKT_LIST
    dest = 0
    int_time = numpy.random.poisson(lamda)
    GEN_TIME[node_id] = GEN_TIME[node_id] + int_time
    while(1):
        dest = randint(0, 3)
        if dest != node_id:
            break
    p = Packet(GEN_TIME[node_id], node_id, dest, 0, 0, GEN_TIME[node_id], 0, node_id, dest) 
    #print p.prev_ref_time    
    s_id = p.src
    d_id = p.dst
    
    int_node = next_hop_matrix[s_id][d_id]
    p.int_src = s_id
    p.int_dst = int_node
   # print "Packet source, destination and intermediate node ", p.src, p.dst, p.int_dst
    PKT_LIST.append(p)
    a = 0
    for i in link_contents:
        if p.int_src in i and int_node in i:
            LINK_PKT_LISTS[a].append(p)
            break
        a = a + 1
    
def delay_packets(delay):
    global PKT_LIST    
    global CLOCK
    global LINK_PKT_LISTS
    CLOCK = CLOCK + delay
    #print 'CLOCK', CLOCK
    
    count = 0
    list1 = []
    for i in PKT_LIST:
        if (i.prev_ref_time - CLOCK) < 0:
            list1.append(count)
        count = count + 1
    for i in list1:
        PKT_LIST[i].prev_ref_time = CLOCK
    for i in LINK_PKT_LISTS:
        list1 = []
        count = 0
        for j in i:
            if (j.prev_ref_time - CLOCK) < 0:
                list1.append(count)
            count = count + 1
        for j in list1:
            i[j].prev_ref_time = CLOCK
                    

def getcurtime(node):
    global PKT_LIST
    count = 0
    t = 0
    idx = 0
    for i in PKT_LIST:
        if i.int_src == node:
            idx = count
            break
        count = count + 1
    t = PKT_LIST[idx].prev_ref_time
    return t
            
def delaynodepkts(node, delay):
    global LINK_PKT_LISTS
    global k
    DELAYTIME = getcurtime(node) + delay
    #print 'in delaynodepkts '
    #print 'current_time of', node,' is', getcurtime(node)    
   # print 'delay of', node,' is', delay    
  #  print 'DELAYTIME ', DELAYTIME
    count = 0
    list1 = []
    for i in PKT_LIST:
        if (i.prev_ref_time - DELAYTIME) < 0 and i.int_src == node:
            list1.append(count)
        count = count + 1
    for i in list1:
        PKT_LIST[i].prev_ref_time = DELAYTIME
    for i in LINK_PKT_LISTS:
        list1 = []
        count = 0
        for j in i:
            if (j.prev_ref_time - DELAYTIME) < 0 and j.int_src == node:
                list1.append(count)
            count = count + 1
        for j in list1:
            i[j].prev_ref_time = DELAYTIME
                        
        #print PKT_LIST[i].prev_ref_time

if __name__ == '__main__':
    c_count = 0
    calculate_nexthop()
    create_packet(0)
    create_packet(1)
    create_packet(2)
    create_packet(3)
    update_clock()
    tot_delay = 0
    while(True):
    #for i in range(50000):
        update_clock()
        if len(LINK_PKT_LISTS[k]) == 0:
            k = (k + 1) % 6
            continue
        else:        
            p = LINK_PKT_LISTS[k][0]
            int_src = p.int_src
            int_dest = p.int_dst
           # print "Current packet's intermediate source and destination ",int_src, int_dest
          #  print "Current packet's prev_ref_time ", p.prev_ref_time            
            if len(LINK_PKT_LISTS[k]) == 1:
                t_diff = pd + 1
            else:
                q = LINK_PKT_LISTS[k][1]
                t_diff = q.prev_ref_time - p.prev_ref_time
           # print "for iteration", i
           # print q.prev_ref_time, p.prev_ref_time, t_diff
            
            if t_diff > pd: #No collision case
                if p.txtime == 0:
                    p.txtime = p.prev_ref_time
                if k < 2:
                    tot_delay = tot_delay1
                else:
                    tot_delay = tot_delay2
                p.rectime = p.prev_ref_time + tot_delay
                count_track[int_src] = count_track[int_src] + 1            
               # print "Transmission and receiving time ",p.txtime, p.rectime
                LINK_PKT_LISTS[k].pop(0)
                PKT_LIST.pop(0) 
                #INSERT NEXT HOP CODE
                if int_src < 4:
                    create_packet(p.src)
                    delay_packets(tot_delay)
                if p.int_dst > 3:
                    p.create_time = p.rectime                    
                    int_node = next_hop_matrix[p.int_dst][p.dst]
                    p.int_src = p.int_dst
                    p.int_dst = int_node   
                    a = 0
                    for i in link_contents:
                        if p.int_src in i and p.int_dst in i:
                            LINK_PKT_LISTS[a].append(p)
                            PKT_LIST.append(p)
                            break
                        a = a + 1
                #print "Packet created at ", src
                #delay_packets(tot_delay)
                #print '----------------------------------------------------'
    
            else: #Collision case
                #print "collision case", i 
                c_count = c_count + 1
                if p.txtime == 0:
                    p.txtime = p.prev_ref_time
                if q.txtime == 0:
                    q.txtime == q.prev_ref_time
                
                p.collision = p.collision + 1
                q.collision = q.collision + 1
                
                if p.collision < maxbackoff:
                    backoff_dict[p.int_src] = (numpy.random.random_integers(0, math.pow(2, int(p.collision))-1)) * tbackoff
                else:
                    backoff_dict[p.int_src] = (numpy.random.random_integers(0, math.pow(2,maxbackoff)) - 1) * tbackoff
                
                if q.collision < maxbackoff:
                    backoff_dict[q.int_src] = (numpy.random.random_integers(0, math.pow(2, int(q.collision))-1)) * tbackoff
                else:
                    backoff_dict[q.int_src] = (numpy.random.random_integers(0,math.pow(2,maxbackoff)) - 1) * tbackoff
               # print 'p.int_src:', p.int_src
              #  print 'q.int_src:', q.int_src
               # print k
               # print backoff_dict[p.int_src]            
               # print backoff_dict[q.int_src]
                delaynodepkts(p.int_src, pd + t_diff + backoff_dict[p.int_src])
                delaynodepkts(q.int_src, pd - t_diff + backoff_dict[q.int_src])
                #print 'no of collisions', c_count
               # print '----------------------------------------------------'
        k = (k + 1) % 6
        if numpy.min(GEN_TIME) > SIM_TIME:
            print "Completed"
            #calcstat()
            break
    
    print "No of packets from A: ", count_track[0]
    print "No of packets from B: ", count_track[1]
    print "No of packets from C: ", count_track[2]
    print "No of packets from D: ", count_track[3]
    print "No of packets from R1: ", count_track[4]
    print "No of packets from R2: ", count_track[5]
    print "No of packets from R3: ", count_track[6]
    print "No of packets from R4: ", count_track[7]
    
    print "No of packets which suffered collisions: ", c_count
    