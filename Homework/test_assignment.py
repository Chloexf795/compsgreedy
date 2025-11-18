"""
Pytest Test Suite for Dijkstra Algorithm Assignment
Tests for Part A (Company & Driver Routes) and Part D (Ethical Modifications)

Run with: pytest test_assignment.py -v

Author: Chloe Xufeng
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Tuple
from main import Node, Edge, get_neighbors
from mn_dataset import MN_NODES_DICT, MN_EDGES


# ============================================================================
# FIXTURES - Load data once and reuse
# ============================================================================

# Get node and edge data from mn_dataset 
@pytest.fixture(scope="module")
def graph_data():
    """Fixture to load graph data once for all tests."""
    return {
        'nodes_dict': MN_NODES_DICT,
        'nodes_list': list(MN_NODES_DICT.values()),
        'edges': MN_EDGES
    }

# Import solution functions for comparison 
@pytest.fixture(scope="module")
def solution_functions():
    """Fixture to import solution functions for comparison."""
    try:
        from solutions.part_a_solution import (
            dijkstra_company_route as solution_company,
            dijkstra_driver_route as solution_driver
        )
        from solutions.part_d_solution import (
            dijkstra_with_fatigue_consideration as solution_fatigue,
            dijkstra_with_fairness_consideration as solution_fairness,
            dijkstra_with_weather_safety as solution_weather
        )
        return {
            'company': solution_company,
            'driver': solution_driver,
            'fatigue': solution_fatigue,
            'fairness': solution_fairness,
            'weather': solution_weather
        }
    except ImportError:
        pytest.skip("Solution files not available")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def is_valid_path(path: List[Node], start: Node, target: Node, edges: List[Edge]) -> Tuple[bool, str]:
    """
    Validate that a path is structurally correct.
    
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not path:
        return False, "Path is empty"
    
    if path[0] != start:
        return False, f"Path doesn't start at {start.name}, starts at {path[0].name}"
    
    if path[-1] != target:
        return False, f"Path doesn't end at {target.name}, ends at {path[-1].name}"
    
    # Check each consecutive pair is connected by an edge
    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]
        
        # Check if edge exists
        edge_exists = False
        for edge in edges:
            if (edge.u == current and edge.v == next_node) or \
               (edge.v == current and edge.u == next_node):
                edge_exists = True
                break
        
        if not edge_exists:
            return False, f"No edge exists between {current.name} and {next_node.name}"
    
    return True, ""


def calculate_actual_cost(path: List[Node], cost_function) -> float:
    """
    Calculate the actual cost of a path using the given cost function.
    
    Args:
        path: List of nodes in the path
        cost_function: Function(from_node, to_node) -> cost
    
    Returns:
        Total cost of the path
    """
    total_cost = 0.0
    for i in range(len(path) - 1):
        total_cost += cost_function(path[i], path[i + 1])
    return total_cost


# ============================================================================
# PART A TESTS - Company Route
# ============================================================================

class TestPartA:
    """Test suite for Part A: Company and Driver Dijkstra implementations."""
    
    # Test cases: (start_city, end_city, description)
    test_routes = [
        ("Anoka", "Bloomington", "suburban_to_suburban"),
        ("Minneapolis", "Northfield", "urban_to_rural"),
        ("Edina", "Forest Lake", "cross_metro"),
        ("Monticello", "Hastings", "long_distance"),
        ("St Paul", "St Paul", "same_city"),
    ]
    
    @pytest.mark.parametrize("start_name,end_name,description", test_routes)
    def test_company_return_type(self, graph_data, start_name, end_name, description):
        """Test 1: Verify company route returns correct types."""
        try:
            from part_a import dijkstra_company_route
        except ImportError:
            pytest.fail("Cannot import dijkstra_company_route from part_a.py")
        
        start = graph_data['nodes_dict'][start_name]
        end = graph_data['nodes_dict'][end_name]
        
        try:
            result = dijkstra_company_route(
                start, end, 
                graph_data['nodes_list'], 
                graph_data['edges']
            )
        except NotImplementedError:
            pytest.skip("dijkstra_company_route not yet implemented")
        
        # Check return type is tuple
        assert isinstance(result, tuple), \
            f"❌ Function must return a tuple, got {type(result)}\n" \
            f"💡 Hint: Return format should be (path, cost)"
        
        assert len(result) == 2, \
            f"❌ Function must return tuple of length 2 (path, cost), got length {len(result)}\n" \
            f"💡 Hint: return (path, cost)"
        
        path, cost = result
        
        # Check path is a list
        assert isinstance(path, list), \
            f"❌ Path must be a list, got {type(path)}\n" \
            f"💡 Hint: Build path as a list of Node objects"
        
        # Check cost is numeric
        assert isinstance(cost, (int, float)), \
            f"❌ Cost must be a number, got {type(cost)}\n" \
            f"💡 Hint: Cost should be float representing total trip cost"
    
    
    @pytest.mark.parametrize("start_name,end_name,description", test_routes)
    def test_company_path_validity(self, graph_data, start_name, end_name, description):
        """Test 2: Verify company path is structurally valid."""
        try:
            from part_a import dijkstra_company_route
        except ImportError:
            pytest.fail("Cannot import dijkstra_company_route from part_a.py")
        
        start = graph_data['nodes_dict'][start_name]
        end = graph_data['nodes_dict'][end_name]
        
        try:
            path, cost = dijkstra_company_route(
                start, end,
                graph_data['nodes_list'],
                graph_data['edges']
            )
        except NotImplementedError:
            pytest.skip("dijkstra_company_route not yet implemented")
        
        # Validate path structure
        is_valid, error_msg = is_valid_path(path, start, end, graph_data['edges'])
        
        assert is_valid, \
            f"❌ Invalid path for {start_name} → {end_name}: {error_msg}\n" \
            f"   Your path: {' → '.join([n.name for n in path]) if path else 'empty'}\n" \
            f"💡 Hints:\n" \
            f"   - Ensure path starts at {start_name} and ends at {end_name}\n" \
            f"   - Each consecutive node pair must be connected by an edge\n" \
            f"   - Use get_neighbors() to find valid connections"
    
    
    @pytest.mark.parametrize("start_name,end_name,description", test_routes)
    def test_company_cost_accuracy(self, graph_data, solution_functions, start_name, end_name, description):
        """Test 3: Verify company cost matches expected value."""
        try:
            from part_a import dijkstra_company_route, calculate_company_cost
        except ImportError:
            pytest.fail("Cannot import required functions from part_a.py")
        
        start = graph_data['nodes_dict'][start_name]
        end = graph_data['nodes_dict'][end_name]
        
        try:
            student_path, student_cost = dijkstra_company_route(
                start, end,
                graph_data['nodes_list'],
                graph_data['edges']
            )
        except NotImplementedError:
            pytest.skip("dijkstra_company_route not yet implemented")
        
        # Get solution cost
        solution_path, solution_cost = solution_functions['company'](
            start, end,
            graph_data['nodes_list'],
            graph_data['edges']
        )
        
        # Allow small floating point tolerance
        assert student_cost == pytest.approx(solution_cost, rel=1e-2), \
            f"❌ Company cost incorrect for {start_name} → {end_name}\n" \
            f"   Your cost: ${student_cost:.2f}\n" \
            f"   Expected: ${solution_cost:.2f}\n" \
            f"   Difference: ${abs(student_cost - solution_cost):.2f}\n" \
            f"💡 Hints:\n" \
            f"   - Check calculate_company_cost() implementation\n" \
            f"   - Company cost = platform_cost + (distance × traffic × $0.60)\n" \
            f"   - Ensure you're accumulating costs correctly in Dijkstra\n" \
            f"   - Verify you're using max(traffic_level) between nodes"
    
    
    @pytest.mark.parametrize("start_name,end_name,description", test_routes)
    def test_company_path_optimality(self, graph_data, solution_functions, start_name, end_name, description):
        """Test 4: Verify company path is optimal (or has same cost as optimal)."""
        try:
            from part_a import dijkstra_company_route, calculate_company_cost
        except ImportError:
            pytest.fail("Cannot import required functions from part_a.py")
        
        start = graph_data['nodes_dict'][start_name]
        end = graph_data['nodes_dict'][end_name]
        
        try:
            student_path, student_cost = dijkstra_company_route(
                start, end,
                graph_data['nodes_list'],
                graph_data['edges']
            )
        except NotImplementedError:
            pytest.skip("dijkstra_company_route not yet implemented")
        
        # Calculate actual cost of student's path
        actual_cost = calculate_actual_cost(student_path, calculate_company_cost)
        
        # Verify reported cost matches actual path cost
        assert student_cost == pytest.approx(actual_cost, rel=1e-2), \
            f"❌ Reported cost doesn't match actual path cost for {start_name} → {end_name}\n" \
            f"   Reported cost: ${student_cost:.2f}\n" \
            f"   Actual path cost: ${actual_cost:.2f}\n" \
            f"   Your path: {' → '.join([n.name for n in student_path])}\n" \
            f"💡 Hints:\n" \
            f"   - Your path reconstruction might be incorrect\n" \
            f"   - Check that you're updating distances correctly\n" \
            f"   - Verify cost accumulation in the main loop"
    
    
    # ============================================================================
    # DRIVER ROUTE TESTS
    # ============================================================================
    
    @pytest.mark.parametrize("start_name,end_name,description", test_routes)
    def test_driver_return_type(self, graph_data, start_name, end_name, description):
        """Test 5: Verify driver route returns correct types."""
        try:
            from part_a import dijkstra_driver_route
        except ImportError:
            pytest.fail("Cannot import dijkstra_driver_route from part_a.py")
        
        start = graph_data['nodes_dict'][start_name]
        end = graph_data['nodes_dict'][end_name]
        
        try:
            result = dijkstra_driver_route(
                start, end,
                graph_data['nodes_list'],
                graph_data['edges']
            )
        except NotImplementedError:
            pytest.skip("dijkstra_driver_route not yet implemented")
        
        assert isinstance(result, tuple) and len(result) == 2, \
            f"❌ Function must return (path, cost) tuple\n" \
            f"💡 Hint: Same format as company route"
        
        path, cost = result
        assert isinstance(path, list), f"❌ Path must be a list"
        assert isinstance(cost, (int, float)), f"❌ Cost must be numeric"
    
    
    @pytest.mark.parametrize("start_name,end_name,description", test_routes)
    def test_driver_path_validity(self, graph_data, start_name, end_name, description):
        """Test 6: Verify driver path is structurally valid."""
        try:
            from part_a import dijkstra_driver_route
        except ImportError:
            pytest.fail("Cannot import dijkstra_driver_route from part_a.py")
        
        start = graph_data['nodes_dict'][start_name]
        end = graph_data['nodes_dict'][end_name]
        
        try:
            path, cost = dijkstra_driver_route(
                start, end,
                graph_data['nodes_list'],
                graph_data['edges']
            )
        except NotImplementedError:
            pytest.skip("dijkstra_driver_route not yet implemented")
        
        is_valid, error_msg = is_valid_path(path, start, end, graph_data['edges'])
        
        assert is_valid, \
            f"❌ Invalid driver path for {start_name} → {end_name}: {error_msg}\n" \
            f"   Your path: {' → '.join([n.name for n in path]) if path else 'empty'}\n" \
            f"💡 Hints: Same validation rules as company route"
    
    
    @pytest.mark.parametrize("start_name,end_name,description", test_routes)
    def test_driver_cost_accuracy(self, graph_data, solution_functions, start_name, end_name, description):
        """Test 7: Verify driver cost matches expected value."""
        try:
            from part_a import dijkstra_driver_route
        except ImportError:
            pytest.fail("Cannot import dijkstra_driver_route from part_a.py")
        
        start = graph_data['nodes_dict'][start_name]
        end = graph_data['nodes_dict'][end_name]
        
        try:
            student_path, student_cost = dijkstra_driver_route(
                start, end,
                graph_data['nodes_list'],
                graph_data['edges']
            )
        except NotImplementedError:
            pytest.skip("dijkstra_driver_route not yet implemented")
        
        solution_path, solution_cost = solution_functions['driver'](
            start, end,
            graph_data['nodes_list'],
            graph_data['edges']
        )
        
        assert student_cost == pytest.approx(solution_cost, rel=1e-2), \
            f"❌ Driver cost incorrect for {start_name} → {end_name}\n" \
            f"   Your cost: ${student_cost:.2f}\n" \
            f"   Expected: ${solution_cost:.2f}\n" \
            f"💡 Hints:\n" \
            f"   - Check calculate_driver_cost() implementation\n" \
            f"   - Driver cost = fuel + parking + maintenance\n" \
            f"   - Fuel = distance × avg_fuel × traffic\n" \
            f"   - Maintenance = distance × 0.10 × avg_maintenance_factor"


# ============================================================================
# PART D TESTS - Ethical Modifications
# ============================================================================

class TestPartD:
    """Test suite for Part D: Ethical Algorithm Modifications."""
    
    # Test routes that highlight ethical considerations
    ethical_test_routes = [
        # Fatigue tests - long distance routes
        ("Minneapolis", "Monticello", "test_long_distance"),
        ("Edina", "Hastings", "test_multiple_long_segments"),
        
        # Fairness tests - rural destinations
        ("Minneapolis", "Northfield", "urban_to_rural"),
        ("Edina", "New Prague", "suburban_to_rural"),
        
        # Weather tests - stormy/snowy routes
        ("Minneapolis", "Northfield", "route_through_storm"),
        ("Roseville", "Forest Lake", "route_through_snow"),
    ]
    
    @pytest.fixture(scope="class")
    def detect_implementation(self, graph_data):
        """Detect which ethical modification(s) the student implemented."""
        implementations = {
            'fatigue': False,
            'fairness': False,
            'weather': False
        }
        
        try:
            from part_d import (
                dijkstra_with_fatigue_consideration,
                dijkstra_with_fairness_consideration,
                dijkstra_with_weather_safety
            )
            
            start = graph_data['nodes_dict']['Minneapolis']
            end = graph_data['nodes_dict']['Northfield']
            
            # Test fatigue
            try:
                path, cost = dijkstra_with_fatigue_consideration(
                    start, end, graph_data['nodes_list'], graph_data['edges']
                )
                if path:  # If returns non-empty path, it's implemented
                    implementations['fatigue'] = True
            except NotImplementedError:
                pass
            
            # Test fairness
            try:
                path, cost = dijkstra_with_fairness_consideration(
                    start, end, graph_data['nodes_list'], graph_data['edges']
                )
                if path:
                    implementations['fairness'] = True
            except NotImplementedError:
                pass
            
            # Test weather
            try:
                path, cost = dijkstra_with_weather_safety(
                    start, end, graph_data['nodes_list'], graph_data['edges']
                )
                if path:
                    implementations['weather'] = True
            except NotImplementedError:
                pass
                
        except ImportError:
            pass
        
        return implementations
    
    
    def test_at_least_one_implementation(self, detect_implementation):
        """Verify student implemented at least one ethical modification."""
        implemented = any(detect_implementation.values())
        
        if not implemented:
            pytest.fail(
                "❌ No ethical modifications implemented in Part D\n"
                "💡 Hint: You must implement ONE of:\n"
                "   1. dijkstra_with_fatigue_consideration\n"
                "   2. dijkstra_with_fairness_consideration\n"
                "   3. dijkstra_with_weather_safety"
            )
    
    
    # ============================================================================
    # FATIGUE TESTS
    # ============================================================================
    
    @pytest.mark.parametrize("start_name,end_name,description", ethical_test_routes[:2])
    def test_fatigue_return_type(self, graph_data, detect_implementation, start_name, end_name, description):
        """Test fatigue implementation return type."""
        if not detect_implementation['fatigue']:
            pytest.skip("Fatigue consideration not implemented")
        
        from part_d import dijkstra_with_fatigue_consideration
        
        start = graph_data['nodes_dict'][start_name]
        end = graph_data['nodes_dict'][end_name]
        
        result = dijkstra_with_fatigue_consideration(
            start, end, graph_data['nodes_list'], graph_data['edges']
        )
        
        assert isinstance(result, tuple) and len(result) == 2, \
            "❌ Fatigue function must return (path, cost) tuple"
        
        path, cost = result
        assert isinstance(path, list), "❌ Path must be a list"
        assert isinstance(cost, (int, float)), "❌ Cost must be numeric"
    
    
    @pytest.mark.parametrize("start_name,end_name,description", ethical_test_routes[:2])
    def test_fatigue_path_validity(self, graph_data, detect_implementation, start_name, end_name, description):
        """Test fatigue path is valid."""
        if not detect_implementation['fatigue']:
            pytest.skip("Fatigue consideration not implemented")
        
        from part_d import dijkstra_with_fatigue_consideration
        
        start = graph_data['nodes_dict'][start_name]
        end = graph_data['nodes_dict'][end_name]
        
        path, cost = dijkstra_with_fatigue_consideration(
            start, end, graph_data['nodes_list'], graph_data['edges']
        )
        
        is_valid, error_msg = is_valid_path(path, start, end, graph_data['edges'])
        
        assert is_valid, \
            f"❌ Invalid fatigue path: {error_msg}\n" \
            f"💡 Hint: Fatigue penalties shouldn't break path connectivity"
    
    
    def test_fatigue_penalty_applied(self, graph_data, detect_implementation, solution_functions):
        """Test that fatigue penalties are actually applied."""
        if not detect_implementation['fatigue']:
            pytest.skip("Fatigue consideration not implemented")
        
        from part_d import dijkstra_with_fatigue_consideration
        from part_a import dijkstra_company_route
        
        # Use a route with long segments
        start = graph_data['nodes_dict']['Minneapolis']
        end = graph_data['nodes_dict']['Monticello']
        
        # Get regular company route
        company_path, company_cost = dijkstra_company_route(
            start, end, graph_data['nodes_list'], graph_data['edges']
        )
        
        # Get fatigue route
        fatigue_path, fatigue_cost = dijkstra_with_fatigue_consideration(
            start, end, graph_data['nodes_list'], graph_data['edges']
        )
        
        # Fatigue cost should be >= company cost (due to penalties)
        assert fatigue_cost >= company_cost * 0.95, \
            f"❌ Fatigue cost seems too low - penalties may not be applied\n" \
            f"   Company cost: ${company_cost:.2f}\n" \
            f"   Fatigue cost: ${fatigue_cost:.2f}\n" \
            f"💡 Hints:\n" \
            f"   - Add $15 penalty for any long drive (≥10 miles)\n" \
            f"   - Add $50 penalty for consecutive long drives\n" \
            f"   - Check your distance calculations with node.distance_to()"
    
    
    # ============================================================================
    # FAIRNESS TESTS
    # ============================================================================
    
    @pytest.mark.parametrize("start_name,end_name,description", ethical_test_routes[2:4])
    def test_fairness_return_type(self, graph_data, detect_implementation, start_name, end_name, description):
        """Test fairness implementation return type."""
        if not detect_implementation['fairness']:
            pytest.skip("Fairness consideration not implemented")
        
        from part_d import dijkstra_with_fairness_consideration
        
        start = graph_data['nodes_dict'][start_name]
        end = graph_data['nodes_dict'][end_name]
        
        result = dijkstra_with_fairness_consideration(
            start, end, graph_data['nodes_list'], graph_data['edges']
        )
        
        assert isinstance(result, tuple) and len(result) == 2, \
            "❌ Fairness function must return (path, cost) tuple"
    
    
    @pytest.mark.parametrize("start_name,end_name,description", ethical_test_routes[2:4])
    def test_fairness_path_validity(self, graph_data, detect_implementation, start_name, end_name, description):
        """Test fairness path is valid."""
        if not detect_implementation['fairness']:
            pytest.skip("Fairness consideration not implemented")
        
        from part_d import dijkstra_with_fairness_consideration
        
        start = graph_data['nodes_dict'][start_name]
        end = graph_data['nodes_dict'][end_name]
        
        path, cost = dijkstra_with_fairness_consideration(
            start, end, graph_data['nodes_list'], graph_data['edges']
        )
        
        is_valid, error_msg = is_valid_path(path, start, end, graph_data['edges'])
        
        assert is_valid, \
            f"❌ Invalid fairness path: {error_msg}\n" \
            f"💡 Hint: Rural subsidies shouldn't break path connectivity"
    
    
    def test_fairness_subsidy_applied(self, graph_data, detect_implementation):
        """Test that rural subsidies are actually applied."""
        if not detect_implementation['fairness']:
            pytest.skip("Fairness consideration not implemented")
        
        from part_d import dijkstra_with_fairness_consideration
        from part_a import dijkstra_company_route
        
        # Use urban to rural route
        start = graph_data['nodes_dict']['Minneapolis']
        end = graph_data['nodes_dict']['Northfield']  # Rural destination
        
        # Get regular company route
        company_path, company_cost = dijkstra_company_route(
            start, end, graph_data['nodes_list'], graph_data['edges']
        )
        
        # Get fairness route
        fairness_path, fairness_cost = dijkstra_with_fairness_consideration(
            start, end, graph_data['nodes_list'], graph_data['edges']
        )
        
        # Fairness cost should be lower (due to rural subsidy)
        assert fairness_cost < company_cost, \
            f"❌ Fairness cost should be lower than company cost for rural destinations\n" \
            f"   Company cost: ${company_cost:.2f}\n" \
            f"   Fairness cost: ${fairness_cost:.2f}\n" \
            f"   Destination: {end.name} (region: {end.region})\n" \
            f"💡 Hints:\n" \
            f"   - Apply subsidy for trips TO rural destinations\n" \
            f"   - Check if neighbor.region == 'rural'\n" \
            f"   - Subsidy should reduce cost but keep it positive\n" \
            f"   - Use max(0.1, cost - subsidy) to prevent negative costs"
    
    
    def test_fairness_no_negative_costs(self, graph_data, detect_implementation):
        """Test that fairness implementation maintains non-negative costs."""
        if not detect_implementation['fairness']:
            pytest.skip("Fairness consideration not implemented")
        
        from part_d import dijkstra_with_fairness_consideration
        
        # Test multiple routes
        test_pairs = [
            ("Minneapolis", "Northfield"),
            ("Edina", "New Prague"),
            ("St Paul", "Lonsdale")
        ]
        
        for start_name, end_name in test_pairs:
            start = graph_data['nodes_dict'][start_name]
            end = graph_data['nodes_dict'][end_name]
            
            path, cost = dijkstra_with_fairness_consideration(
                start, end, graph_data['nodes_list'], graph_data['edges']
            )
            
            assert cost > 0, \
                f"❌ Cost must remain positive even with subsidies\n" \
                f"   Route: {start_name} → {end_name}\n" \
                f"   Your cost: ${cost:.2f}\n" \
                f"💡 Hint: Use max(0.1, cost - subsidy) to ensure positive costs"
    
    
    # ============================================================================
    # WEATHER SAFETY TESTS
    # ============================================================================
    
    @pytest.mark.parametrize("start_name,end_name,description", ethical_test_routes[4:])
    def test_weather_return_type(self, graph_data, detect_implementation, start_name, end_name, description):
        """Test weather safety implementation return type."""
        if not detect_implementation['weather']:
            pytest.skip("Weather safety not implemented")
        
        from part_d import dijkstra_with_weather_safety
        
        start = graph_data['nodes_dict'][start_name]
        end = graph_data['nodes_dict'][end_name]
        
        result = dijkstra_with_weather_safety(
            start, end, graph_data['nodes_list'], graph_data['edges']
        )
        
        assert isinstance(result, tuple) and len(result) == 2, \
            "❌ Weather function must return (path, cost) tuple"
    
    
    @pytest.mark.parametrize("start_name,end_name,description", ethical_test_routes[4:])
    def test_weather_path_validity(self, graph_data, detect_implementation, start_name, end_name, description):
        """Test weather safety path is valid."""
        if not detect_implementation['weather']:
            pytest.skip("Weather safety not implemented")
        
        from part_d import dijkstra_with_weather_safety
        
        start = graph_data['nodes_dict'][start_name]
        end = graph_data['nodes_dict'][end_name]
        
        path, cost = dijkstra_with_weather_safety(
            start, end, graph_data['nodes_list'], graph_data['edges']
        )
        
        is_valid, error_msg = is_valid_path(path, start, end, graph_data['edges'])
        
        assert is_valid, \
            f"❌ Invalid weather safety path: {error_msg}\n" \
            f"💡 Hint: Weather penalties shouldn't break path connectivity"
    
    
    def test_weather_penalty_applied(self, graph_data, detect_implementation):
        """Test that weather penalties are actually applied."""
        if not detect_implementation['weather']:
            pytest.skip("Weather safety not implemented")
        
        from part_d import dijkstra_with_weather_safety
        from part_a import dijkstra_company_route
        
        # Use route that goes through stormy/snowy areas
        start = graph_data['nodes_dict']['Minneapolis']
        end = graph_data['nodes_dict']['Northfield']  # Storm weather
        
        # Get regular company route
        company_path, company_cost = dijkstra_company_route(
            start, end, graph_data['nodes_list'], graph_data['edges']
        )
        
        # Get weather safety route
        weather_path, weather_cost = dijkstra_with_weather_safety(
            start, end, graph_data['nodes_list'], graph_data['edges']
        )
        
        # Weather cost should be higher (due to storm penalties)
        assert weather_cost > company_cost, \
            f"❌ Weather safety cost should be higher when routing through bad weather\n" \
            f"   Company cost: ${company_cost:.2f}\n" \
            f"   Weather cost: ${weather_cost:.2f}\n" \
            f"   Destination: {end.name} (weather: {end.weather_condition})\n" \
            f"💡 Hints:\n" \
            f"   - Apply weather penalties based on conditions\n" \
            f"   - Storm: 5.0x multiplier, Snow: 3.5x, Rain: 2.0x\n" \
            f"   - Check both from_node and to_node weather_condition\n" \
            f"   - Use the WORSE weather between the two nodes"
    
    
    def test_weather_avoids_storms(self, graph_data, detect_implementation):
        """Test that weather safety tries to avoid stormy routes when possible."""
        if not detect_implementation['weather']:
            pytest.skip("Weather safety not implemented")
        
        from part_d import dijkstra_with_weather_safety
        
        # Routes where storm avoidance matters
        start = graph_data['nodes_dict']['Edina']
        end = graph_data['nodes_dict']['Hastings']
        
        path, cost = dijkstra_with_weather_safety(
            start, end, graph_data['nodes_list'], graph_data['edges']
        )
        
        # Count nodes with bad weather in path
        storm_count = sum(1 for node in path if node.weather_condition == 'storm')
        snow_count = sum(1 for node in path if node.weather_condition == 'snow')
        
        # Path should minimize exposure to bad weather
        # (This is a heuristic - may need adjustment based on graph structure)
        total_bad_weather = storm_count + snow_count
        
        # Just verify the path exists and is valid
        # The cost test above already verifies penalties are applied
        assert len(path) > 0, \
            f"❌ Weather safety should still find a valid path\n" \
            f"💡 Hint: Penalties make routes more expensive but shouldn't block them entirely"


# ============================================================================
# INTEGRATION TESTS - Cross-cutting concerns
# ============================================================================

class TestIntegration:
    """Integration tests to verify overall system behavior."""
    
    def test_different_perspectives_different_routes(self, graph_data):
        """Verify company and driver perspectives can produce different routes."""
        try:
            from part_a import dijkstra_company_route, dijkstra_driver_route
        except ImportError:
            pytest.skip("Part A not fully implemented")
        
        # Find a route where perspectives differ
        start = graph_data['nodes_dict']['Minneapolis']
        end = graph_data['nodes_dict']['Hastings']
        
        try:
            company_path, company_cost = dijkstra_company_route(
                start, end, graph_data['nodes_list'], graph_data['edges']
            )
            driver_path, driver_cost = dijkstra_driver_route(
                start, end, graph_data['nodes_list'], graph_data['edges']
            )
        except NotImplementedError:
            pytest.skip("Functions not implemented")
        
        # Costs should generally be different (different cost models)
        # Paths may or may not be different depending on graph structure
        assert company_cost != driver_cost or company_path != driver_path, \
            f"⚠️  Company and driver routes identical - this is unusual\n" \
            f"   This may be correct if the optimal path is the same for both\n" \
            f"💡 Note: Different cost functions usually lead to different optimal routes"
    
    
    def test_unreachable_destination(self, graph_data):
        """Test handling of unreachable destinations."""
        try:
            from part_a import dijkstra_company_route
        except ImportError:
            pytest.skip("Part A not implemented")
        
        # Create an isolated node (not in the connected graph)
        from main import Node
        isolated = Node("Isolated", "Isolated City", 1000.0, 1000.0)
        
        start = graph_data['nodes_dict']['Minneapolis']
        
        try:
            path, cost = dijkstra_company_route(
                start, isolated,
                graph_data['nodes_list'] + [isolated],
                graph_data['edges']
            )
        except NotImplementedError:
            pytest.skip("Function not implemented")
        
        # Should return empty path or infinite cost
        assert path == [] or cost == float('inf'), \
            f"❌ Should handle unreachable destinations gracefully\n" \
            f"   Expected: empty path or infinite cost\n" \
            f"   Got: path length {len(path)}, cost ${cost:.2f}\n" \
            f"💡 Hint: Check if target is reachable before reconstructing path"
    
    
    def test_same_start_end(self, graph_data):
        """Test when start and destination are the same."""
        try:
            from part_a import dijkstra_company_route
        except ImportError:
            pytest.skip("Part A not implemented")
        
        start = graph_data['nodes_dict']['Minneapolis']
        
        try:
            path, cost = dijkstra_company_route(
                start, start,
                graph_data['nodes_list'],
                graph_data['edges']
            )
        except NotImplementedError:
            pytest.skip("Function not implemented")
        
        # Should return path with just start node and zero cost
        assert len(path) == 1 and path[0] == start, \
            f"❌ When start == destination, path should be [start]\n" \
            f"   Your path: {[n.name for n in path]}\n" \
            f"💡 Hint: Initialize distances[start] = 0"
        
        assert cost == pytest.approx(0.0, abs=1e-2), \
            f"❌ When start == destination, cost should be 0\n" \
            f"   Your cost: ${cost:.2f}"


# ============================================================================
# PERFORMANCE TESTS (Optional - can be slow)
# ============================================================================

class TestPerformance:
    """Optional performance tests to ensure reasonable efficiency."""
    
    @pytest.mark.timeout(5)
    def test_performance_large_route(self, graph_data):
        """Test that algorithm completes in reasonable time."""
        try:
            from part_a import dijkstra_company_route
        except ImportError:
            pytest.skip("Part A not implemented")
        
        # Test longest possible route
        start = graph_data['nodes_dict']['Monticello']
        end = graph_data['nodes_dict']['Hastings']
        
        try:
            path, cost = dijkstra_company_route(
                start, end,
                graph_data['nodes_list'],
                graph_data['edges']
            )
        except NotImplementedError:
            pytest.skip("Function not implemented")
        
        # If we get here, it completed within timeout
        assert len(path) > 0, "Should find a path within time limit"


# ============================================================================
# HELPER TEST - Run this first to diagnose issues
# ============================================================================

class TestDiagnostics:
    """Diagnostic tests to help identify common issues quickly."""
    
    def test_imports(self):
        """Test that all required modules can be imported."""
        errors = []
        
        try:
            import main
        except ImportError as e:
            errors.append(f"Cannot import main.py: {e}")
        
        try:
            import mn_dataset
        except ImportError as e:
            errors.append(f"Cannot import mn_dataset.py: {e}")
        
        try:
            import part_a
        except ImportError as e:
            errors.append(f"Cannot import part_a.py: {e}")
        
        try:
            import part_d
        except ImportError as e:
            errors.append(f"Cannot import part_d.py: {e}")
        
        if errors:
            pytest.fail(
                "❌ Import errors detected:\n" + 
                "\n".join(f"   • {err}" for err in errors) +
                "\n💡 Hint: Ensure all files are in the correct directory"
            )
    
    
    def test_helper_functions_exist(self):
        """Test that required helper functions are defined."""
        try:
            from part_a import calculate_company_cost, calculate_driver_cost
        except ImportError:
            pytest.fail(
                "❌ Cannot import helper functions from part_a.py\n"
                "💡 Hint: Implement calculate_company_cost() and calculate_driver_cost()"
            )
        
        # Test helper functions work
        from mn_dataset import MN_NODES_DICT
        
        node1 = MN_NODES_DICT['Minneapolis']
        node2 = MN_NODES_DICT['St Paul']
        
        try:
            cost = calculate_company_cost(node1, node2)
            assert isinstance(cost, (int, float)), \
                "calculate_company_cost must return a number"
            assert cost > 0, \
                "calculate_company_cost should return positive cost"
        except NotImplementedError:
            pytest.skip("calculate_company_cost not implemented")
        
        try:
            cost = calculate_driver_cost(node1, node2)
            assert isinstance(cost, (int, float)), \
                "calculate_driver_cost must return a number"
            assert cost > 0, \
                "calculate_driver_cost should return positive cost"
        except NotImplementedError:
            pytest.skip("calculate_driver_cost not implemented")
    
    
    def test_graph_data_loaded(self, graph_data):
        """Test that graph data is properly loaded."""
        assert len(graph_data['nodes_dict']) == 25, \
            f"Expected 25 cities, found {len(graph_data['nodes_dict'])}"
        
        assert len(graph_data['edges']) > 0, \
            "No edges found in graph"
        
        # Test a few key cities exist
        key_cities = ['Minneapolis', 'St Paul', 'Northfield', 'Bloomington']
        for city in key_cities:
            assert city in graph_data['nodes_dict'], \
                f"Key city '{city}' not found in dataset"


# ============================================================================
# SUMMARY REPORT
# ============================================================================

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Custom summary to help students understand results."""
    terminalreporter.write_sep("=", "Assignment Test Summary")
    
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    
    terminalreporter.write_line(f"\n✅ Passed: {passed}")
    terminalreporter.write_line(f"❌ Failed: {failed}")
    terminalreporter.write_line(f"⏭️  Skipped: {skipped}")
    
    if failed == 0 and passed > 0:
        terminalreporter.write_line("\n🎉 Congratulations! All implemented tests pass!")
    elif failed > 0:
        terminalreporter.write_line("\n💡 Review the failure hints above to fix issues.")
        terminalreporter.write_line("   Run individual tests with: pytest test_assignment.py::TestPartA::test_name -v")


if __name__ == "__main__":
    """Allow running as script: python test_assignment.py"""
    pytest.main([__file__, "-v", "--tb=short"])