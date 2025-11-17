"""
Part A: Dijkstra Algorithm for Different Stakeholders 

This file focuses on implementing Dijkstra's algorithm from company and driver's different perspectives

You should implement basic dijkstra algorithms and their helper functions here.
Start from PART A: DIJKSTRA ALGORITHM FOR DIFFERENT PARTIES,
Come back to implement HELPER FUNCTIONS if instructed to do so
"""

import heapq
from typing import List, Tuple
from main import Node, Edge, get_neighbors



# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_company_cost(from_node: Node, to_node: Node) -> float:
    """
    Calculate the company's cost for traveling from one node to another.
    
    Total Company cost = Platform costs per ride + mileage * driver base pay per mile
    
    Args:
        from_node (Node): Starting city
        to_node (Node): Destination city
        
    Returns:
        float: Total cost from company's perspective
        
    TODO: Implement this helper function when asked.
    """
    # START YOUR IMPLEMENTATION HERE
    
    # Hints:
    # - Get distance using: distance = from_node.distance_to(to_node)
    # - Average Platform cost of both cities
    # - Driver base pay per mile = $0.60 (what company pays driver)
    # - Effective_distance = distance * the higher traffic_level from 2 cities
    # - Mileage cost = effective_distance * driver_base_pay_per_mile
    # - Return: total cost
    
    raise NotImplementedError("calculate_company_cost not yet implemented - implement this helper function first!")
    
    # END YOUR IMPLEMENTATION


def calculate_driver_cost(from_node: Node, to_node: Node) -> float:
    """
    Calculate the driver's cost for traveling from one node to another.
    
    Total Driver cost = mileage * fuel per mile + parking + maintenance
    
    Args:
        from_node (Node): Starting city
        to_node (Node): Destination city
        
    Returns:
        float: Total cost from driver's perspective
        
    TODO: Implement this helper function when asked.
    """
    # START YOUR IMPLEMENTATION HERE
    
    # Hints:
    # - Get distance using: distance = from_node.distance_to(to_node)
    # - Average fuel_cost_per_mile of both cities
    # - Pick Higher Traffic factor from 2 cities
    # - Fuel cost = distance * avg_fuel_cost_per_mile * traffic_factor
    # - Parking cost = to_node.parking_cost
    # - Average maintenance_factor of both cities
    # - Maintenance cost = distance * 0.10 * avg_maintenance_factor  # Base $0.10 per mile
    # - Return: total cost
    
    raise NotImplementedError("calculate_driver_cost not yet implemented - implement this helper function first!")
    
    # END YOUR IMPLEMENTATION


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
    
    TODO: Implement this function
    """
    # START YOUR IMPLEMENTATION HERE
    
    # Hints:
    # - Review your notes from day 3 for algorithm steps
    # - First implement calculate_company_cost() helper function above!
    # - Use float('inf') for infinity
    # - Use heapq.heappush() and heapq.heappop() for priority queue
    # - Priority queue stores tuples: (distance, node)
    # - Use get_neighbors(node, edges) to find connected cities (helper function in main)
    # - Use calculate_company_cost(from_node, to_node) for edge weights
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
        
    TODO: Implement this function (similar structure to Part A①)
    """
    # START YOUR IMPLEMENTATION HERE
    
    # Hints:
    # - First implement calculate_driver_cost() helper function above!
    # - Same Dijkstra algorithm structure
    # - Use calculate_driver_cost(from_node, to_node) instead
    
    raise NotImplementedError("Part A2 (Driver Dijkstra) not yet implemented")
    
    # END YOUR IMPLEMENTATION




# ============================================================================
# RUN FUNCTIONS
# ============================================================================

def run_part_a():
    """
    Run Part A implementations with Minnesota data.
    """
    try:
        from mn_dataset import MN_NODES_DICT, MN_EDGES
        
        print("=" * 80)
        print("PART A: COMPANY VS DRIVER ALGORITHM COMPARISON")

        # Run with diverse start/destination pairs
        test_routes = [
            ("Edina", "Northfield"),      
            ("Minneapolis", "Stillwater")
        ]
        
        for start_name, dest_name in test_routes:
            if start_name not in MN_NODES_DICT or dest_name not in MN_NODES_DICT:
                continue
                
            start_city = MN_NODES_DICT[start_name]
            destination = MN_NODES_DICT[dest_name]
            print(f"\nRoute from {start_city.name} to {destination.name}:")
            print("-" * 50)
            
            # Run Part A1 - Company
            try:
                company_path, company_cost = dijkstra_company_route(start_city, destination, list(MN_NODES_DICT.values()), MN_EDGES)
                print(f"Company algorithm: {' -> '.join([node.name for node in company_path])}")
                print(f"Company cost: ${company_cost:.2f}")
                    
            except NotImplementedError:
                print("Company algorithm: Not yet implemented")
            except Exception as e:
                print(f"Company algorithm error: {e}")
            
            # Run Part A2 - Driver's algorithm  
            try:
                driver_path, driver_cost = dijkstra_driver_route(start_city, destination, list(MN_NODES_DICT.values()), MN_EDGES)
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
    
    # Load dataset
    try:
        from mn_dataset import MN_NODES_DICT, MN_EDGES
    except ImportError:
        print("Error: Could not load Minnesota dataset")
    
    # Run tests
    run_part_a()


if __name__ == "__main__":
    main()
