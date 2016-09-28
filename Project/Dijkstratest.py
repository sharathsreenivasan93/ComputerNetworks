from collections import OrderedDict

next_hop_matrix = OrderedDict()
node_dict = {}

next_hop_matrix[0] = {0: 0, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None}
next_hop_matrix[1] = {0: None, 1: 1, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None}
next_hop_matrix[2] = {0: None, 1: None, 2: 2, 3: None, 4: None, 5: None, 6: None, 7: None}
next_hop_matrix[3] = {0: None, 1: None, 2: None, 3: 3, 4: None, 5: None, 6: None, 7: None}
next_hop_matrix[4] = {0: None, 1: None, 2: None, 3: None, 4: 4, 5: None, 6: None, 7: None}
next_hop_matrix[5] = {0: None, 1: None, 2: None, 3: None, 4: None, 5: 5, 6: None, 7: None}
next_hop_matrix[6] = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: 6, 7: None}
next_hop_matrix[7] = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: 7}


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
    current_node = initial_node
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

def print_route(graph, x, y):
    global next_hop_matrix
    global node_dict
    r = route(graph, x, y)
    #prmpt = ['({})'.format(x)]
    #print "Route is ",r
    last = r[-1]
    #temp_dict = {}
    count = 1
    if len(r) == 2:
        next_hop_matrix[r[0]][r[1]]=r[1]
    else:    
        for i in r:
            #temp_dict[last] = i+1
            next_hop_matrix[i][last]= r[count]
            count = count + 1
            if count == len(r)-1:
                break
    #print next_hop_matrix
    #for y in r[1:]:
     #   d = graph.distances.get((x, y))
      #  prmpt.append(' --{}-> ({})'.format(d,y))
       # x = y
    #print(''.join(prmpt))


if __name__ == '__main__':
    g = Graph()
    list = [0,1,2,3,4,5,6,7]
    g.nodes = set(list)
    node_dict = {1:'A', 2:'B', 3:'R1', 4:'R2', 5:'R3', 6:'R4', 7:'C', 8:'D'}
    g.add_edge(0, 1, 2000)
    g.add_edge(0, 4, 2000)
    g.add_edge(0, 5, 2000)
    
    g.add_edge(1, 0, 2000)
    g.add_edge(1, 4, 2000)
    g.add_edge(1, 5, 2000)
    
    g.add_edge(4, 0, 2000)
    g.add_edge(4, 1, 2000)
    g.add_edge(4, 5, 2000)
    g.add_edge(4, 7, 2000)
    g.add_edge(4, 6, 2000)
    
    g.add_edge(5, 0, 2000)
    g.add_edge(5, 1, 2000)
    g.add_edge(5, 4, 2000)
    g.add_edge(5, 6, 2000)
    g.add_edge(5, 7, 2000)
    
    g.add_edge(6, 2, 2000)
    g.add_edge(6, 3, 2000)
    g.add_edge(6, 4, 2000)
    g.add_edge(6, 5, 2000)
    g.add_edge(6, 7, 2000)
    
    g.add_edge(7, 2, 2000)
    g.add_edge(7, 3, 2000)
    g.add_edge(7, 4, 2000)
    g.add_edge(7, 5, 2000)
    g.add_edge(7, 6, 2000)
    
    g.add_edge(2, 3, 2000)
    g.add_edge(2, 6, 2000)
    g.add_edge(2, 7, 2000)
    
    g.add_edge(3, 2, 2000)
    g.add_edge(3, 6, 2000)
    g.add_edge(3, 7, 2000)
    #assert route(g, 1, 5) == [1, 3, 6, 5]
    #assert route(g, 5, 1) == [5, 6, 3, 1]
    #assert route(g, 2, 5) == [2, 3, 6, 5]
    #assert route(g, 1, 4) == [1, 3, 4]
    for i in range (0,8):
        for j in range(0,8):
            if i != j:
                print_route(g,i,j)
    print next_hop_matrix