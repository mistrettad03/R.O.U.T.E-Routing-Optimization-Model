from scipy.optimize import linprog
import numpy as np
import math

from itertools import permutations

class Optimization:
    def __init__(self, network):
        self.network = network
        self.isStrength = False
        self.nodes = list(self.network.get_nodes())
        self.arcs = list(self.network.get_arcs())
        self.A = None
        self.b = None
        self.c = None
        self.bounds = None
        
    # create matrices and arrays for LP
    def set_matrices(self):
        
        # create A matrix and b array for Flow Balance constraints
        self.A = np.zeros((len(self.nodes), len(self.arcs)))
        self.b = np.zeros(len(self.nodes))
        for n in self.nodes:
            i = self.nodes.index(n)
            for a in n.outArcList:
                j = self.arcs.index(a)
                self.A[i][j] = 1
            for a in n.inArcList:
                j = self.arcs.index(a)
                self.A[i][j] = -1
                
        # create objective function and bounds
        self.c = np.zeros(len(self.arcs))
        self.bounds = []
        for a in self.arcs:
            j = self.arcs.index(a)
            if self.isStrength:
                self.c[j] = -math.log10(a.weight/(1 + a.weight))
            else:
                self.c[j] = a.weight
            self.bounds.append((0, 1))
            
    # finds shortest or strongest path between origin and destination
    def shortest_path(self, origin, destination):
        path = None
        length = 0
        strength = 1
        
        if origin == destination:
            return path, length, strength
        
        # only b array changes with origin and destination
        self.b = np.zeros(len(self.nodes))
        orig_node = self.network.get_node(origin)
        dest_node = self.network.get_node(destination)
        orig_index = self.nodes.index(orig_node)
        dest_index = self.nodes.index(dest_node)
        self.b[orig_index] = 1
        self.b[dest_index] = -1
        
        # solve model
        res = linprog(self.c, A_eq = self.A, b_eq = self.b, bounds = self.bounds)
        
        # get results
        if res.status == 0:
            path = []
            n = orig_node
            while n.name != destination:
                for a in n.outArcList:
                    j = self.arcs.index(a)
                    if res.x[j] > 0.01:
                        path.append(a)
                        length += a.weight
                        strength *= a.weight / (1 + a.weight)
                        n = a.head
        return path, length, strength            
    
class Routing:

    def __init__(self, model, start_location, stopping_locations):       
        self.start_location = start_location
        self.stopping_locations = stopping_locations 
        self.model = model

        # generate route
    def generate_route(self, location_list):
        route_paths = None
        path_lengths = None
        if len(location_list) < 3:
            return path_lengths, route_paths
        route_paths = []
        path_lengths = []
        for i in range(len(location_list)-1):
            origin = location_list[i]
            destination = location_list[i+1]
            path, length, strength = self.model.shortest_path(origin, destination)
            route_paths.append(path)
            path_lengths.append(length)
        return route_paths, path_lengths    
    
        # generate all routes
    def get_optimal_route(self):     
        all_permutations = permutations(self.stopping_locations)
        optimal_route = None
        optimal_lengths = None
        best_length = 999999999
        for p in all_permutations:
            current_route = []
            current_route.append(self.start_location)
            current_route.extend(p)
            current_route.append(self.start_location)
            route_paths, path_lengths = self.generate_route(current_route)
            if sum(path_lengths) < best_length:
                optimal_route = route_paths
                best_length = sum(path_lengths)
                optimal_lengths = path_lengths
        return optimal_route, optimal_lengths
    
    # greedy solution
    def get_greedy_route(self):
        remaining_locations = [x for x in self.stopping_locations]
        greedy_length = []
        greedy_route = []
        origin = self.start_location
        while len(remaining_locations) > 0:
            best_path = None
            destination = None
            best_length = 999999999            
            for d in remaining_locations:
                path, length, strength = self.model.shortest_path(origin, d)
                if length < best_length:
                    best_path = path
                    destination = d
                    best_length = length
            greedy_length.append(best_length)
            greedy_route.append(best_path)
            origin = destination
            remaining_locations.remove(destination)
        path, length, strength = self.model.shortest_path(origin, self.start_location)
        greedy_length.append(length)
        greedy_route.append(path)
        return greedy_route, greedy_length    