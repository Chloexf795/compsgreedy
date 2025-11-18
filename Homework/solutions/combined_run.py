
"""
Combined Assignment Runner for Parts A and D
Dijkstra Algorithm Assignment - Student Starter Code

This file helps you run Part A and Part D by taking in the start and end cities from command line input

"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def main():
    """
    Run both Parts A and D with user-specified cities.
    """
    try:
        from mn_dataset import MN_NODES_DICT, MN_EDGES
        from part_a_solution import dijkstra_company_route, dijkstra_driver_route
        from part_d_solution import dijkstra_with_fatigue_consideration, dijkstra_with_fairness_consideration, dijkstra_with_weather_safety

    # ============================================================================
    #  HANDLE INPUTS
    # ============================================================================
        print("=" * 70) 
        print("DIJKSTRA ALGORITHM ASSIGNMENT")
        print("=" * 70)
        print("Type in 2 cities to discover the cheapest path. Remember to type cities start with captial letter. ")
        print()
        # Display available cities
        available_cities = sorted(MN_NODES_DICT.keys())
        print("Available cities (case sensitive):")
        print(", ".join(available_cities))
        print()
        
        # Get user input
        start_name = input("Enter start city: ").strip()
        dest_name = input("Enter destination city: ").strip()
        
        # Validate input
        if start_name not in MN_NODES_DICT:
            print(f"Error: '{start_name}' not found in available cities")
            return
        if dest_name not in MN_NODES_DICT:
            print(f"Error: '{dest_name}' not found in available cities")
            return
            
        start_city = MN_NODES_DICT[start_name]
        destination = MN_NODES_DICT[dest_name]
        
        print(f"\nRunning algorithms for route: {start_city.name} to {destination.name}")
        print("=" * 70)

    # ============================================================================
    #  RUN PART A
    # ============================================================================
        print("\nPART A: COMPANY VS DRIVER ALGORITHM COMPARISON")
        print("-" * 50)
        
        # Company Route
        try:
            company_path, company_cost = dijkstra_company_route(start_city, destination, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"Company Route: {' -> '.join([node.name for node in company_path])}")
            print(f"Company Cost: ${company_cost:.2f}")
        except NotImplementedError:
            print("Company algorithm not yet implemented")
        except Exception as e:
            print(f"Company Route Error: {e}")
            
        # Driver Route
        try:
            driver_path, driver_cost = dijkstra_driver_route(start_city, destination, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"Driver Route: {' -> '.join([node.name for node in driver_path])}")
            print(f"Driver Cost: ${driver_cost:.2f}")
            print()
        except NotImplementedError:
            print("Driver algorithm not yet implemented")
        except Exception as e:
            print(f"Driver Route Error: {e}")

    # ============================================================================
    #  RUN PART D
    # ============================================================================
        print(f"\nPART D: ETHICAL ALGORITHM MODIFICATIONS")
        print("-" * 50)
        # Run Fatigue Consideration
        print(f"\nFATIGUE CONSIDERATION (Option 1):")
        try:
            fatigue_path, fatigue_cost = dijkstra_with_fatigue_consideration(start_city, destination, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"MODIFIED Route: {' -> '.join([node.name for node in fatigue_path])}")
            print(f"MODIFIED Cost: ${fatigue_cost:.2f}")
        except NotImplementedError:
            print("Fatigue consideration not implemented")
        except Exception as e:
            print(f"Error: {e}")

        # Run Fairness Consideration
        print(f"\nFAIRNESS CONSIDERATION (Option 2):")
        try:
            fairness_path, fairness_cost = dijkstra_with_fairness_consideration(start_city, destination, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"MODIFIED Route: {' -> '.join([node.name for node in fairness_path])}")
            print(f"MODIFIED Cost: ${fairness_cost:.2f}")
        except NotImplementedError:
            print("Fairness consideration not implemented")
        except Exception as e:
            print(f"Error: {e}")

        # Run Weather Safety
        print(f"\nWEATHER SAFETY CONSIDERATION (Option 3):")
        try:
            weather_path, weather_cost = dijkstra_with_weather_safety(start_city, destination, list(MN_NODES_DICT.values()), MN_EDGES)
            print(f"MODIFIED Route: {' -> '.join([node.name for node in weather_path])}")
            print(f"MODIFIED Cost: ${weather_cost:.2f}")
        except NotImplementedError:
            print("Weather safety not implemented")
        except Exception as e:
            print(f"Error: {e}")
            
    except ImportError:
        print("Error: Could not import Minnesota dataset or required functions")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
