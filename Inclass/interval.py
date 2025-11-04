def min_pipes(n, ranges):
    """
    Find minimum number of pipes needed to water all garden plots [0, n].
    
    Args:
        n: rightmost point to cover
        ranges: list where ranges[i] is the watering capacity of pipe at position i
    
    Returns:
        Minimum number of pipes needed, or -1 if impossible
    """
    # Step 1: Create intervals from pipes
    intervals = []
    for i in range(len(ranges)):
        left = max(0, i - ranges[i])
        right = min(n, i + ranges[i])
        # Only add intervals that actually cover something in [0, n]
        if left <= n and right >= 0:
            intervals.append((left, right))
    
    # Step 2: Sort intervals by start point
    intervals.sort(key=lambda x: x[0])
    
    # If no intervals or first interval doesn't start at or before 0, impossible
    if not intervals or intervals[0][0] > 0:
        return -1
    
    # Step 3: Greedily select intervals
    watered = 0  
    count = 0    # number of pipes used
    i = 0        # current index in intervals
    
    while watered <= n:
        # ToDO: Implement the greedy selection of intervals here. 
    
    return count


# Test cases
if __name__ == "__main__":
    # Example 1: Simple case - each pipe at position i with range 0 covers only [i, i]
    print("Test 1:", min_pipes(3, [0, 0, 0, 0]))  
    
    # Example 2: Overlapping coverage
    print("Test 2:", min_pipes(5, [1, 2, 1, 0, 2, 1]))
    
    # Example 3: Impossible case
    print("Test 3:", min_pipes(10, [1, 0, 1]))  
    
    # Example 4: Better test - pipes with good coverage
    print("Test 4:", min_pipes(5, [3, 0, 0, 0, 0, 3])) 