"""
Solutions for Dijkstra Algorithm Assignment - Part D: Ethical Algorithm Modifications

This file contains complete implementations for all Part D functions with
ethical considerations including fatigue, fairness, and weather safety.

Author: Course Solutions
"""

import heapq
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from typing import List, Tuple
from main import Node, Edge, get_neighbors
from solutions.part_a_solution import calculate_company_cost


# ============================================================================
# Helper Functions for Part D Ethical Modifications
# ============================================================================

def apply_rural_subsidy(base_cost: float, destination: Node, subsidy_amount: float = 8.0) -> float:
    """
    Apply rural subsidy to reduce transportation costs for rural destinations.
    
    Args:
        base_cost: The original cost of the trip
        destination: The destination node
        subsidy_amount: The amount of subsidy to apply (default $8.00)
        
    Returns:
        Modified cost with subsidy applied (minimum $0.50 to prevent negative costs)
    """
    if destination.region == "rural":
        subsidized_cost = base_cost - subsidy_amount
        return max(0.50, subsidized_cost)  # Ensure minimum cost
    return base_cost


def apply_weather_penalty(base_cost: float, current: Node, destination: Node) -> float:
    """
    Apply weather-based penalties for safety considerations.
    
    Args:
        base_cost: The original cost of the trip
        current: The current node
        destination: The destination node
        
    Returns:
        Modified cost with weather penalties applied
    """
    # Apply penalty based on destination weather conditions
    weather_multiplier = 1.0
    
    if destination.weather_condition == "storm":
        weather_multiplier = 5.0  # Very dangerous - high penalty
    elif destination.weather_condition == "snow":
        weather_multiplier = 3.5  # Dangerous - moderate penalty  
    elif destination.weather_condition == "rain":
        weather_multiplier = 2.0  # Somewhat dangerous - light penalty
    
    return base_cost * weather_multiplier


# ============================================================================
# Part D Algorithm Implementations
# ============================================================================

def dijkstra_with_fatigue_consideration(start: Node, target: Node, nodes: List[Node], edges: List[Edge]) -> Tuple[List[Node], float]:
    """
    Option 1: Complete Fatigue Rule Implementation
    
    Tracks driver fatigue by monitoring consecutive long drives and applying penalties:
    - $15 penalty for any long drive (≥10 miles)
    - $50 additional penalty for consecutive long drives
    """
    # We need to track path history for fatigue calculation
    # State: (node, previous_drive_was_long)
    distances = {}
    previous = {}
    
    # Initialize for all nodes and both fatigue states
    for was_long in [False, True]:
        for node in nodes:
            distances[(node, was_long)] = float('inf')
            previous[(node, was_long)] = None
    
    distances[(start, False)] = 0.0
    
    # Priority queue: (distance, node, previous_was_long)
    pq = [(0.0, start, False)]
    visited = set()
    
    while pq:
        current_dist, current_node, prev_was_long = heapq.heappop(pq)
        
        state = (current_node, prev_was_long)
        if state in visited:
            continue
            
        visited.add(state)
        
        # Check all neighbors
        neighbors = get_neighbors(current_node, edges)
        for neighbor in neighbors:
            # Calculate base cost using company perspective
            base_cost = calculate_company_cost(current_node, neighbor)
            
            # Check if this drive is long (≥10 miles)
            drive_distance = current_node.distance_to(neighbor)
            this_drive_is_long = drive_distance >= 10.0
            
            # Apply fatigue penalty
            edge_cost = base_cost
            if prev_was_long and this_drive_is_long:
                edge_cost += 50.0  # $50 penalty for consecutive long drives
            elif this_drive_is_long:
                edge_cost += 15.0  # $15 penalty for any long drive
                
            new_distance = current_dist + edge_cost
            
            # Update if shorter path found
            new_state = (neighbor, this_drive_is_long)
            if new_distance < distances.get(new_state, float('inf')):
                distances[new_state] = new_distance
                previous[new_state] = (current_node, prev_was_long)
                heapq.heappush(pq, (new_distance, neighbor, this_drive_is_long))
    
    # Find best path to target (either ending state)
    best_cost = float('inf')
    best_ending_state = None
    
    for was_long in [False, True]:
        state = (target, was_long)
        if distances.get(state, float('inf')) < best_cost:
            best_cost = distances[state]
            best_ending_state = state
    
    # Reconstruct path
    if best_ending_state is None or best_cost == float('inf'):
        return [], float('inf')
    
    path = []
    current_state = best_ending_state
    
    while current_state is not None:
        node, _ = current_state
        path.append(node)
        current_state = previous.get(current_state)
    
    path.reverse()
    return path, best_cost


def dijkstra_with_fairness_consideration(start: Node, target: Node, nodes: List[Node], edges: List[Edge]) -> Tuple[List[Node], float]:
    """
    Option 2: Complete Fairness Rule Implementation
    
    Applies rural subsidies to ensure equitable transportation access.
    Uses $8.00 subsidy for rural destinations (minimum cost $0.50).
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
                
            # Calculate base cost using company perspective
            base_cost = calculate_company_cost(current_node, neighbor)
            
            # Apply rural subsidy (reduces cost by $8.0 for rural destinations)
            edge_cost = apply_rural_subsidy(base_cost, neighbor, subsidy_amount=8.0)
            
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


def dijkstra_with_weather_safety(start: Node, target: Node, nodes: List[Node], edges: List[Edge]) -> Tuple[List[Node], float]:
    """
    Option 3: Complete Weather Safety Rule Implementation
    
    Applies weather-based penalties to prioritize safety:
    - Storm: 5x cost multiplier
    - Snow: 3.5x cost multiplier  
    - Rain: 2x cost multiplier
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
                
            # Calculate base cost using company perspective
            base_cost = calculate_company_cost(current_node, neighbor)
            
            # Apply weather penalty based on weather conditions
            edge_cost = apply_weather_penalty(base_cost, current_node, neighbor)
            
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


def run_part_d():
    """
    Run Part D to test ethical algorithm modifications
    """
    print("Dijkstra Algorithm Assignment - Part D: Ethical Algorithm Modifications")
    print("=" * 80)
    
    try:
        from mn_dataset import MN_NODES_DICT, MN_EDGES
        
        print("PART D: ETHICAL ALGORITHM MODIFICATIONS")        
        # run route for ethical considerations: Edina to Forest Lake
        start_city = MN_NODES_DICT["Edina"]
        destination = MN_NODES_DICT["Forest Lake"]
        
        print(f"\nTesting ethical modifications on route: {start_city.name} to {destination.name}")
        print(f"\n" + ""*60)
        
        # Get baseline for comparison
        try:
            # Import company route from Part A for comparison
            from solutions.part_a_solution import dijkstra_company_route
            
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
            print(f"MODIFIED Cost: ${fatigue_cost:.2f}")
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