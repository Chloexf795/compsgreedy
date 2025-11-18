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
# HELPER FUNCTIONS COMPLETE IMPLEMENTATIONS
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
    Ethical Rural Subsidy Policy:
    - Provides subsidies to make rural routes more attractive
    - Ensures equitable transportation access to underserved areas
    - Maintains algorithm correctness (no negative weights)
    """
    # Initialize distances and previous pointers
    distances = {node: float('inf') for node in nodes}
    distances[start] = 0.0
    previous = {node: None for node in nodes}
    
    # Priority queue: (distance, counter, node) - counter prevents Node comparison
    pq = [(0.0, 0, start)]
    visited = set()
    counter = 1  # For tie-breaking in heapq
    
    while pq:
        current_dist, _, current_node = heapq.heappop(pq)
        
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
            
            # Apply fairness modification: reduce costs for rural access
            if neighbor.region == 'rural':
                edge_cost = base_cost * 0.3  # Customer pays only 30%
            elif current_node.region == 'rural':
                edge_cost = base_cost * 0.5  # Customer pays only 50%
            else:
                edge_cost = base_cost
            
            new_distance = current_dist + edge_cost
            
            # Update if shorter path found
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (new_distance, counter, neighbor))
                counter += 1
    
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
    
    # Priority queue: (distance, counter, node) - counter prevents Node comparison
    pq = [(0.0, 0, start)]
    visited = set()
    counter = 1  # For tie-breaking in heapq
    
    while pq:
        current_dist, _, current_node = heapq.heappop(pq)
        
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
                heapq.heappush(pq, (new_distance, counter, neighbor))
                counter += 1
    
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

