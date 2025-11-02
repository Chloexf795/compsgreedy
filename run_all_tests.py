"""
Complete Test Runner for Dijkstra Algorithm Assignment

This script runs all tests for Parts A and D.
Use this to verify your complete implementation.

Usage: python3 run_all_tests.py
       python3 run_all_tests.py --part a    # Test only Part A
       python3 run_all_tests.py --part d    # Test only Part D
"""

import sys
import argparse


def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*80)
    print(title.center(80))
    print("="*80 + "\n")


def run_part_a_tests():
    """Run Part A tests"""
    print_header("PART A: DIJKSTRA ALGORITHM TESTS")
    try:
        import test_part_a
        success = test_part_a.run_all_tests()
        return success
    except ImportError as e:
        print(f"Could not import test_part_a.py: {e}")
        return False
    except Exception as e:
        print(f"Error running Part A tests: {e}")
        return False


def run_part_d_tests():
    """Run Part D tests"""
    print_header("PART D: ETHICAL ALGORITHMS TESTS")
    try:
        import test_part_d
        success = test_part_d.run_all_tests()
        return success
    except ImportError as e:
        print(f"Could not import test_part_d.py: {e}")
        return False
    except Exception as e:
        print(f"Error running Part D tests: {e}")
        return False


def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(
        description='Run tests for Dijkstra Algorithm Assignment'
    )
    parser.add_argument(
        '--part',
        choices=['a', 'd', 'all'],
        default='all',
        help='Which part to test (default: all)'
    )
    
    args = parser.parse_args()
    
    print_header("DIJKSTRA ALGORITHM ASSIGNMENT - TEST SUITE")
    print("This will test your implementation for correctness.")
    print("Make sure you have completed the corresponding parts before running tests.")
    print("\nNote: Part B is not tested - you will reflect on that implementation yourself.\n")
    
    results = {}
    
    # Run requested tests
    if args.part in ['a', 'all']:
        results['Part A'] = run_part_a_tests()
    
    if args.part in ['d', 'all']:
        results['Part D'] = run_part_d_tests()
    
    # Final summary
    if results:
        print_header("FINAL TEST SUMMARY")
        
        all_passed = True
        for part, passed in results.items():
            status = "PASSED" if passed else "FAILED"
            print(f"{status}: {part}")
            if not passed:
                all_passed = False
        
        print("\n" + "="*80)
        
        if all_passed:
            print(" CONGRATULATIONS! All implemented parts passed their tests!")
            print("\nNext steps:")
            print("  • Part B: Run your implementation and complete your reflection")
            print("  • Part C: Write your formal proof in LaTeX")
            print("  • Double-check all documentation and comments")
        else:
            print("  Some tests failed. Please review the error messages above.")
            print("\nDebugging tips:")
            print("  • Read the error messages carefully")
            print("  • Check your algorithm logic against the hints")
            print("  • Verify you're using the correct cost calculation functions")
            print("  • Make sure paths are properly reconstructed")
        
        print("="*80 + "\n")
        
        return all_passed
    else:
        print("No tests were run.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)