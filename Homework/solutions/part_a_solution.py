"""
Part A: Dijkstra Algorithm for Different Parties - Solution

This file focuses on implementing Dijkstra's algorithm from company and driver's different perspectives

Complete implementation for Instructors
"""

import heapq
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Tuple
from main import Node, Edge, get_neighbors


# ============================================================================
# HELPER FUNCTIONS COMPLETE IMPLEMENTATIONS
# ============================================================================

def calculate_company_cost(from_node: Node, to_node: Node) -> float:
    """
    Calculate the company's cost for traveling from one node to another.
    
    Company cost = Platform costs per ride + mileage * driver base pay per mile
    
    Args:
        from_node (Node): Starting city
        to_node (Node): Destination city
        
    Returns:
        float: Total cost from company's perspective
    """
    distance = from_node.distance_to(to_node)
    
    # Platform cost is the average of the two cities' platform costs
    platform_cost = (from_node.platform_cost + to_node.platform_cost) / 2
    
    # Driver base pay per mile (what company pays driver)
    driver_base_pay_per_mile = 0.60
    
    # Traffic increases the effective mileage for payment purposes
    effective_distance = distance * max(from_node.traffic_level, to_node.traffic_level)
    
    mileage_cost = effective_distance * driver_base_pay_per_mile
    
    return platform_cost + mileage_cost


def calculate_driver_cost(from_node: Node, to_node: Node) -> float:
    """
    Calculate the driver's cost for traveling from one node to another.
    
    Driver cost = mileage * fuel per mile + parking + maintenance
    
    Args:
        from_node (Node): Starting city
        to_node (Node): Destination city
        
    Returns:
        float: Total cost from driver's perspective
    """
    distance = from_node.distance_to(to_node)
    
    # Fuel cost varies by region and is affected by traffic
    avg_fuel_cost_per_mile = (from_node.fuel_cost_per_mile + to_node.fuel_cost_per_mile) / 2
    traffic_factor = max(from_node.traffic_level, to_node.traffic_level)
    fuel_cost = distance * avg_fuel_cost_per_mile * traffic_factor
    
    # Parking cost at destination
    parking_cost = to_node.parking_cost
    
    # Maintenance cost affected by road quality and distance
    avg_maintenance_factor = (from_node.maintenance_factor + to_node.maintenance_factor) / 2
    maintenance_cost = distance * 0.10 * avg_maintenance_factor  # Base $0.10 per mile
    
    return fuel_cost + parking_cost + maintenance_cost


# ============================================================================
# PART A: DIJKSTRA ALGORITHM COMPLETE IMPLEMENTATIONS
# ============================================================================

def dijkstra_company_route(start: Node, target: Node, nodes: List[Node], edges: List[Edge]) -> Tuple[List[Node], float]:
    """
    Part A1: Complete implementation of Dijkstra's algorithm from company's perspective.
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
        
        # Skip if already visited (handles duplicate entries in pq)
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
                
            # Calculate cost using company perspective
            edge_cost = calculate_company_cost(current_node, neighbor)
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


def dijkstra_driver_route(start: Node, target: Node, nodes: List[Node], edges: List[Edge]) -> Tuple[List[Node], float]:
    """
    Part A2: Complete implementation of Dijkstra's algorithm from driver's perspective.
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
                
            # Calculate cost using driver perspective
            edge_cost = calculate_driver_cost(current_node, neighbor)
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

