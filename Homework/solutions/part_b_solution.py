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
from solutions.part_a_solution import calculate_driver_cost


# ============================================================================
# PART B: NORTHFIELD SUBSIDIES COMPLETE IMPLEMENTATION
# ============================================================================

def dijkstra_with_northfield_subsidy(start: Node, target: Node, nodes: List[Node], edges: List[Edge]) -> Tuple[List[Node], float]:
    """
    Complete implementation: Dijkstra with Northfield subsidy (demonstrates negative weight issue).
    
    This implementation shows what happens when we introduce negative edge weights.
    Trip from Lakeville to Northfield costs -$20.00
    """
    # Initialize distances and previous pointers
    distances = {node: float('inf') for node in nodes}
    distances[start] = 0.0
    previous = {node: None for node in nodes}
    
    # Priority queue: (distance, counter, node) - counter prevents Node comparison
    pq = [(0.0, 0, start)]
    visited = set()
    counter = 1  # For tie-breaking in heapq
    
    while pq:
        current_dist, _, current_node = heapq.heappop(pq)
        
        # Skip if already visited
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        # Found target - we can stop early (this is Dijkstra's greedy assumption!)
        # This is WHY Dijkstra fails with negative weights!
        if current_node == target:
            break
            
        # Check all neighbors
        neighbors = get_neighbors(current_node, edges)
        for neighbor in neighbors:
            if neighbor in visited:
                continue
                
            # MODIFICATION: Subsidy - make an edge that's NOT on the direct path negative
            if current_node.id == "Lonsdale" and neighbor.id == "Northfield":
                edge_cost = -20.0  # Negative cost from Lonsdale to Northfield
            else:
                edge_cost = calculate_driver_cost(current_node, neighbor)
                
            new_distance = current_dist + edge_cost
            
            # Update if shorter path found
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (new_distance, counter, neighbor))
                counter += 1
    
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
    Demonstrate Dijkstra's failure: it finds the same path as Part A, missing the cheaper negative-weight path.
    """
    print("=" * 80)
    print("PART B ANALYSIS: Negative Edge Weights Problem")
    print("=" * 80)
    try:
        from mn_dataset import MN_NODES_DICT, MN_EDGES
        from solutions.part_a_solution import dijkstra_driver_route
        
        start_city = MN_NODES_DICT["Edina"]
        northfield = MN_NODES_DICT["Northfield"]
        print(f"Route from {start_city.name} to {northfield.name}")
        print(f"Subsidy rule: Trip from Lonsdale to Northfield costs -$20.00")
        print()
        
        # Get the regular path (without subsidy)
        regular_path, regular_cost = dijkstra_driver_route(start_city, northfield, list(MN_NODES_DICT.values()), MN_EDGES)
        print(f"Regular (Part A): {' -> '.join([node.name for node in regular_path])} (${regular_cost:.2f})")
        
        # Get Dijkstra's path with negative edge available (should be SAME as regular!)
        subsidy_path, subsidy_cost = dijkstra_with_northfield_subsidy(start_city, northfield, list(MN_NODES_DICT.values()), MN_EDGES)
        print(f"With Negative Edge: {' -> '.join([node.name for node in subsidy_path])} (${subsidy_cost:.2f})")
        print()
        
        # Calculate what the TRUE optimal path should be via Lonsdale
        lonsdale = MN_NODES_DICT["Lonsdale"]
        path_to_lonsdale, cost_to_lonsdale = dijkstra_driver_route(start_city, lonsdale, list(MN_NODES_DICT.values()), MN_EDGES)
        true_optimal_cost = cost_to_lonsdale + (-20.0)
        
        print("ANALYSIS:")
        print("Because we add in the subsidy")
        print(f"the TRUE cheapest path is: {' -> '.join([node.name for node in path_to_lonsdale])} -> Northfield")
        print(f"True optimal cost: ${cost_to_lonsdale:.2f} + (-$20.00) = ${true_optimal_cost:.2f}")
        print()
        
        if abs(subsidy_cost - regular_cost) < 0.01:
            print("DIJKSTRA FAILED!")
            print(f"• Found the same path as regular Dijkstra (${subsidy_cost:.2f})")
            print(f"• Missed the cheaper path via Lonsdale (${true_optimal_cost:.2f})")
            print(f"• Reflect on why that happened!")
            print()
    except Exception as e:
        print(f"Error: {e}")

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