"""
Part B: Northfield Subsidies! - Solution

This file explores what happens when Dijkstra's algorithm encounters negative edge weights.

Complete implementation for Instructors
"""
import heapq
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Tuple
from main import Node, Edge, calculate_driver_cost, get_neighbors


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
        
        # Found target - we can stop early
        if current_node == target:
            break
            
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
# ANALYSIS FUNCTIONS
# ============================================================================

def demonstrate_negative_weight_problem():
    """
    Demonstrate the issues with negative weights in Dijkstra's algorithm.
    """
    try:
        from mn_dataset import MN_NODES_DICT, MN_EDGES, START_CITY
        from solutions.part_a_solution import dijkstra_driver_route
        
        print("=" * 80)
        print("PART B ANALYSIS: Negative Edge Weights Problem")
        
        # Test: Route to Lonsdale (through Northfield chain)
        lonsdale = MN_NODES_DICT["Lonsdale"]
        print(f"\nRun routes from {START_CITY.name} to {lonsdale.name}")
        print("Subsidy rule: Lakeville to Northfield costs -$100.00")
        print("-" * 60)
        
        regular_path, regular_cost = dijkstra_driver_route(START_CITY, lonsdale, list(MN_NODES_DICT.values()), MN_EDGES)
        subsidy_path, subsidy_cost = dijkstra_with_northfield_subsidy(START_CITY, lonsdale, list(MN_NODES_DICT.values()), MN_EDGES)
        
        print(f"Regular: {' -> '.join([node.name for node in regular_path])} (${regular_cost:.2f})")
        print(f"Subsidy: {' -> '.join([node.name for node in subsidy_path])} (${subsidy_cost:.2f})")
        print(f"{'='*80}")
    
    except Exception as e:
        print(f"Error in negative weight demonstration: {e}")


def main():
    """
    Main function for Part B solution testing.
    """
    print("Dijkstra Algorithm Assignment - Part B Solution Testing")
    
    # Load dataset info
    try:
        from mn_dataset import MN_NODES_DICT, MN_EDGES, START_CITY
        print(f"Minnesota rideshare network: {len(MN_NODES_DICT)} cities, {len(MN_EDGES)} connections")
    except ImportError:
        print("Error: Could not load Minnesota dataset")
        return
    
    # Run analysis
    demonstrate_negative_weight_problem()


if __name__ == "__main__":
    main()
