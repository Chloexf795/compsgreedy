"""
Dijkstra Algorithm Assignment - Minnesota Cities Dataset 

This file include list of Nodes of MN cities and list of Edges of simplfied Roads.

You shouldn't need to modify this file.
"""
from main import Node, Edge

# ============================================================================
# Minnesota City Nodes (with attributes)
# ============================================================================

MN_NODES = [
    # Twin Cities Urbans - High traffic, expensive parking, high platform costs
    Node("Minneapolis", "Minneapolis", 0.0, 0.0, 
         region="urban", traffic_level=2.0, parking_cost=8.0, 
         maintenance_factor=1.0, platform_cost=4.5, fuel_cost_per_mile=0.18,
         weather_condition="clear"),
    
    Node("St Paul", "St Paul", 10.0, -2.0,
         region="urban", traffic_level=1.8, parking_cost=7.0,
         maintenance_factor=1.0, platform_cost=4.2, fuel_cost_per_mile=0.17,
         weather_condition="clear"),
    
    # Inner Suburbs - Moderate values
    Node("Edina", "Edina", -4.0, -6.0,
         region="suburban", traffic_level=1.4, parking_cost=4.0,
         maintenance_factor=0.9, platform_cost=3.8, fuel_cost_per_mile=0.15,
         weather_condition="clear"),
    
    Node("Bloomington", "Bloomington", -2.0, -8.0,
         region="suburban", traffic_level=1.5, parking_cost=3.5,
         maintenance_factor=0.9, platform_cost=3.5, fuel_cost_per_mile=0.15,
         weather_condition="clear"),
    
    Node("Roseville", "Roseville", 5.0, 3.0,
         region="suburban", traffic_level=1.3, parking_cost=3.0,
         maintenance_factor=1.0, platform_cost=3.2, fuel_cost_per_mile=0.14,
         weather_condition="clear"),
    
    # Northern Suburbs
    Node("Maple Grove", "Maple Grove", -6.0, 6.0,
         region="suburban", traffic_level=1.2, parking_cost=2.5,
         maintenance_factor=0.8, platform_cost=3.0, fuel_cost_per_mile=0.14,
         weather_condition="clear"),
    
    Node("Blaine", "Blaine", 4.0, 10.0,
         region="suburban", traffic_level=1.1, parking_cost=2.0,
         maintenance_factor=0.9, platform_cost=2.8, fuel_cost_per_mile=0.13,
         weather_condition="rain"),  
    
    Node("Anoka", "Anoka", -3.0, 9.0,
         region="suburban", traffic_level=1.0, parking_cost=2.0,
         maintenance_factor=1.1, platform_cost=2.5, fuel_cost_per_mile=0.13,
         weather_condition="clear"),
    
    # Eastern Cities
    Node("Forest Lake", "Forest Lake", 15.0, 10.0,
         region="rural", traffic_level=0.8, parking_cost=1.5,
         maintenance_factor=1.2, platform_cost=2.2, fuel_cost_per_mile=0.16,
         weather_condition="snow"), 
    
    Node("Stillwater", "Stillwater", 20.0, 3.0,
         region="rural", traffic_level=0.9, parking_cost=2.0,
         maintenance_factor=1.0, platform_cost=2.5, fuel_cost_per_mile=0.16,
         weather_condition="clear"),
    
    Node("Woodbury", "Woodbury", 15.0, -1.0,
         region="suburban", traffic_level=1.3, parking_cost=3.0,
         maintenance_factor=0.8, platform_cost=3.2, fuel_cost_per_mile=0.14,
         weather_condition="clear"),
    
    Node("Cottage Grove", "Cottage Grove", 13.0, -6.0,
         region="suburban", traffic_level=1.1, parking_cost=2.5,
         maintenance_factor=1.0, platform_cost=2.8, fuel_cost_per_mile=0.15,
         weather_condition="clear"),
    
    # Southern Cities
    Node("Eagan", "Eagan", 3.0, -10.0,
         region="suburban", traffic_level=1.4, parking_cost=3.5,
         maintenance_factor=0.9, platform_cost=3.3, fuel_cost_per_mile=0.15,
         weather_condition="clear"),
    
    Node("Burnsville", "Burnsville", 1.0, -12.0,
         region="suburban", traffic_level=1.3, parking_cost=3.0,
         maintenance_factor=1.0, platform_cost=3.0, fuel_cost_per_mile=0.15,
         weather_condition="clear"),
    
    Node("Apple Valley", "Apple Valley", 2.0, -13.0,
         region="suburban", traffic_level=0.5, parking_cost=0.5, 
         maintenance_factor=0.8, platform_cost=1.5, fuel_cost_per_mile=0.08, 
         weather_condition="clear"),
    
    Node("Rosemount", "Rosemount", 5.0, -14.0,
         region="suburban", traffic_level=1.1, parking_cost=2.5,
         maintenance_factor=1.0, platform_cost=2.7, fuel_cost_per_mile=0.14,
         weather_condition="clear"),
    
    Node("Lakeville", "Lakeville", 1.0, -16.0,
         region="suburban", traffic_level=0.3, parking_cost=0.5,  
         maintenance_factor=0.7, platform_cost=1.5, fuel_cost_per_mile=0.08,  
         weather_condition="clear"),
    
    # Western/Southwest Cities
    Node("Shakopee", "Shakopee", -8.0, -10.0,
         region="suburban", traffic_level=1.5, parking_cost=4.0,
         maintenance_factor=1.3, platform_cost=2.8, fuel_cost_per_mile=0.18,
         weather_condition="clear"),
    
    Node("Prior Lake", "Prior Lake", -6.0, -12.0,
         region="suburban", traffic_level=1.0, parking_cost=2.0,
         maintenance_factor=1.1, platform_cost=2.6, fuel_cost_per_mile=0.14,
         weather_condition="clear"),
    
    Node("Chanhassen", "Chanhassen", -10.0, -9.0,
         region="suburban", traffic_level=1.1, parking_cost=2.5,
         maintenance_factor=0.9, platform_cost=2.8, fuel_cost_per_mile=0.14,
         weather_condition="clear"),
    
    # Rural/Distant Cities - Lower traffic, cheaper parking, higher fuel/maintenance costs
    Node("Hastings", "Hastings", 18.0, -10.0,
         region="rural", traffic_level=0.8, parking_cost=1.0,
         maintenance_factor=1.3, platform_cost=2.0, fuel_cost_per_mile=0.17,
         weather_condition="clear"),
    
    Node("Northfield", "Northfield", 0.0, -20.0,
         region="rural", traffic_level=0.7, parking_cost=1.0,
         maintenance_factor=1.2, platform_cost=1.8, fuel_cost_per_mile=0.17,
         weather_condition="storm"),
    
    Node("Lonsdale", "Lonsdale", -5.0, -17.0,
         region="rural", traffic_level=0.6, parking_cost=0.5,
         maintenance_factor=1.4, platform_cost=1.5, fuel_cost_per_mile=0.18,
         weather_condition="clear"),
    
    Node("New Prague", "New Prague", -8.0, -18.0,
         region="rural", traffic_level=0.6, parking_cost=5.0,
         maintenance_factor=2.0, platform_cost=1.5, fuel_cost_per_mile=0.25,
         weather_condition="clear"),
    
    Node("Monticello", "Monticello", -15.0, 13.0,
         region="rural", traffic_level=0.7, parking_cost=1.0,
         maintenance_factor=1.3, platform_cost=1.8, fuel_cost_per_mile=0.18,
         weather_condition="snow"), 
]

# Mapping so we can access nodes by name
MN_NODES_DICT = {node.id: node for node in MN_NODES}

# ============================================================================
# Minnesota Road Edges
# ============================================================================
MN_EDGES = [
    # Major east-west spine (I-94 corridor)
    Edge(MN_NODES_DICT["Monticello"], MN_NODES_DICT["Maple Grove"]),   # Monticello - Maple Grove
    Edge(MN_NODES_DICT["Maple Grove"], MN_NODES_DICT["Minneapolis"]),   # Maple Grove - Minneapolis
    Edge(MN_NODES_DICT["Minneapolis"], MN_NODES_DICT["St Paul"]),   # Minneapolis - St Paul
    Edge(MN_NODES_DICT["St Paul"], MN_NODES_DICT["Woodbury"]),   # St Paul - Woodbury
    Edge(MN_NODES_DICT["Woodbury"], MN_NODES_DICT["Stillwater"]),   # Woodbury - Stillwater
    
    # North arc (I-35 / 694 corridor)
    Edge(MN_NODES_DICT["Maple Grove"], MN_NODES_DICT["Anoka"]),   # Maple Grove - Anoka
    Edge(MN_NODES_DICT["Anoka"], MN_NODES_DICT["Blaine"]),   # Anoka - Blaine
    Edge(MN_NODES_DICT["Blaine"], MN_NODES_DICT["Forest Lake"]),   # Blaine - Forest Lake
    Edge(MN_NODES_DICT["Forest Lake"], MN_NODES_DICT["Stillwater"]),   # Forest Lake - Stillwater
    
    # South/east arc (494/35E corridor)
    Edge(MN_NODES_DICT["St Paul"], MN_NODES_DICT["Roseville"]),   # St Paul - Roseville
    Edge(MN_NODES_DICT["St Paul"], MN_NODES_DICT["Eagan"]),   # St Paul - Eagan
    Edge(MN_NODES_DICT["Eagan"], MN_NODES_DICT["Rosemount"]),   # Eagan - Rosemount
    Edge(MN_NODES_DICT["Rosemount"], MN_NODES_DICT["Apple Valley"]),   # Rosemount - Apple Valley
    Edge(MN_NODES_DICT["Apple Valley"], MN_NODES_DICT["Burnsville"]),   # Apple Valley - Burnsville
    Edge(MN_NODES_DICT["Burnsville"], MN_NODES_DICT["Lakeville"]),   # Burnsville - Lakeville
    Edge(MN_NODES_DICT["Lakeville"], MN_NODES_DICT["Northfield"]),   # Lakeville - Northfield
    Edge(MN_NODES_DICT["Northfield"], MN_NODES_DICT["Lonsdale"]),   # Northfield - Lonsdale
    Edge(MN_NODES_DICT["Lonsdale"], MN_NODES_DICT["New Prague"]),   # Lonsdale - New Prague
    
    # Southwest arc (169 corridor)
    Edge(MN_NODES_DICT["Edina"], MN_NODES_DICT["Bloomington"]),   # Edina - Bloomington
    Edge(MN_NODES_DICT["Bloomington"], MN_NODES_DICT["Shakopee"]),   # Bloomington - Shakopee
    Edge(MN_NODES_DICT["Shakopee"], MN_NODES_DICT["Prior Lake"]),   # Shakopee - Prior Lake
    Edge(MN_NODES_DICT["Prior Lake"], MN_NODES_DICT["Chanhassen"]),   # Prior Lake - Chanhassen
    Edge(MN_NODES_DICT["Chanhassen"], MN_NODES_DICT["Maple Grove"]),   # Chanhassen - Maple Grove
    
    # Downtown spokes
    Edge(MN_NODES_DICT["Minneapolis"], MN_NODES_DICT["Edina"]),   # Minneapolis - Edina
    Edge(MN_NODES_DICT["Minneapolis"], MN_NODES_DICT["Roseville"]),   # Minneapolis - Roseville
    Edge(MN_NODES_DICT["Minneapolis"], MN_NODES_DICT["Bloomington"]),   # Minneapolis - Bloomington
    Edge(MN_NODES_DICT["Minneapolis"], MN_NODES_DICT["Maple Grove"]),   # Minneapolis - Maple Grove
    Edge(MN_NODES_DICT["Minneapolis"], MN_NODES_DICT["Eagan"]),   # Minneapolis - Eagan
    
    Edge(MN_NODES_DICT["Woodbury"], MN_NODES_DICT["Cottage Grove"]),   # Woodbury - Cottage Grove
    Edge(MN_NODES_DICT["Cottage Grove"], MN_NODES_DICT["Hastings"]),   # Cottage Grove - Hastings
    Edge(MN_NODES_DICT["Roseville"], MN_NODES_DICT["Blaine"]),   # Roseville - Blaine
    Edge(MN_NODES_DICT["Edina"], MN_NODES_DICT["Chanhassen"]),   # Edina - Chanhassen

    Edge(MN_NODES_DICT["Shakopee"], MN_NODES_DICT["New Prague"]),   # Shakopee - New Prague
    Edge(MN_NODES_DICT["New Prague"], MN_NODES_DICT["Lonsdale"]),   # New Prague - Lonsdale

    Edge(MN_NODES_DICT["Edina"], MN_NODES_DICT["Minneapolis"]),     # Edina - Minneapolis
    Edge(MN_NODES_DICT["Minneapolis"], MN_NODES_DICT["Anoka"]),     # Minneapolis - Anoka
    Edge(MN_NODES_DICT["Anoka"], MN_NODES_DICT["Forest Lake"]),     # Anoka - Forest Lake
    Edge(MN_NODES_DICT["Chanhassen"], MN_NODES_DICT["Prior Lake"]), # Chanhassen - Prior Lake
    Edge(MN_NODES_DICT["Prior Lake"], MN_NODES_DICT["Burnsville"]), # Prior Lake - Burnsville
    Edge(MN_NODES_DICT["Burnsville"], MN_NODES_DICT["Rosemount"]),  # Burnsville - Rosemount
    
    Edge(MN_NODES_DICT["Edina"], MN_NODES_DICT["Bloomington"]),     # Edina - Bloomington
    Edge(MN_NODES_DICT["Bloomington"], MN_NODES_DICT["Eagan"]),     # Bloomington - Eagan
    Edge(MN_NODES_DICT["Eagan"], MN_NODES_DICT["Woodbury"]),        # Eagan - Woodbury
    Edge(MN_NODES_DICT["Woodbury"], MN_NODES_DICT["Forest Lake"]),  # Woodbury - Forest Lake
    

    Edge(MN_NODES_DICT["Edina"], MN_NODES_DICT["Roseville"]),       # Edina - Roseville
    Edge(MN_NODES_DICT["Roseville"], MN_NODES_DICT["St Paul"]),     # Roseville - St Paul
    Edge(MN_NODES_DICT["St Paul"], MN_NODES_DICT["Forest Lake"]),   # St Paul - Forest Lake 
]

# ============================================================================
# Nodes Collection for Student Implementation Feedback
# ============================================================================

STORMY_CITIES = [node.id for node in MN_NODES if node.weather_condition == "storm"]
SNOWY_CITIES = [node.id for node in MN_NODES if node.weather_condition == "snow"]
RAINY_CITIES = [node.id for node in MN_NODES if node.weather_condition == "rain"]
RURAL_CITIES = [node.id for node in MN_NODES if node.region == "rural"]
URBAN_CITIES = [node.id for node in MN_NODES if node.region == "urban"]
SUBURBAN_CITIES = [node.id for node in MN_NODES if node.region == "suburban"]