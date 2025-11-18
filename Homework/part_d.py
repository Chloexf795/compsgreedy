"""
Part D: Ethical Algorithm Modifications

This file explores how ethical considerations can be integrated into algorithmic decision-making.

You will implement ONE of the modifications:
- Driver fatigue and safety considerations
- Rural accessibility and fairness
- Weather-based safety prioritization

You should copy and modify dijkstra algorithm from A1(company).

You Should Run Part D with combined_run.py
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

