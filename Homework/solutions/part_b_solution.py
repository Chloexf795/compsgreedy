"""
Part B: Northfield Subsidies! - Solution

This file explores what happens when Dijkstra's algorithm encounters negative edge weights.

You should copy and modify dijkstra algorithm from A2.
"""
import heapq
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Tuple
from main import Node, Edge, get_neighbors
from part_a_solution import calculate_driver_cost


# ============================================================================
# PART B: NORTHFIELD SUBSIDIES COMPLETE IMPLEMENTATION
# ============================================================================

def dijkstra_with_northfield_subsidy(start: Node, target: Node, nodes: List[Node], edges: List[Edge]) -> Tuple[List[Node], float]:
    """
    Complete implementation: Dijkstra with Northfield subsidy (demonstrates negative weight issue).
    
    This implementation shows what happens when we introduce negative edge weights.
    Trip from Lakeville to Northfield costs -$100, which creates incorrect shortest paths.
    Normal connectivity is preserved, just Lakeville->Northfield has negative cost.
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
        
        # Continue exploring (no early termination to find subsidized paths)
        # This allows us to find cheaper paths with negative weights
            
        # Check all neighbors
        neighbors = get_neighbors(current_node, edges)
        for neighbor in neighbors:
            if neighbor in visited:
                continue
                
            # MODIFICATION: Northfield subsidy
            if current_node.id == "Lakeville" and neighbor.id == "Northfield":
                edge_cost = -100.0  # Large negative cost from Lakeville to Northfield!
            else:
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
# RUN FUNCTIONS
# ============================================================================

def run_part_b():
    """
    Demonstrate the issues with negative weights in Dijkstra's algorithm.
    """
    try:
        from mn_dataset import MN_NODES_DICT, MN_EDGES
        from part_a_solution import dijkstra_driver_route
        
        print("=" * 80)
        print("PART B ANALYSIS: Negative Edge Weights Problem")
        
        # Test: Route from Minneapolis to Northfield (multiple paths available)
        start_city = MN_NODES_DICT["Minneapolis"]
        northfield = MN_NODES_DICT["Northfield"]
        print(f"\nRun routes from {start_city.name} to {northfield.name}")
        
        regular_path, regular_cost = dijkstra_driver_route(start_city, northfield, list(MN_NODES_DICT.values()), MN_EDGES)
        subsidy_path, subsidy_cost = dijkstra_with_northfield_subsidy(start_city, northfield, list(MN_NODES_DICT.values()), MN_EDGES)
        
        print(f"Regular: {' -> '.join([node.name for node in regular_path])} (${regular_cost:.2f})")
        print(f"Subsidy: {' -> '.join([node.name for node in subsidy_path])} (${subsidy_cost:.2f})")

    
    except Exception as e:
        print(f"Error in negative weight demonstration: {e}")


def main():
    """
    Main function for Part B solution running.
    """
    print("Dijkstra Algorithm Assignment - Part B Solution Testing")
    
    # Load dataset
    try:
        from mn_dataset import MN_NODES_DICT, MN_EDGES
        print(f"Minnesota rideshare network: {len(MN_NODES_DICT)} cities, {len(MN_EDGES)} connections")
    except ImportError:
        print("Error: Could not load Minnesota dataset")
        return
    
    # Run part b
    run_part_b()


if __name__ == "__main__":
    main()
