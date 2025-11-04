"""
Test Suite for Part A: Dijkstra Algorithm for Different Stakeholders

This file contains tests to verify the correctness of your Dijkstra implementations.
Run this file to check if your Part A implementation is correct.

Usage: python3 test_part_a.py
"""

import sys
from typing import List, Tuple
from main import Node, Edge, calculate_company_cost, calculate_driver_cost
from mn_dataset import MN_NODES_DICT, MN_EDGES, START_CITY


def test_basic_path_structure():
    """Test 1: Check if functions return correct data types"""
    print("\n" + "="*70)
    print("TEST 1: Basic Return Type Validation")
    print("="*70)
    
    try:
        from part_a import dijkstra_company_route, dijkstra_driver_route
        
        start = START_CITY
        target = MN_NODES_DICT["Northfield"]
        
        # Test company route
        company_result = dijkstra_company_route(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        assert isinstance(company_result, tuple), " Company route should return a tuple"
        assert len(company_result) == 2, " Company route should return (path, cost)"
        path, cost = company_result
        assert isinstance(path, list), " Path should be a list"
        assert isinstance(cost, (int, float)), " Cost should be a number"
        
        print(" Company route returns correct types")
        
        # Test driver route
        driver_result = dijkstra_driver_route(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        assert isinstance(driver_result, tuple), " Driver route should return a tuple"
        assert len(driver_result) == 2, " Driver route should return (path, cost)"
        path, cost = driver_result
        assert isinstance(path, list), " Path should be a list"
        assert isinstance(cost, (int, float)), " Cost should be a number"
        
        print(" Driver route returns correct types")
        print("\n TEST 1 PASSED: Return types are correct\n")
        return True
        
    except NotImplementedError:
        print(" TEST 1 FAILED: Functions not yet implemented")
        return False
    except Exception as e:
        print(f" TEST 1 FAILED: {e}")
        return False


def test_path_validity():
    """Test 2: Check if returned paths are valid"""
    print("\n" + "="*70)
    print("TEST 2: Path Validity")
    print("="*70)
    
    try:
        from part_a import dijkstra_company_route, dijkstra_driver_route
        
        start = START_CITY
        target = MN_NODES_DICT["Northfield"]
        
        # Test company route
        company_path, company_cost = dijkstra_company_route(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        
        # Check path starts at start and ends at target
        assert len(company_path) > 0, " Path should not be empty"
        assert company_path[0] == start, f" Path should start at {start.name}"
        assert company_path[-1] == target, f" Path should end at {target.name}"
        
        # Check all nodes in path are Node objects
        for node in company_path:
            assert isinstance(node, Node), " All elements in path should be Node objects"
        
        # Check path connectivity
        for i in range(len(company_path) - 1):
            current = company_path[i]
            next_node = company_path[i + 1]
            # Verify edge exists
            edge_exists = any(
                (edge.u == current and edge.v == next_node) or 
                (edge.v == current and edge.u == next_node)
                for edge in MN_EDGES
            )
            assert edge_exists, f" No edge between {current.name} and {next_node.name}"
        
        print(f" Company path is valid: {' -> '.join([n.name for n in company_path])}")
        
        # Test driver route
        driver_path, driver_cost = dijkstra_driver_route(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        
        assert len(driver_path) > 0, " Path should not be empty"
        assert driver_path[0] == start, f" Path should start at {start.name}"
        assert driver_path[-1] == target, f" Path should end at {target.name}"
        
        for i in range(len(driver_path) - 1):
            current = driver_path[i]
            next_node = driver_path[i + 1]
            edge_exists = any(
                (edge.u == current and edge.v == next_node) or 
                (edge.v == current and edge.u == next_node)
                for edge in MN_EDGES
            )
            assert edge_exists, f" No edge between {current.name} and {next_node.name}"
        
        print(f" Driver path is valid: {' -> '.join([n.name for n in driver_path])}")
        print("\n TEST 2 PASSED: Paths are valid and connected\n")
        return True
        
    except NotImplementedError:
        print(" TEST 2 FAILED: Functions not yet implemented")
        return False
    except AssertionError as e:
        print(f" TEST 2 FAILED: {e}")
        return False
    except Exception as e:
        print(f" TEST 2 FAILED: {e}")
        return False


def test_cost_calculation():
    """Test 3: Verify cost calculations are correct"""
    print("\n" + "="*70)
    print("TEST 3: Cost Calculation Accuracy")
    print("="*70)
    
    try:
        from part_a import dijkstra_company_route, dijkstra_driver_route
        
        start = START_CITY
        target = MN_NODES_DICT["Northfield"]
        
        # Test company route
        company_path, company_cost = dijkstra_company_route(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        
        # Manually calculate cost
        manual_cost = 0.0
        for i in range(len(company_path) - 1):
            manual_cost += calculate_company_cost(company_path[i], company_path[i + 1])
        
        assert abs(company_cost - manual_cost) < 0.01, \
            f" Company cost mismatch: returned {company_cost:.2f}, expected {manual_cost:.2f}"
        
        print(f" Company cost correct: ${company_cost:.2f}")
        
        # Test driver route
        driver_path, driver_cost = dijkstra_driver_route(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        
        manual_cost = 0.0
        for i in range(len(driver_path) - 1):
            manual_cost += calculate_driver_cost(driver_path[i], driver_path[i + 1])
        
        assert abs(driver_cost - manual_cost) < 0.01, \
            f" Driver cost mismatch: returned {driver_cost:.2f}, expected {manual_cost:.2f}"
        
        print(f" Driver cost correct: ${driver_cost:.2f}")
        print("\n TEST 3 PASSED: Cost calculations are accurate\n")
        return True
        
    except NotImplementedError:
        print(" TEST 3 FAILED: Functions not yet implemented")
        return False
    except AssertionError as e:
        print(f" TEST 3 FAILED: {e}")
        return False
    except Exception as e:
        print(f" TEST 3 FAILED: {e}")
        return False


def test_optimality():
    """Test 4: Check if paths match expected optimal routes"""
    print("\n" + "="*70)
    print("TEST 4: Path Optimality Check")
    print("="*70)
    
    try:
        from part_a import dijkstra_company_route, dijkstra_driver_route
        
        # Test case 1: Minneapolis to Northfield
        start = MN_NODES_DICT["Minneapolis"]
        target = MN_NODES_DICT["Northfield"]
        
        company_path, company_cost = dijkstra_company_route(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        driver_path, driver_cost = dijkstra_driver_route(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        
        # Expected optimal paths (from solution)
        expected_company_path = ["Minneapolis", "Bloomington", "Shakopee", "New Prague", "Lonsdale", "Northfield"]
        expected_driver_path = ["Minneapolis", "Eagan", "Rosemount", "Burnsville", "Lakeville", "Northfield"]
        
        company_path_names = [node.name for node in company_path]
        driver_path_names = [node.name for node in driver_path]
        
        print(f"Route: {start.name} → {target.name}")
        print(f"  Company path: {' → '.join(company_path_names)}")
        print(f"  Expected:     {' → '.join(expected_company_path)}")
        
        assert company_path_names == expected_company_path, \
            f" Company path incorrect.\n   Got: {company_path_names}\n   Expected: {expected_company_path}"
        
        print("   Company path matches expected optimal route")
        
        print(f"\n  Driver path: {' → '.join(driver_path_names)}")
        print(f"  Expected:    {' → '.join(expected_driver_path)}")
        
        assert driver_path_names == expected_driver_path, \
            f" Driver path incorrect.\n   Got: {driver_path_names}\n   Expected: {expected_driver_path}"
        
        print("   Driver path matches expected optimal route")
        
        # Test case 2: Minneapolis to Stillwater
        target = MN_NODES_DICT["Stillwater"]
        
        company_path, company_cost = dijkstra_company_route(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        driver_path, driver_cost = dijkstra_driver_route(start, target, list(MN_NODES_DICT.values()), MN_EDGES)
        
        expected_company_path_2 = ["Minneapolis", "St Paul", "Woodbury", "Stillwater"]
        expected_driver_path_2 = ["Minneapolis", "Anoka", "Forest Lake", "Stillwater"]
        
        company_path_names = [node.name for node in company_path]
        driver_path_names = [node.name for node in driver_path]
        
        print(f"\nRoute: {start.name} → {target.name}")
        print(f"  Company path: {' → '.join(company_path_names)}")
        print(f"  Expected:     {' → '.join(expected_company_path_2)}")
        
        assert company_path_names == expected_company_path_2, \
            f" Company path incorrect.\n   Got: {company_path_names}\n   Expected: {expected_company_path_2}"
        
        print("   Company path matches expected optimal route")
        
        print(f"\n  Driver path: {' → '.join(driver_path_names)}")
        print(f"  Expected:    {' → '.join(expected_driver_path_2)}")
        
        assert driver_path_names == expected_driver_path_2, \
            f" Driver path incorrect.\n   Got: {driver_path_names}\n   Expected: {expected_driver_path_2}"
        
        print("   Driver path matches expected optimal route")
        
        print("\n TEST 4 PASSED: All paths match expected optimal routes\n")
        return True
        
    except NotImplementedError:
        print(" TEST 4 FAILED: Functions not yet implemented")
        return False
    except AssertionError as e:
        print(f" TEST 4 FAILED: {e}")
        return False
    except Exception as e:
        print(f" TEST 4 FAILED: {e}")
        return False


def test_unreachable_target():
    """Test 5: Handle unreachable targets gracefully"""
    print("\n" + "="*70)
    print("TEST 5: Unreachable Target Handling")
    print("="*70)
    
    try:
        from part_a import dijkstra_company_route, dijkstra_driver_route
        
        # Create an isolated node not connected to the main graph
        isolated_node = Node("Isolated", "Isolated City", 100.0, 100.0)
        all_nodes = list(MN_NODES_DICT.values()) + [isolated_node]
        
        start = START_CITY
        target = isolated_node
        
        company_path, company_cost = dijkstra_company_route(start, target, all_nodes, MN_EDGES)
        driver_path, driver_cost = dijkstra_driver_route(start, target, all_nodes, MN_EDGES)
        
        # Should return empty path or infinity cost
        assert (len(company_path) == 0 or company_cost == float('inf')), \
            " Should handle unreachable target (empty path or inf cost)"
        assert (len(driver_path) == 0 or driver_cost == float('inf')), \
            " Should handle unreachable target (empty path or inf cost)"
        
        print(" Unreachable targets handled correctly")
        print("\n TEST 5 PASSED: Edge cases handled properly\n")
        return True
        
    except NotImplementedError:
        print(" TEST 5 FAILED: Functions not yet implemented")
        return False
    except AssertionError as e:
        print(f" TEST 5 FAILED: {e}")
        return False
    except Exception as e:
        print(f" TEST 5 FAILED: {e}")
        return False


def run_all_tests():
    """Run all tests and provide summary"""
    print("\n" + "="*70)
    print("PART A: DIJKSTRA ALGORITHM TEST SUITE")
    print("="*70)
    print("Testing your implementation against expected behavior...")
    
    tests = [
        ("Basic Return Types", test_basic_path_structure),
        ("Path Validity", test_path_validity),
        ("Cost Calculation", test_cost_calculation),
        ("Path Optimality", test_optimality),
        ("Edge Cases", test_unreachable_target),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n {test_name} encountered an error: {e}")
            results.append((test_name, False))
    
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
        print("\n Congratulations! All tests passed!")
        print("Your Part A implementation is correct.")
    else:
        print(f"\n  {total - passed} test(s) failed. Please review your implementation.")
        print("Check the error messages above for details.")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)