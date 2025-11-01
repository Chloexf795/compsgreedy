"""
Part D: Ethical Algorithm Modifications - Solution

This file explores how ethical considerations can be integrated into algorithmic decision-making.

You will implement ONE modifications:
- Driver fatigue and safety considerations
- Rural accessibility and fairness
- Weather-based safety prioritization

Complete implementation for Instructors
"""

import heapq
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Tuple
from main import Node, Edge, calculate_company_cost, apply_weather_penalty, apply_rural_subsidy, get_neighbors


# ============================================================================
# PART D: ETHICAL ALGORITHM COMPLETE IMPLEMENTATIONS

# ALL implemented below!
# ============================================================================

def dijkstra_with_fatigue_consideration(start: Node, target: Node, nodes: List[Node], edges: List[Edge]) -> Tuple[List[Node], float]:
    """
    Option 1: Complete Fatigue Rule Implementation
    """
    # We need to track path history for fatigue calculation
    # State: (node, previous_drive_was_long)
    # distances[(node, was_long)] = minimum cost to reach node with given long-drive state
    
    distances = {}
    previous = {}
    
    # Initialize for start node (both states)
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
            # Calculate base cost
            base_cost = calculate_company_cost(current_node, neighbor)
            
            # Check if this drive is long (≥10 miles) - lowered threshold
            drive_distance = current_node.distance_to(neighbor)
            this_drive_is_long = drive_distance >= 10.0
            
            # Apply fatigue penalty for consecutive long drives
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
            from solutions.part_a_solution import dijkstra_company_route
            
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
            if baseline_path and fatigue_path != baseline_path:
                print("✓ Fatigue consideration changed the route!")
            elif baseline_path:
                print(f"Same route, but cost increased by ${fatigue_cost - baseline_cost:.2f}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Run Fairness Consideration
        print(f"\nFAIRNESS CONSIDERATION:")
        try:
            fairness_path, fairness_cost = dijkstra_with_fairness_consideration(start_city, destination, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"Fairness-aware route: {' -> '.join([node.name for node in fairness_path])}")
            print(f"Cost with rural subsidies: ${fairness_cost:.2f}")
            if baseline_path and fairness_path != baseline_path:
                print("✓ Fairness consideration changed the route!")
            elif baseline_path:
                print(f"Same route, but cost decreased by ${baseline_cost - fairness_cost:.2f}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Run Weather Safety
        print(f"\nWEATHER SAFETY CONSIDERATION:")
        try:
            weather_path, weather_cost = dijkstra_with_weather_safety(start_city, destination, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"Weather-safe route: {' -> '.join([node.name for node in weather_path])}")
            print(f"Cost with weather penalties: ${weather_cost:.2f}")
            if baseline_path and weather_path != baseline_path:
                print("✓ Weather safety changed the route!")
            elif baseline_path:
                print(f"Same route, but cost increased by ${weather_cost - baseline_cost:.2f}")
        except Exception as e:
            print(f"Error: {e}")
            
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
