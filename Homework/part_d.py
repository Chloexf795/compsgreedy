"""
Part D: Ethical Algorithm Modifications

This file explores how ethical considerations can be integrated into algorithmic decision-making.

You will implement ONE of the modifications:
- Driver fatigue and safety considerations
- Rural accessibility and fairness
- Weather-based safety prioritization

You should copy and modify dijkstra algorithm from A1(company).
"""

import heapq
from typing import List, Tuple
from main import Node, Edge, get_neighbors
from part_a import calculate_company_cost


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
    # - The calculate_company_cost function is imported from part_a 
    # - Track consecutive long drives in your algorithm state
    # - A "long drive" is ≥10 miles between cities (use node.distance_to(neighbor))
    # - Add penalty: $50 for consecutive long drives, $15 for any long drive
    # - Use max() to ensure costs never go negative
    # - You might need to modify the algorithm to track path history
    
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
    # - The calculate_company_cost function is imported from part_a
    # - Implement rural subsidy yourself: reduce cost by $8.00 for trips TO rural destinations
    # - Check if destination node has node.region == "rural"
    # - Apply subsidy: subsidized_cost = max(0.1, original_cost - 8.0)
    # - Use max() to ensure costs never go negative
    # - This subsidy is large enough to change optimal paths but maintains positive costs (Why?)
    
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
    # - The calculate_company_cost function is imported from part_a
    # - Implement weather penalty yourself for each edge cost calculation
    # - Check weather conditions: from_node.weather_condition and to_node.weather_condition
    # - Apply penalty multipliers based on WORST weather on the route:
    #   * 'storm': 5.0x penalty (severe safety risk)
    #   * 'snow': 3.5x penalty (high safety risk)  
    #   * 'rain': 2.0x penalty (moderate safety risk)
    #   * 'clear': 1.0x (no penalty)
    # - Formula: penalized_cost = original_cost * penalty_multiplier
    # - Use conditions like: if 'storm' in [from_node.weather_condition, to_node.weather_condition]
    # - Use max() to ensure costs never go negative
    
    raise NotImplementedError("Part D3 (Weather Safety) not yet implemented - choose one ethical rule to implement")
    
    # END YOUR IMPLEMENTATION


# ============================================================================
# RUN FUNCTIONS
# ============================================================================

def run_part_d():
    """
    Run Part D to test ethical algorithm modifications
    """
    print("Dijkstra Algorithm Assignment - Part D: Ethical Algorithm Modifications")
    print("=" * 80)
    
    try:
        from mn_dataset import MN_NODES_DICT, MN_EDGES
        
        print("PART D: ETHICAL ALGORITHM MODIFICATIONS")        
        # run with route Edina to Forest Lake
        start_city = MN_NODES_DICT["Edina"]
        destination = MN_NODES_DICT["Forest Lake"]
        
        print(f"\nTesting ethical modifications on route: {start_city.name} to {destination.name}")
        print(f"\n" + "-"*60)
        
        # Get baseline for comparison
        try:
            # Import company route from Part A for comparison
            from part_a import dijkstra_company_route
            
            baseline_path, baseline_cost = dijkstra_company_route(start_city, destination, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"BASELINE (Company Route):")
            print(f"  Route: {' -> '.join([node.name for node in baseline_path])}")
            print(f"  Cost: ${baseline_cost:.2f}")
            
        except Exception as e:
            print(f"Error getting baseline: {e}")
            baseline_path, baseline_cost = [], 0.0
        
        # Run Fatigue Consideration
        print(f"\n" + "-"*60)
        print(f"FATIGUE CONSIDERATION (Option 1):")
        try:
            fatigue_path, fatigue_cost = dijkstra_with_fatigue_consideration(start_city, destination, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"MODIFIED Route: {' -> '.join([node.name for node in fatigue_path])}")
        except NotImplementedError:
            print(" Fatigue consideration not implemented")
        except Exception as e:
            print(f" Error: {e}")
        
        # Run Fairness Consideration
        print(f"\n" + "-"*60)
        print(f"FAIRNESS CONSIDERATION (Option 2):")
        try:
            fairness_path, fairness_cost = dijkstra_with_fairness_consideration(start_city, destination, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"MODIFIED Route: {' -> '.join([node.name for node in fairness_path])}")
            print(f"MODIFIED Cost: ${fairness_cost:.2f}")
            
        except NotImplementedError:
            print("Fairness consideration not implemented")
        except Exception as e:
            print(f"Error: {e}")
        
        # Run Weather Safety
        print(f"\n" + "-"*60)
        print(f"WEATHER SAFETY CONSIDERATION (Option 3):")
        try:
            weather_path, weather_cost = dijkstra_with_weather_safety(start_city, destination, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"MODIFIED Route: {' -> '.join([node.name for node in weather_path])}")
            print(f"MODIFIED Cost: ${weather_cost:.2f}")
         
        except NotImplementedError:
            print("Weather safety not implemented")
        except Exception as e:
            print(f"Error: {e}")
            
    except ImportError:
        print("Error: Could not import Minnesota dataset")
    except Exception as e:
        print(f"Error in Part D testing: {e}")


def main():
    """
    Main function to run Part D tests
    """
    run_part_d()


if __name__ == "__main__":
    main()