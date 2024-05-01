import misc as Misc
from PyQt6.QtWidgets import QMessageBox
import random
import math
# from database import NetworkDatabase
from delaunay import get_delaunay_edges

# represents users in the social network
class Node:
    
    
    # parameterized constructor
    def __init__(self, name=None):
        self.name = name # instance property
        # self.edgeList = [] # instance property
        self.outArcList = []
        self.inArcList = [] 
        
        self.degree = 0
        self.closeness = 0
        self.betweenness = 0
        
    # given node and edge returns friend
    @staticmethod
    def get_friend(n, e):
        try:
            if not n in e.nodeList:
                raise Exception('Node and edge are not connected.')
            j = abs(e.nodeList.index(n)-1)
            return e.nodeList[j]
        except Exception as e:
            Misc.show_message(e.args[0], 'Error', QMessageBox.Icon.Critical)
            return None  
        
    # overloaded addition operator to return friend node
    def __add__(self, e):
        return Node.get_friend(self, e)
        
# represents a (undirected) connection between users
class Edge:
    
    # default constructor
    def __init__(self):
        self.edgeName = None
        self.nodeList = []
        
    # return edge string
    @staticmethod
    def get_edge_name(s1, s2):
        key = s1 + '--' + s2
        if s1 > s2:
            key = s2 + '--' + s1
        return key        
    
# represents a directed connection between users
class Arc(Edge):
    
    def __init__(self, tail, head, weight):
        self.name = tail.name + '->' + head.name
        self.tail = tail
        self.head = head
        self.weight = weight
        self.edgeName = Edge.get_edge_name(tail.name, head.name)
        self.nodeList = [tail, head]
        tail.outArcList.append(self)
        head.inArcList.append(self)
        
    def get_strength(self):
        return self.weight / (1 + self.weight)
        
# representes the social network object with nodes and edges
class Network:
    # defaultbconstructor
    def __init__(self, database):
        self.nodeDict = {}
        self.edgeDict = {}
        self.arcDict = {}
        self.database = database
        
        self.generate_network()
        
    # add new node if it does not exit and return node
    def get_node(self, user):
        if not user in self.nodeDict:
            self.nodeDict[user] = Node(user)
        return self.nodeDict[user]
    
    # create the forward and backward arcs between two nodes
    def get_connection(self, user1, user2, weight):
        edgeName = Edge.get_edge_name(user1, user2)
        if not edgeName in self.edgeDict:
            n1 = self.get_node(user1)
            n2 = self.get_node(user2)
            # w = random.randint(1, 10)
            w = weight
            a1 = Arc(n1, n2, w)
            a2 = Arc(n2, n1, w)
            self.edgeDict[edgeName] = a1
            self.arcDict[a1.name] = a1
            self.arcDict[a2.name] = a2
    
    # initialize edges for all connections
    def generate_network(self):
        # connections, fields = self.database.get_network_data()
        data, fields = self.database.get_data()
        connections = get_delaunay_edges(data)

        for x in connections:
            self.get_connection(x[0], x[1], x[2])    
    
    # return keys from the node dictionary
    def get_node_names(self):
        return self.nodeDict.keys()
    
    # return values from the node dictionary
    def get_nodes(self):
        return self.nodeDict.values()
    
    # return values from the arc dictionary
    def get_arcs(self):
        return self.arcDict.values()

        
# class for hard-coded social network data
class NetworkData:
    # return the data for the application
    @staticmethod    
    def get_connections():
        return[["Alice", "Celine"],
            ["Alice", "Frank"],
            ["Blake", "Alice"],
            ["Celine", "Blake"],
            ["Celine", "Frank"],
            ["Daniel", "Alice"],
            ["Daniel", "Henry"],
            ["Emma", "Alice"],
            ["Emma", "Celine"],
            ["Emma", "Henry"],
            ["Frank", "Blake"],
            ["Frank", "Daniel"],
            ["Frank", "Henry"],
            ["Grace", "Alice"],
            ["Grace", "Daniel"],
            ["Grace", "Frank"],
            ["Henry", "Celine"],
            ["Henry", "Grace"],
            ["Henry", "Iris"],
            ["Iris", "Alice"],
            ["Iris", "Celine"]]
        
    # static method to create random connections
    @staticmethod
    def get_random_connections(n):
        userList = []      
        numdigit = math.floor(math.log10(n))
        for cnt in range(n):
            numzero = numdigit-math.floor(math.log10(cnt+1))
            userName = 'user'  
            for i in range(numzero):
                userName += '0'
            userName += str(cnt+1)
            userList.append(userName)
        connections = []
        while len(userList) > 1:
            u1 = userList[random.randint(0, len(userList)-1)]
            userList.remove(u1)
            u2 = userList[random.randint(0, len(userList)-1)]
            connections.append([u1, u2])
        return connections