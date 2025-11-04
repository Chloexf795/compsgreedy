"""
Dijkstra Algorithm Assignment - Core Classes and Helper Functions

This file contains the Node and Edge classes for the rideshare routing problem.

You shouldn't need to modify this file.
"""
import math
from typing import List


class Node:
    """
    Represents a city in the rideshare network.
    
    Attributes:
        id (str): Unique identifier for the city
        name (str): Human-readable city name
        x (float): X-coordinate of the city location
        y (float): Y-coordinate of the city location
        region (str): Region type ('urban', 'suburban', 'rural')
        traffic_level (float): Traffic congestion factor (1.0 = normal, 2.0 = heavy)
        parking_cost (float): Average parking cost in dollars
        maintenance_factor (float): Road quality factor (1.0 = normal, 1.5 = poor roads)
        platform_cost (float): Company platform cost per ride in this city
        fuel_cost_per_mile (float): Fuel cost per mile in this region
        weather_condition (str): Current weather ('clear', 'rain', 'snow', 'storm')
    """
    
    def __init__(self, node_id: str, name: str, x: float, y: float,
                 region: str = "suburban", traffic_level: float = 1.0,
                 parking_cost: float = 2.0, maintenance_factor: float = 1.0,
                 platform_cost: float = 3.0, fuel_cost_per_mile: float = 0.15,
                 weather_condition: str = "clear"):
        self.id = node_id
        self.name = name
        self.x = x
        self.y = y
        self.region = region
        self.traffic_level = traffic_level
        self.parking_cost = parking_cost
        self.maintenance_factor = maintenance_factor
        self.platform_cost = platform_cost
        self.fuel_cost_per_mile = fuel_cost_per_mile
        self.weather_condition = weather_condition
    
    def distance_to(self, other_node) -> float:
        """
        Calculate Euclidean distance to another node.
        
        Args:
            other_node (Node): The target node
            
        Returns:
            float: Euclidean distance between this node and the other node
        """
        return math.sqrt((self.x - other_node.x) ** 2 + (self.y - other_node.y) ** 2)
    
    def __repr__(self):
        return (f"Node({self.id}): {self.name} at ({self.x}, {self.y}), "
                f"Region={self.region}, Traffic={self.traffic_level}")
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id
    
    def __hash__(self):
        return hash(self.id)


class Edge:
    """
    Represents a road connecting two cities.
    
    Note: Edge weights are NOT stored here. They are computed based on 
    the node attributes and the cost perspective (company vs driver).
    
    Attributes:
        u (Node): First endpoint city
        v (Node): Second endpoint city
    """
    
    def __init__(self, u: Node, v: Node):
        self.u = u
        self.v = v
    
    def get_distance(self) -> float:
        """
        Calculate Euclidean distance between the two cities.
        
        Returns:
            float: Distance between cities u and v
        """
        return self.u.distance_to(self.v)
    
    def get_other_node(self, node: Node) -> Node:
        """
        Given one endpoint of the edge, return the other endpoint.
        
        Args:
            node (Node): One endpoint of the edge
            
        Returns:
            Node: The other endpoint
            
        Raises:
            ValueError: If the given node is not an endpoint of this edge
        """
        if node == self.u:
            return self.v
        elif node == self.v:
            return self.u
        else:
            raise ValueError(f"Node {node.id} is not an endpoint of edge {self}")
    
    def __repr__(self):
        return f"Edge({self.u.id} <-> {self.v.id})"


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


def get_neighbors(node: Node, edges: List[Edge]) -> List[Node]:
    """
    Get all nodes that are directly connected to the given node.
    
    Args:
        node (Node): The node to find neighbors for
        edges (List[Edge]): All available edges in the graph
        
    Returns:
        List[Node]: List of neighboring nodes
    """
    neighbors = []
    for edge in edges:
        try:
            neighbor = edge.get_other_node(node)
            neighbors.append(neighbor)
        except ValueError:
            # Node is not an endpoint of this edge, skip
            continue
    return neighbors


def apply_weather_penalty(cost: float, from_node: Node, to_node: Node) -> float:
    """
    Apply weather-related penalties to travel cost for safety considerations.
    
    Args:
        cost (float): Base travel cost
        from_node (Node): Starting city
        to_node (Node): Destination city
        
    Returns:
        float: Cost with weather penalty applied
    """
    # Check worst weather condition on the route
    weather_conditions = [from_node.weather_condition, to_node.weather_condition]
    
    penalty_multiplier = 1.0
    if 'storm' in weather_conditions:
        penalty_multiplier = 5.0  # Severe penalty for storms
    elif 'snow' in weather_conditions:
        penalty_multiplier = 3.5  # High penalty for snow
    elif 'rain' in weather_conditions:
        penalty_multiplier = 2.0  # Moderate penalty for rain
    
    return cost * penalty_multiplier


def apply_rural_subsidy(cost: float, to_node: Node, subsidy_amount: float = 1.0) -> float:
    """
    Apply subsidy for trips to rural areas to promote fairness.
    
    Args:
        cost (float): Base travel cost
        to_node (Node): Destination city
        subsidy_amount (float): Amount to reduce cost by for rural destinations
        
    Returns:
        float: Cost with rural subsidy applied (minimum 0.1 to avoid negative costs)
    """
    if to_node.region == 'rural':
        return max(0.1, cost - subsidy_amount)
    return cost
