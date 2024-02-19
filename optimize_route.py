import numpy as np
from itertools import permutations
from scipy.spatial.distance import pdist, squareform

def main(path_coordinates):
    # Calculate the distance matrix using Euclidean distance
    distance_matrix = squareform(pdist(path_coordinates, metric='euclidean'))

    # Generate all possible routes, excluding the starting point for permutation
    # to prevent unnecessary repetition and reduce computational load
    all_routes = permutations(range(1, len(path_coordinates)))

    # Initialize variables to store the shortest route and its distance
    shortest_distance = np.inf
    shortest_route = None

    # Iterate through all possible routes to find the shortest one
    for route in all_routes:
        # Add the start point to the beginning and end of the route
        complete_route = (0,) + route + (0,)
        distance = sum(distance_matrix[route[i], route[i+1]] for i in range(len(route) - 1))
        if distance < shortest_distance:
            shortest_distance = distance
            shortest_route = complete_route

    return_list = list()
    for item in shortest_route:
        return_list.append(path_coordinates[item])
    
    return return_list