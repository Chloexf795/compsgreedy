"""
Part A: Dijkstra Algorithm for Different Parties

This file focuses on implementing Dijkstra's algorithm from company and driver's different perspectives

You should implement basic dijkstra algorithms here.
"""

import heapq
from typing import List, Tuple
from main import Node, Edge, calculate_company_cost, calculate_driver_cost, get_neighbors


# ============================================================================
# PART A: DIJKSTRA ALGORITHM FOR DIFFERENT PARTIES
# ============================================================================

def dijkstra_company_route(start: Node, target: Node, nodes: List[Node], edges: List[Edge]) -> Tuple[List[Node], float]:
    """
    Part A1: Implement Dijkstra's algorithm from the company's perspective.
    
    Goal: Find the minimum cost route where cost = Platform costs + mileage * driver base pay
    
    Args:
        start (Node): Starting city (where driver currently is)
        target (Node): Destination city (where passenger wants to go)
        nodes (List[Node]): All cities in the network
        edges (List[Edge]): All road connections
        
    Returns:
        Tuple[List[Node], float]: (shortest path as list of nodes, total cost)
        
    Algorithm Steps (Dijkstra's Algorithm):
    1. Initialize distances: start=0, all others=infinity
    2. Use a min-priority queue (heapq) to track unvisited nodes
    3. While queue is not empty:
       a. Pop node u with minimum distance
       b. If u is the target, we're done
       c. For each neighbor v of u:
          - Calculate newDist = dist[u] + cost(u, v) using calculate_company_cost
          - If newDist < dist[v], update dist[v] and previous[v]
    4. Reconstruct path from target back to start using previous pointers
    
    TODO: Students implement this function
    """
    # START YOUR IMPLEMENTATION HERE
    
    # Hints:
    # - Use float('inf') for infinity
    # - Use heapq.heappush() and heapq.heappop() for priority queue
    # - Priority queue stores tuples: (distance, node)
    # - Use get_neighbors(node, edges) to find connected cities (helper function in main)
    # - Use calculate_company_cost(from_node, to_node) for edge weights (helper function in main)
    # - Keep track of previous nodes to reconstruct the path
    # - Handle the case where target is unreachable
    
    raise NotImplementedError("Part A1 (Company Dijkstra) not yet implemented")
    
    # END YOUR IMPLEMENTATION


def dijkstra_driver_route(start: Node, target: Node, nodes: List[Node], edges: List[Edge]) -> Tuple[List[Node], float]:
    """
    Part A2: Implement Dijkstra's algorithm from the driver's perspective.
    
    Goal: Find the minimum cost route where cost = mileage * fuel + parking + maintenance
    
    Args:
        start (Node): Starting city
        target (Node): Destination city  
        nodes (List[Node]): All cities in the network
        edges (List[Edge]): All road connections
        
    Returns:
        Tuple[List[Node], float]: (shortest path as list of nodes, total cost)
        
    TODO: Students implement this function (similar structure to Part A①)
    """
    # START YOUR IMPLEMENTATION HERE
    
    # Hints:
    # - Very similar to dijkstra_company_route above
    # - Main difference: use calculate_driver_cost(from_node, to_node) instead
    # - Same Dijkstra algorithm structure
    
    raise NotImplementedError("Part A2 (Driver Dijkstra) not yet implemented")
    
    # END YOUR IMPLEMENTATION


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
            
            # Run Part A1 - Company
            try:
                company_path, company_cost = dijkstra_company_route(START_CITY, destination, list(MN_NODES_DICT.values()), MN_EDGES)
                print(f"Company algorithm: {' -> '.join([node.name for node in company_path])}")
                print(f"Company cost: ${company_cost:.2f}")
                    
            except NotImplementedError:
                print("Company algorithm: Not yet implemented")
            except Exception as e:
                print(f"Company algorithm error: {e}")
            
            # Run Part A2 - Driver's algorithm  
            try:
                driver_path, driver_cost = dijkstra_driver_route(START_CITY, destination, list(MN_NODES_DICT.values()), MN_EDGES)
                print(f"Driver algorithm: {' -> '.join([node.name for node in driver_path])}")
                print(f"Driver cost: ${driver_cost:.2f}")
                    
            except NotImplementedError:
                print("Driver algorithm: Not yet implemented")
            except Exception as e:
                print(f"Driver algorithm error: {e}")

                
    except ImportError:
        print("Error: Could not import Minnesota dataset")
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
