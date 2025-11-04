"""
Test Suite for Part D: Ethical Algorithm Modifications

This file contains tests to verify your ethical algorithm implementation.
You only need to implement ONE of the three options (Fatigue, Fairness, or Weather).

Usage: python3 test_part_d.py
"""

import sys
from typing import List, Tuple
from main import Node, Edge, calculate_company_cost
from mn_dataset import MN_NODES_DICT, MN_EDGES, START_CITY


def detect_implemented_option():
    """Detect which ethical rule the student implemented"""
    print("\n" + "="*70)
    print("DETECTING IMPLEMENTED ETHICAL RULE")
    print("="*70)
    
    implemented = []
    
    try:
        from part_d import dijkstra_with_fatigue_consideration
        # Try to run it
        start = MN_NODES_DICT["Edina"]
        target = MN_NODES_DICT["Forest Lake"]
        result = dijkstra_with_fatigue_consideration(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        if isinstance(result, tuple) and len(result) == 2:
            implemented.append("fatigue")
            print(" Fatigue consideration detected")
    except NotImplementedError:
        pass
    except Exception:
        pass
    
    try:
        from part_d import dijkstra_with_fairness_consideration
        start = MN_NODES_DICT["Edina"]
        target = MN_NODES_DICT["Forest Lake"]
        result = dijkstra_with_fairness_consideration(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        if isinstance(result, tuple) and len(result) == 2:
            implemented.append("fairness")
            print(" Fairness consideration detected")
    except NotImplementedError:
        pass
    except Exception:
        pass
    
    try:
        from part_d import dijkstra_with_weather_safety
        start = MN_NODES_DICT["Edina"]
        target = MN_NODES_DICT["Forest Lake"]
        result = dijkstra_with_weather_safety(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        if isinstance(result, tuple) and len(result) == 2:
            implemented.append("weather")
            print(" Weather safety detected")
    except NotImplementedError:
        pass
    except Exception:
        pass
    
    if len(implemented) == 0:
        print(" No ethical rule implementation detected")
        print("   Please implement at least ONE of: Fatigue, Fairness, or Weather")
        return None
    elif len(implemented) > 1:
        print(f"\n Multiple implementations detected: {', '.join(implemented)}")
        print("  (You only need one, but great job implementing more!)")
    
    print("="*70)
    return implemented


def test_fatigue_consideration():
    """Test fatigue rule implementation"""
    print("\n" + "="*70)
    print("TESTING: FATIGUE CONSIDERATION")
    print("="*70)
    
    try:
        from part_d import dijkstra_with_fatigue_consideration
        from part_a import dijkstra_company_route
        
        # Use a route with potential for long consecutive drives
        start = MN_NODES_DICT["Edina"]
        target = MN_NODES_DICT["Forest Lake"]
        
        baseline_path, baseline_cost = dijkstra_company_route(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        fatigue_path, fatigue_cost = dijkstra_with_fatigue_consideration(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        
        print(f"Baseline (Company): {' -> '.join([n.name for n in baseline_path])}")
        print(f"Baseline cost: ${baseline_cost:.2f}")
        print(f"\nFatigue-aware: {' -> '.join([n.name for n in fatigue_path])}")
        print(f"Fatigue-aware cost: ${fatigue_cost:.2f}")
        
        # Check if valid
        assert len(fatigue_path) > 0, " Path should not be empty"
        assert fatigue_path[0] == start, " Should start at correct city"
        assert fatigue_path[-1] == target, " Should end at correct city"
        
        # Fatigue should add penalties, so cost should typically be higher or equal
        if fatigue_cost > baseline_cost:
            print(f"\n Fatigue penalties added: +${fatigue_cost - baseline_cost:.2f}")
        elif fatigue_path != baseline_path:
            print("\n Route changed to avoid fatigue penalties")
        else:
            print("\n Same route (no long consecutive drives in baseline)")
        
        # Check for long drives in the path
        long_drives = []
        for i in range(len(fatigue_path) - 1):
            dist = fatigue_path[i].distance_to(fatigue_path[i + 1])
            if dist >= 10.0:
                long_drives.append((fatigue_path[i].name, fatigue_path[i + 1].name, dist))
        
        if long_drives:
            print(f"\n Path contains {len(long_drives)} long drive(s) (≥10 miles):")
            for from_city, to_city, dist in long_drives:
                print(f"    {from_city} → {to_city}: {dist:.2f} miles")
            print("  Penalties should have been applied to these segments")
        else:
            print("\n No long drives in path (fatigue rule successfully avoided them)")
        
        print("\n FATIGUE TEST PASSED\n")
        return True
        
    except NotImplementedError:
        print("  Fatigue consideration not implemented (that's OK if you chose another option)")
        return None
    except ImportError:
        print(" Could not import required functions")
        return False
    except AssertionError as e:
        print(f" FATIGUE TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f" FATIGUE TEST FAILED: {e}")
        return False


def test_fairness_consideration():
    """Test fairness rule implementation"""
    print("\n" + "="*70)
    print("TESTING: FAIRNESS CONSIDERATION")
    print("="*70)
    
    try:
        from part_d import dijkstra_with_fairness_consideration
        from part_a import dijkstra_company_route
        
        # Use a route that goes to a rural area
        start = MN_NODES_DICT["Edina"]
        target = MN_NODES_DICT["Forest Lake"]  # Rural destination
        
        baseline_path, baseline_cost = dijkstra_company_route(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        fairness_path, fairness_cost = dijkstra_with_fairness_consideration(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        
        print(f"Baseline (Company): {' -> '.join([n.name for n in baseline_path])}")
        print(f"Baseline cost: ${baseline_cost:.2f}")
        print(f"\nFairness-aware: {' -> '.join([n.name for n in fairness_path])}")
        print(f"Fairness-aware cost: ${fairness_cost:.2f}")
        
        # Check if valid
        assert len(fairness_path) > 0, " Path should not be empty"
        assert fairness_path[0] == start, " Should start at correct city"
        assert fairness_path[-1] == target, " Should end at correct city"
        
        # Check destination is rural
        if target.region == "rural":
            print(f"\n Destination ({target.name}) is rural - subsidy should apply")
            
            # Fairness should reduce cost for rural destinations
            if fairness_cost < baseline_cost:
                print(f" Cost reduced by subsidy: -${baseline_cost - fairness_cost:.2f}")
            else:
                print("  Cost not reduced - check if subsidy is being applied")
        
        # Count rural cities in path
        rural_count = sum(1 for node in fairness_path if node.region == "rural")
        if rural_count > 0:
            print(f" Path includes {rural_count} rural city/cities")
        
        # Ensure cost is still positive (not negative)
        assert fairness_cost > 0, " Cost should remain positive (subsidies shouldn't make it negative)"
        print(" Cost remains positive (proper subsidy implementation)")
        
        print("\n FAIRNESS TEST PASSED\n")
        return True
        
    except NotImplementedError:
        print("  Fairness consideration not implemented (that's OK if you chose another option)")
        return None
    except ImportError:
        print(" Could not import required functions")
        return False
    except AssertionError as e:
        print(f" FAIRNESS TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f" FAIRNESS TEST FAILED: {e}")
        return False


def test_weather_safety():
    """Test weather safety rule implementation"""
    print("\n" + "="*70)
    print("TESTING: WEATHER SAFETY CONSIDERATION")
    print("="*70)
    
    try:
        from part_d import dijkstra_with_weather_safety
        from part_a import dijkstra_company_route
        
        # Use route that can go through bad weather cities
        start = MN_NODES_DICT["Edina"]
        target = MN_NODES_DICT["Forest Lake"]  # Has snow
        
        baseline_path, baseline_cost = dijkstra_company_route(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        weather_path, weather_cost = dijkstra_with_weather_safety(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        
        print(f"Baseline (Company): {' -> '.join([n.name for n in baseline_path])}")
        print(f"Baseline cost: ${baseline_cost:.2f}")
        print(f"\nWeather-safe: {' -> '.join([n.name for n in weather_path])}")
        print(f"Weather-safe cost: ${weather_cost:.2f}")
        
        # Check if valid
        assert len(weather_path) > 0, " Path should not be empty"
        assert weather_path[0] == start, " Should start at correct city"
        assert weather_path[-1] == target, " Should end at correct city"
        
        # Check weather conditions in path
        weather_conditions = {}
        for node in weather_path:
            condition = node.weather_condition
            weather_conditions[condition] = weather_conditions.get(condition, 0) + 1
        
        print(f"\n Weather conditions in path:")
        for condition, count in weather_conditions.items():
            print(f"    {condition}: {count} city/cities")
        
        # Weather penalties should increase cost
        if weather_cost > baseline_cost:
            print(f"\n Weather penalties applied: +${weather_cost - baseline_cost:.2f}")
        elif weather_path != baseline_path:
            print("\n Route changed to avoid bad weather")
        else:
            print("\n No bad weather in baseline route")
        
        # Check if path avoids stormy cities when possible
        stormy_count = sum(1 for node in weather_path if node.weather_condition == "storm")
        if stormy_count > 0:
            print(f"  Path includes {stormy_count} stormy city/cities (high penalty)")
        else:
            print(" Path avoids stormy weather")
        
        print("\n WEATHER SAFETY TEST PASSED\n")
        return True
        
    except NotImplementedError:
        print("  Weather safety not implemented (that's OK if you chose another option)")
        return None
    except ImportError:
        print(" Could not import required functions")
        return False
    except AssertionError as e:
        print(f" WEATHER SAFETY TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f" WEATHER SAFETY TEST FAILED: {e}")
        return False


def test_ethical_impact():
    """Test that ethical rule actually changes behavior"""
    print("\n" + "="*70)
    print("TESTING: ETHICAL IMPACT ANALYSIS")
    print("="*70)
    
    implemented = detect_implemented_option()
    if not implemented:
        return False
    
    option = implemented[0]  # Test first implemented option
    
    try:
        from part_a import dijkstra_company_route
        
        # Import the appropriate function
        if option == "fatigue":
            from part_d import dijkstra_with_fatigue_consideration as ethical_func
        elif option == "fairness":
            from part_d import dijkstra_with_fairness_consideration as ethical_func
        elif option == "weather":
            from part_d import dijkstra_with_weather_safety as ethical_func
        
        start = MN_NODES_DICT["Edina"]
        target = MN_NODES_DICT["Forest Lake"]
        
        baseline_path, baseline_cost = dijkstra_company_route(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        ethical_path, ethical_cost = ethical_func(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        
        has_impact = False
        
        if ethical_path != baseline_path:
            print(f" Ethical rule changed the chosen path")
            has_impact = True
        
        if abs(ethical_cost - baseline_cost) > 0.01:
            print(f" Ethical rule affected the cost (Δ${abs(ethical_cost - baseline_cost):.2f})")
            has_impact = True
        
        if has_impact:
            print("\n Your ethical implementation has measurable impact!")
        else:
            print("\n  Ethical rule doesn't seem to affect this particular route")
            print("   This is OK - it might affect other routes more significantly")
        
        print("\n IMPACT ANALYSIS COMPLETE\n")
        return True
        
    except Exception as e:
        print(f" IMPACT ANALYSIS FAILED: {e}")
        return False


def run_all_tests():
    """Run all tests and provide summary"""
    print("\n" + "="*70)
    print("PART D: ETHICAL ALGORITHMS TEST SUITE")
    print("="*70)
    print("Note: You only need to implement ONE ethical rule")
    
    implemented = detect_implemented_option()
    
    if not implemented:
        print("\n No ethical rule implementation detected")
        print("Please implement ONE of: Fatigue, Fairness, or Weather Safety")
        return False
    
    # Run tests based on what's implemented
    results = []
    
    if "fatigue" in implemented:
        result = test_fatigue_consideration()
        if result is not None:
            results.append(("Fatigue Implementation", result))
    
    if "fairness" in implemented:
        result = test_fairness_consideration()
        if result is not None:
            results.append(("Fairness Implementation", result))
    
    if "weather" in implemented:
        result = test_weather_safety()
        if result is not None:
            results.append(("Weather Safety Implementation", result))
    
    # Always run impact analysis
    impact_result = test_ethical_impact()
    results.append(("Ethical Impact", impact_result))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = " PASSED" if result else " FAILED"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*70)
    print(f"TOTAL: {passed}/{total} tests passed")
    print("="*70)
    
    if passed == total:
        print("\n Excellent! Your ethical algorithm implementation is working correctly.")
        print(f"You implemented: {', '.join(implemented)}")
    else:
        print(f"\n  {total - passed} test(s) failed. Please review your implementation.")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)