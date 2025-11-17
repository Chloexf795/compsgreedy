"""
Dijkstra Algorithm Assignment - Core Classes and Helper Functions

This file contains the Node and Edge classes and helper function.

You shouldn't need to modify this file.
"""
import math
from typing import List

# ============================================================================
# Node and Edge Class
# ============================================================================
class Node:
    """
    Represents a city in the rideshare network.
    
    Attributes:
        id (str): City id
        name (str): City name
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
        Calculate distance to another node.
        
        Args:
            other_node (Node): The target node
            
        Returns:
            float: Distance between this node and the other node
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
    the node attributes and the cost perspective (In Part A).
    
    Attributes:
        u (Node): First endpoint city
        v (Node): Second endpoint city
    """
    
    def __init__(self, u: Node, v: Node):
        self.u = u
        self.v = v
    
    def get_distance(self) -> float:
        """
        Calculate distance between the two cities.
        
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
        """
        if node == self.u:
            return self.v
        elif node == self.v:
            return self.u
        else: #If the given node is not an endpoint of this edge
            raise ValueError(f"Node {node.id} is not an endpoint of edge {self}") 
    
    def __repr__(self):
        return f"Edge({self.u.id} <-> {self.v.id})"



# ============================================================================
# Helper Functions
# ============================================================================
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
