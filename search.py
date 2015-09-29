
import sys
import heapq
import Queue

def BreathFisrtSearch(startNode,endNode):

    visited = list()

    # convert name to actual node obj
    startNode = graph.getNode(startNode)
    endNode = graph.getNode(endNode)

    queue = Queue.Queue()
    queue.put(startNode)

    while not queue.empty() :

        # dequeue
        currentNode = queue.get()

        # mark as visited
        visited.append(currentNode)

        # found the target node
        if currentNode == endNode:
            return result(startNode,endNode)

        # sort connections alphabetically first
        currentNode.edges.sort(key = lambda x:x.nodeTo.name)

        # add connecting nodes to queue
        for connection in currentNode.edges:
            if connection.nodeTo not in visited:
                connection.nodeTo.distanceFromStartNode = currentNode.distanceFromStartNode + connection.cost
                connection.nodeTo.discoveredBy = currentNode
                queue.put(connection.nodeTo)

    return None

def DepthFirstSearch(startNode,endNode):

    # convert name to actual node obj
    startNode = graph.getNode(startNode)
    endNode = graph.getNode(endNode)

    # init
    stack = Stack()
    visited = list()

    stack.push(startNode)
    visited.append(startNode)

    while not stack.isEmpty():

        # get top node
        currentNode = stack.peek()

        # destination reached
        if currentNode == endNode:
            return result(startNode,currentNode)

        # sort connection alphabetically first
        currentNode.edges.sort(key = lambda x:x.nodeTo.name)

        # go deep
        hasEdges = False
        for connection in currentNode.edges:
            if not connection.nodeTo in visited:
                connection.nodeTo.discoveredBy = currentNode
                connection.nodeTo.distanceFromStartNode = connection.cost + currentNode.distanceFromStartNode
                stack.push(connection.nodeTo)
                visited.append(connection.nodeTo)
                hasEdges = True
                break

        # if no edges, pop and continue to next node
        if not hasEdges:
            stack.pop()

    return None

def UniformCostSearch(startNode,endNode):

    # convert name to actual node obj
    startNode = graph.getNode(startNode)
    endNode = graph.getNode(endNode)

    # init a queue
    queue = PriorityQueue()
    visited = list()

    queue.put(startNode,0)

    while not queue.empty():

        currentNode = queue.get()

        # mark node as visited
        visited.append(currentNode)

        # reach destination
        if(currentNode == endNode):
            return result(startNode,currentNode)

        # iterate through all edges
        for edge in currentNode.edges:

            # visited node
            if edge.nodeTo in visited:
                continue

            # this is a shorter path update distance
            if edge.nodeTo.distanceFromStartNode > currentNode.distanceFromStartNode + edge.cost or edge.nodeTo.distanceFromStartNode == 0:
                edge.nodeTo.discoveredBy = currentNode
                edge.nodeTo.distanceFromStartNode = currentNode.distanceFromStartNode + edge.cost

            queue.put(edge.nodeTo,edge.nodeTo.distanceFromStartNode)

    return None

def BestFirstSearch(startNode,endNode):

    # convert name to actual node obj
    startNode = graph.getNode(startNode)
    endNode = graph.getNode(endNode)

    # init a queue
    queue = PriorityQueue()
    visited = list()

    queue.put(startNode,0)

    while not queue.empty():

        currentNode = queue.get()

        # mark node as visited
        visited.append(currentNode)

        # found destination
        if currentNode == endNode:
            return result(startNode,currentNode)

        # iterate through all edges
        for edge in currentNode.edges:

            # visited node
            if edge.nodeTo in visited:
                continue

            edge.nodeTo.discoveredBy = currentNode
            edge.nodeTo.distanceFromStartNode = currentNode.distanceFromStartNode + edge.cost

             # calculate f(n) = h(n)
            queue.put(edge.nodeTo,edge.nodeTo.heuristicValues)

    return None

def AStarSearch(startNode,endNode):

    # convert name to actual node obj
    startNode = graph.getNode(startNode)
    endNode = graph.getNode(endNode)

    # init a queue
    queue = PriorityQueue()
    visited = list()

    queue.put(startNode,0)

    while not queue.empty():

        currentNode = queue.get()

        # mark node as visited
        visited.append(currentNode)

        # found destination
        if currentNode == endNode:
            return result(startNode,currentNode)

        # iterate through all edges
        for edge in currentNode.edges:

            # visited node
            if edge.nodeTo in visited:
                continue

            # this is a shorter path update distance
            #if edge.nodeTo.distanceFromStartNode > currentNode.distanceFromStartNode + edge.cost or edge.nodeTo.distanceFromStartNode == 0:
            edge.nodeTo.discoveredBy = currentNode
            edge.nodeTo.distanceFromStartNode = currentNode.distanceFromStartNode + edge.cost

             # calculate f(n) = g(n) + h(n)
            fvalue = edge.nodeTo.distanceFromStartNode + edge.nodeTo.heuristicValues
            queue.put(edge.nodeTo,fvalue)

    return None

def result(startNode,endNode):

    # get path
    path = list()
    cost = endNode.distanceFromStartNode
    node = endNode
    while not node == startNode:
        path.append(node)
        node = node.discoveredBy

    path.append(startNode)
    path.reverse()

    result = []
    result.append(path)
    result.append(endNode.distanceFromStartNode)

    return result

class Parser(object):
    """InputGraph Parser"""
    def __init__(self):
        pass

    def ParseLine(self,strLine):

        # split string by space
        strParts = strLine.split()

        # parse graph data
        nodeNameFrom = strParts[0]
        nodeNameTo = strParts[1]
        distance = strParts[2]

        if graph.hasNode(nodeNameFrom):
            nodeFrom = graph.getNode(nodeNameFrom)
        else:
            nodeFrom = Node(nodeNameFrom)

        if graph.hasNode(nodeNameTo):
            nodeTo = graph.getNode(nodeNameTo)
        else:
            nodeTo = Node(nodeNameTo)

        # create connection
        connection = Connection(nodeFrom,nodeTo,distance)
        nodeFrom.AddConnection(connection)

        # add nodes to graph
        graph.AddNode(nodeFrom)
        graph.AddNode(nodeTo)

    def ParseHeuristic(self,strLine):

        # split string by space
        strparts = strLine.split()

        nodeName = strparts[0]
        heuristic = strparts[1]

        node = graph.getNode(nodeName)
        node.setHeuristicValues(int(heuristic))

class Graph(object):
    """docstring for Graph"""

    def __init__(self):
        self.nodes = list()

    def AddNode(self,newNode):

        for node in self.nodes:
            if newNode.name == node.name:
                return

        self.nodes.append(newNode)

    def Display(self):
        for node in self.nodes:
            print(node.name)
            print("connections of " + node.name + ": ")

            # sort connection alphabetically first
            node.edges.sort(key = lambda x:x.nodeTo.name)

            for connection in node.edges:
                print(connection.nodeFrom.name + " to " + connection.nodeTo.name + " cost " + str(connection.cost))

            print("")

    def hasNode(self,name):
        for node in self.nodes:
          if node.name == name:
            return True

        return False

    def getNode(self,name):
        for node in self.nodes:
            if node.name == name:
                return node

    def getConnectionCost(self,fromNodeName,toNodeName):

        node = self.getNode(fromNodeName)

        for connection in node.edges:
            if connection.nodeTo.name == toNodeName:
                return connection.cost

class Node(object):
    """docstring for Node"""
    def __init__(self, name):
        self.name = name
        self.edges = list()
        self.discoveredBy = None
        self.distanceFromStartNode = 0
        self.heuristicValues = 0

    def setHeuristicValues(self,heuristicValues):
        self.heuristicValues = heuristicValues

    def AddConnection(self,connection):
        self.edges.append(connection)

class Connection(object):
    """docstring for Edge"""
    def __init__(self, nodeFrom,nodeTo,cost):
        self.nodeFrom = nodeFrom
        self.nodeTo = nodeTo
        self.cost = int(cost)

class Stack(object):

    def __init__(self):
        self.items = []

    def push(self,item):
        self.items.insert(0,item)

    def pop(self):
        return self.items.pop(0)

    def peek(self):
        return self.items[0]

    def size(self):
        return len(self.items)

    def isEmpty(self):
        return self.items == []

class PriorityQueue(object):

    def __init__(self):
        self.items = []

    def empty(self):
        return len(self.items) == 0

    def put(self,item,priority):
        heapq.heappush(self.items,(priority,item))

    def get(self):
        return heapq.heappop(self.items)[1]

# get command line arguments
inputGraphFileName = str(sys.argv[1])
heuristicValuesFileName = str(sys.argv[2])
algorithm = str(sys.argv[3])
startNodeName = str(sys.argv[4])
goalNodeName = str(sys.argv[5])
outputFileName = str(sys.argv[6])

# read input graph file and parse
inputGraph_file = open(inputGraphFileName, "r")

lines = inputGraph_file.readlines()

# init graph
graph = Graph()

# init parser
parser = Parser()

# parse each line
for line in lines:
    parser.ParseLine(line)

# parse heuristic data
heuristic_file = open(heuristicValuesFileName,"r")
lines = heuristic_file.readlines()
for line in lines:
    parser.ParseHeuristic(line)

#graph.Display()

if algorithm == "breadth":
    result = BreathFisrtSearch(startNodeName,goalNodeName)

elif algorithm == "depth":
    result = DepthFirstSearch(startNodeName,goalNodeName)

elif algorithm == "uniform":
    result = UniformCostSearch(startNodeName,goalNodeName)

elif algorithm == "best":
    result = BestFirstSearch(startNodeName,goalNodeName)

elif algorithm == "astar":
    result = AStarSearch(startNodeName,goalNodeName)

outputFile = open(outputFileName,"w")
for node in result[0]:
    outputFile.writelines(node.name + "\n")
outputFile.writelines(str(result[1]))

