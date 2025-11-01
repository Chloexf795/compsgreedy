"""
Part A: Dijkstra Algorithm for Different Parties - Solution

This file focuses on implementing Dijkstra's algorithm from company and driver's different perspectives

Complete implementation for Instructors
"""

import heapq
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Tuple
from main import Node, Edge, calculate_company_cost, calculate_driver_cost, get_neighbors


# ============================================================================
# PART A: DIJKSTRA ALGORITHM COMPLETE IMPLEMENTATIONS
# ============================================================================

def dijkstra_company_route(start: Node, target: Node, nodes: List[Node], edges: List[Edge]) -> Tuple[List[Node], float]:
    """
    Part A1: Complete implementation of Dijkstra's algorithm from company's perspective.
    """
    # Initialize distances and previous pointers
    distances = {node: float('inf') for node in nodes}
    distances[start] = 0.0
    previous = {node: None for node in nodes}
    
    # Priority queue: (distance, node)
    pq = [(0.0, start)]
    visited = set()
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        # Skip if already visited (handles duplicate entries in pq)
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        # Found target - we can stop early
        if current_node == target:
            break
            
        # Check all neighbors
        neighbors = get_neighbors(current_node, edges)
        for neighbor in neighbors:
            if neighbor in visited:
                continue
                
            # Calculate cost using company perspective
            edge_cost = calculate_company_cost(current_node, neighbor)
            new_distance = current_dist + edge_cost
            
            # Update if shorter path found
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (new_distance, neighbor))
    
    # Reconstruct path
    path = []
    current = target
    
    # Check if target is reachable
    if distances[target] == float('inf'):
        return [], float('inf')
    
    while current is not None:
        path.append(current)
        current = previous[current]
    
    path.reverse()
    return path, distances[target]


def dijkstra_driver_route(start: Node, target: Node, nodes: List[Node], edges: List[Edge]) -> Tuple[List[Node], float]:
    """
    Part A2: Complete implementation of Dijkstra's algorithm from driver's perspective.
    """
    # Initialize distances and previous pointers
    distances = {node: float('inf') for node in nodes}
    distances[start] = 0.0
    previous = {node: None for node in nodes}
    
    # Priority queue: (distance, node)
    pq = [(0.0, start)]
    visited = set()
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        # Skip if already visited
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        # Found target - we can stop early
        if current_node == target:
            break
            
        # Check all neighbors
        neighbors = get_neighbors(current_node, edges)
        for neighbor in neighbors:
            if neighbor in visited:
                continue
                
            # Calculate cost using driver perspective
            edge_cost = calculate_driver_cost(current_node, neighbor)
            new_distance = current_dist + edge_cost
            
            # Update if shorter path found
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (new_distance, neighbor))
    
    # Reconstruct path
    path = []
    current = target
    
    # Check if target is reachable
    if distances[target] == float('inf'):
        return [], float('inf')
    
    while current is not None:
        path.append(current)
        current = previous[current]
    
    path.reverse()
    return path, distances[target]


# ============================================================================
# RUNNING FUNCTIONS
# ============================================================================

def run_part_a():
    """
    Run Part A implementations with Minnesota data.
    """
    try:
        from mn_dataset import MN_NODES_DICT, MN_EDGES, START_CITY
        
        print("=" * 80)
        print("PART A: COMPANY VS DRIVER ALGORITHM COMPARISON")

        # Sample destinations  
        sample_destinations = ["Northfield", "Stillwater"]
        
        for dest_name in sample_destinations:
            if dest_name not in MN_NODES_DICT:
                continue
                
            destination = MN_NODES_DICT[dest_name]
            print(f"\nRoute from {START_CITY.name} to {destination.name}:")
            print("-" * 50)
            
            # Company algorithm
            company_path, company_cost = dijkstra_company_route(START_CITY, destination, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"Company algorithm: {' -> '.join([node.name for node in company_path])}")
            print(f"Company cost: ${company_cost:.2f}")
            
            # Driver algorithm
            driver_path, driver_cost = dijkstra_driver_route(START_CITY, destination, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"Driver algorithm: {' -> '.join([node.name for node in driver_path])}")
            print(f"Driver cost: ${driver_cost:.2f}")
                
    except Exception as e:
        print(f"Error in Part A testing: {e}")


def main():
    """
    Main function for Part A testing.
    """
    print("Dijkstra Algorithm Assignment - Part A: Basic Algorithm Implementation")
    
    # Load dataset info
    try:
        from mn_dataset import MN_NODES_DICT, MN_EDGES, START_CITY
    except ImportError:
        print("Error: Could not load Minnesota dataset")
    
    # Run tests
    run_part_a()


if __name__ == "__main__":
    main()
