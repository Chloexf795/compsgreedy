"""
Part D: Ethical Algorithm Modifications

This file explores how ethical considerations can be integrated into algorithmic decision-making.

You will implement ONE modifications:
- Driver fatigue and safety considerations
- Rural accessibility and fairness
- Weather-based safety prioritization

You should copy and modify dijkstra algorithm from A1.
"""

import heapq
from typing import List, Tuple
from main import Node, Edge, calculate_company_cost, apply_weather_penalty, apply_rural_subsidy, get_neighbors


# ============================================================================
# PART D: ETHICAL ALGORITHM MODIFICATIONS

# ONlY choose ONE to implement!
# ============================================================================

def dijkstra_with_fatigue_consideration(start: Node, target: Node, nodes: List[Node], edges: List[Edge]) -> Tuple[List[Node], float]:
    """
    Option 1: Fatigue Rule
    
    Modify the company algorithm to limit consecutive long-distance drives for safety.
    Add penalties for routes with too many consecutive long drives (≥10 miles).
    
    Args:
        start (Node): Starting city
        target (Node): Destination city
        nodes (List[Node]): All cities in the network
        edges (List[Edge]): All road connections
        
    Returns:
        Tuple[List[Node], float]: (ethical path, total cost with penalties)
        
    TODO: Students implement ONE ethical rule (choose this OR fairness OR weather)
    """
    # START YOUR IMPLEMENTATION HERE
    
    # Hints:
    # - Start with your dijkstra_company_route as base 
    # - Track consecutive long drives in your algorithm state
    # - A "long drive" is ≥10 miles between cities (use node.distance_to(neighbor))
    # - Add penalty: $50 for consecutive long drives, $15 for any long drive
    # - You might need to modify the algorithm to track path history
    # - Consider using state: (node, previous_drive_was_long) in your distances dict
    
    raise NotImplementedError("Part D (Fatigue) not yet implemented - choose one ethical rule to implement")
    
    # END YOUR IMPLEMENTATION


def dijkstra_with_fairness_consideration(start: Node, target: Node, nodes: List[Node], edges: List[Edge]) -> Tuple[List[Node], float]:
    """
    Option 2: Fairness Rule
    
    Modify the company algorithm to provide subsidies for rural regions
    to ensure equitable service without making costs negative.
    
    Args:
        start (Node): Starting city
        target (Node): Destination city
        nodes (List[Node]): All cities in the network
        edges (List[Edge]): All road connections
        
    Returns:
        Tuple[List[Node], float]: (ethical path, total cost with subsidies)
        
    TODO: implement ONE ethical rule (choose this OR fatigue OR weather)
    """
    # START YOUR IMPLEMENTATION HERE
    
    # Hints:
    # - Start with your dijkstra_company_route as base
    # - Use apply_rural_subsidy(cost, to_node, subsidy_amount=8.0) for rural destinations (helper function in main)
    # - This reduces cost by $8.00 for trips to rural areas
    # - Subsidy is large enough to change paths but won't create negative costs
    # - Rural regions are marked as node.region == "rural"
    
    raise NotImplementedError("Part D (Fairness) not yet implemented - choose one ethical rule to implement")
    
    # END YOUR IMPLEMENTATION


def dijkstra_with_weather_safety(start: Node, target: Node, nodes: List[Node], edges: List[Edge]) -> Tuple[List[Node], float]:
    """
    Option 3: Weather Safety Consideration
    
    Modify the company algorithm to add penalties for dangerous weather conditions
    to prioritize driver and passenger safety.
    
    Args:
        start (Node): Starting city
        target (Node): Destination city
        nodes (List[Node]): All cities in the network
        edges (List[Edge]): All road connections
        
    Returns:
        Tuple[List[Node], float]: (safe path, total cost with weather penalties)
        
    TODO: implement ONE ethical rule (choose this OR fatigue OR fairness)
    """
    # START YOUR IMPLEMENTATION HERE
    
    # Hints:
    # - Start with your dijkstra_company_route as base
    # - Use apply_weather_penalty(cost, from_node, to_node) for each edge. (helper function in main)
    # - This increases cost for routes through storms (5x), snow (3.5x), rain (2x)
    # - Weather conditions are stored in node.weather_condition
    
    raise NotImplementedError("Part D3 (Weather Safety) not yet implemented - choose one ethical rule to implement")
    
    # END YOUR IMPLEMENTATION


# ============================================================================
# RUN FUNCTIONS
# ============================================================================

def run_part_d():
    """
    Test Part D - Ethical algorithm modifications.
    """
    try:
        from mn_dataset import MN_NODES_DICT, MN_EDGES, START_CITY
        
        print("=" * 80)
        print("PART D: ETHICAL ALGORITHM MODIFICATIONS")        
        # run route for ethical considerations: Edina to Forest Lake
        start_city = MN_NODES_DICT["Edina"]
        destination = MN_NODES_DICT["Forest Lake"]
        
        print(f"\nTesting ethical modifications on route: {start_city.name} to {destination.name}")
        print(f"Route type: {start_city.region} to {destination.region}")
        print(f"Destination weather: {destination.weather_condition}")
        print("-" * 80)
        
        # Get baseline for comparison
        try:
            # Import company route from Part A for comparison
            try:
                from part_a import dijkstra_company_route
            except ImportError:
                  print("Error: Could not import company route implementation")
                  return                    
            
            baseline_path, baseline_cost = dijkstra_company_route(start_city, destination, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"Company(base): {' -> '.join([node.name for node in baseline_path])} (${baseline_cost:.2f})")
            
        except Exception as e:
            print(f"Error getting baseline: {e}")
            baseline_path, baseline_cost = [], 0.0
        
        # Run Fatigue Consideration
        print(f"\nFATIGUE CONSIDERATION:")
        try:
            fatigue_path, fatigue_cost = dijkstra_with_fatigue_consideration(start_city, destination, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"Fatigue-aware route: {' -> '.join([node.name for node in fatigue_path])}")
            print(f"Cost with fatigue penalties: ${fatigue_cost:.2f}")
        except NotImplementedError:
            print("Fatigue consideration not implemented")
        except Exception as e:
            print(f"Error: {e}")
        
        # Run Fairness Consideration
        print(f"\nFAIRNESS CONSIDERATION:")
        try:
            fairness_path, fairness_cost = dijkstra_with_fairness_consideration(start_city, destination, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"Fairness-aware route: {' -> '.join([node.name for node in fairness_path])}")
            print(f"Cost with rural subsidies: ${fairness_cost:.2f}")
        except NotImplementedError:
            print("Fairness consideration not implemented")
        
        # Run Weather Safety
        print(f"\nWEATHER SAFETY CONSIDERATION:")
        try:
            weather_path, weather_cost = dijkstra_with_weather_safety(start_city, destination, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"Weather-safe route: {' -> '.join([node.name for node in weather_path])}")
            print(f"Cost with weather penalties: ${weather_cost:.2f}")
        except NotImplementedError:
            print("Weather safety not implemented")
            
    except ImportError:
        print("Error: Could not import Minnesota dataset")
    except Exception as e:
        print(f"Error in Part D testing: {e}")


def main():
    """
    Main function for Part D testing.
    """
    print("Dijkstra Algorithm Assignment - Part D: Ethical Algorithm Modifications")
    
    # Load and display dataset info
    try:
        from mn_dataset import MN_NODES_DICT, MN_EDGES, START_CITY
        rural_cities = [node.name for node in MN_NODES_DICT.values() if node.region == "rural"]
        stormy_cities = [node.name for node in MN_NODES_DICT.values() if node.weather_condition != "clear"]

    except ImportError:
        print("Error: Could not load Minnesota dataset")
    
    # Run tests
    run_part_d()


if __name__ == "__main__":
    main()
