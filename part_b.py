"""
Part B: Northfield Subsidies! 

This file explores what happens when Dijkstra's algorithm encounters negative edge weights.

You should copy and modify dijkstra algorithm from A2.
"""

import heapq
from typing import List, Tuple
from main import Node, Edge, calculate_driver_cost, get_neighbors


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
        
    TODO: Students implement and observe what happens with negative weights
    """
    # START YOUR IMPLEMENTATION HERE
    
    # Hints:
    # - Copy your dijkstra_driver_route implementation from Part A2 Drivers
    # - Modify the cost calculation: if from_node.id == "Lakeville" and to_node.id == "Northfield": cost = -100.0
    # - will be tested with Lonsdale destination to see if algorithm chooses different paths
    # - Run this and observe the results and finish the reflection.
    
    raise NotImplementedError("Part B (Northfield Subsidy) not yet implemented")
    
    # END YOUR IMPLEMENTATION


# ============================================================================
# RUN FUNCTIONS
# ============================================================================

def run_part_b():
    """
    Run Part B - Northfield subsidy investigation.
    """
    try:
        from mn_dataset import MN_NODES_DICT, MN_EDGES, START_CITY
        
        print("=" * 80)
        print("PART B: NORTHFIELD SUBSIDY INVESTIGATION")
        
        northfield = MN_NODES_DICT["Northfield"]
        lonsdale = MN_NODES_DICT["Lonsdale"]
        
        print(f"Run route from {START_CITY.name} to {lonsdale.name}")
        print(f"Subsidy rule: Trip from Lakeville to Northfield costs -$100.00")
        print("-" * 70)
        
        try:
            # Import driver route from Part A for comparison
            try:
                from part_a import dijkstra_driver_route
            except ImportError:
                print("Error: Could not import driver route implementation")
                return
            
            # Run regular driver route
            regular_path, regular_cost = dijkstra_driver_route(START_CITY, lonsdale, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"Regular driver route: {' -> '.join([node.name for node in regular_path])}")
            print(f"Regular driver cost: ${regular_cost:.2f}")
            
            # Run subsidized route
            subsidy_path, subsidy_cost = dijkstra_with_northfield_subsidy(START_CITY, lonsdale, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"\nSubsidized route: {' -> '.join([node.name for node in subsidy_path])}")
            print(f"Subsidized cost: ${subsidy_cost:.2f}")
          
            print(f"\nCost difference: ${regular_cost - subsidy_cost:.2f}")     
        except NotImplementedError:
            print("Part B not yet implemented")

            
    except ImportError:
        print("Error: Could not import Minnesota dataset")
    except Exception as e:
        print(f"Error in Part B testing: {e}")


def main():
    """
    Main function for Part B.
    """
    # Load and display dataset info
    try:
        from mn_dataset import MN_NODES_DICT, MN_EDGES, START_CITY
    except ImportError:
        print("Error: Could not load Minnesota dataset")
    
    # Run tests
    run_part_b()


if __name__ == "__main__":
    main()
