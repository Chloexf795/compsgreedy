"""
Part B: Northfield Subsidies! 

This file explores what happens when Dijkstra's algorithm encounters negative edge weights.

You should copy and modify dijkstra algorithm from A2(driver).

You should run Part B by running this file directly
"""

import heapq
from typing import List, Tuple
from main import Node, Edge, get_neighbors
from part_a import calculate_driver_cost


# ============================================================================
# PART B: NORTHFIELD SUBSIDIES - NEGATIVE EDGE WEIGHTS
# ============================================================================

def dijkstra_with_northfield_subsidy(start: Node, target: Node, nodes: List[Node], edges: List[Edge]) -> Tuple[List[Node], float]:
    """
    Part B: Investigate Dijkstra with negative edge weights (Northfield subsidies).
    
    Args:
        start (Node): Starting city
        target (Node): Destination city
        nodes (List[Node]): All cities in the network  
        edges (List[Edge]): All road connections
        
    Returns:
        Tuple[List[Node], float]: (shortest path, total cost)
        
    TODO: Implement and observe what happens with negative weights
    """
    # START YOUR IMPLEMENTATION HERE
    
    # Hints:
    # - Copy your dijkstra_driver_route implementation from Part A2 Drivers
    # - The calculate_driver_cost function is imported from part_a (your implementation)
    # - Modify the cost calculation: if from_node.id == "Lakeville" and to_node.id == "Northfield": cost = -20.0
    # - Otherwise use normal cost = calculate_driver_cost(from_node, to_node)
    # - This will be tested with Northfield destination to see if algorithm chooses different paths
    # - Run this and observe if the subsidy changes the route selection
    
    raise NotImplementedError("Part B (Northfield Subsidy) not yet implemented")
    
    # END YOUR IMPLEMENTATION


# ============================================================================
# RUN FUNCTIONS
# ============================================================================

def run_part_b():
    """
    Demonstrate the issues with negative weights in Dijkstra's algorithm.
    """
    try:
        from mn_dataset import MN_NODES_DICT, MN_EDGES
        from part_a import dijkstra_driver_route
        
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
    Main function for Part B solution testing.
    """
    print("Dijkstra Algorithm Assignment - Part B Solution Testing")
    
    # Load dataset info
    try:
        from mn_dataset import MN_NODES_DICT, MN_EDGES
        print(f"Minnesota rideshare network: {len(MN_NODES_DICT)} cities, {len(MN_EDGES)} connections")
    except ImportError:
        print("Error: Could not load Minnesota dataset")
        return
    
    # Run analysis
    run_part_b()


if __name__ == "__main__":
    main()
