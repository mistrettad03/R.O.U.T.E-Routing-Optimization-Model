from scipy.spatial import Delaunay

import numpy as np

import csv

import math

def get_delaunay_edges(entities):
    points = np.array([(x, y) for _, x, y in entities])
    entity_names = [name for name, _, _ in entities]

    tri = Delaunay(points)
    edges = set()
    for simplex in tri.simplices:
        for i in range(3):
            for j in range(i + 1, 3):
                entities = [min(entity_names[simplex[i]], entity_names[simplex[j]]),
                            max(entity_names[simplex[i]], entity_names[simplex[j]])]
                p = list(points[entity_names.index(entities[0])])
                q = list(points[entity_names.index(entities[1])])
                dist = math.dist(p, q)
                edge = (entities[0], entities[1], dist)
                edges.add(edge)

    return list(edges)