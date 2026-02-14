"""
Fibonacci Sequence - Optimized Implementation

Problem Statement:
Write a function that returns the nth Fibonacci number. The Fibonacci 
sequence is defined as: F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2) for n > 1.

Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import Dict


def fibonacci_iterative(n: int) -> int:
    """
    Calculate nth Fibonacci number using iterative approach.
    
    This is the most space-efficient solution with O(1) space complexity.
    
    Args:
        n: Position in Fibonacci sequence (0-indexed)
        
    Returns:
        The nth Fibonacci number
        
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if n <= 1:
        return n
    
    prev, curr = 0, 1
    
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    
    return curr


def fibonacci_memoized(n: int, memo: Dict[int, int] = None) -> int:
    """
    Calculate nth Fibonacci number using memoization.
    
    This provides O(n) time complexity with O(n) space for the memo.
    
    Args:
        n: Position in Fibonacci sequence (0-indexed)
        memo: Dictionary for caching computed values
        
    Returns:
        The nth Fibonacci number
    """
    if memo is None:
        memo = {}
    
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if n <= 1:
        return n
    
    if n not in memo:
        memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    
    return memo[n]


def fibonacci_sequence(count: int) -> list:
    """
    Generate the first 'count' Fibonacci numbers.
    
    Args:
        count: Number of Fibonacci numbers to generate
        
    Returns:
        List of the first 'count' Fibonacci numbers
    """
    if count <= 0:
        return []
    
    if count == 1:
        return [0]
    
    sequence = [0, 1]
    
    for i in range(2, count):
        sequence.append(sequence[i - 1] + sequence[i - 2])
    
    return sequence


# Test cases
if __name__ == "__main__":
    print("Fibonacci Sequence Tests\n" + "=" * 50)
    
    # Test individual values
    test_values = [0, 1, 5, 10, 15, 20]
    
    print("\nIterative Implementation:")
    for n in test_values:
        result = fibonacci_iterative(n)
        print(f"F({n:2d}) = {result:6d}")
    
    print("\nMemoized Implementation:")
    for n in test_values:
        result = fibonacci_memoized(n)
        print(f"F({n:2d}) = {result:6d}")
    
    print("\nFirst 15 Fibonacci numbers:")
    print(fibonacci_sequence(15))
    
    # Performance comparison
    print("\nPerformance Test (n=30):")
    import time
    
    start = time.time()
    result_iter = fibonacci_iterative(30)
    time_iter = time.time() - start
    
    start = time.time()
    result_memo = fibonacci_memoized(30)
    time_memo = time.time() - start
    
    print(f"Iterative: {result_iter} (Time: {time_iter*1000:.4f}ms)")
    print(f"Memoized:  {result_memo} (Time: {time_memo*1000:.4f}ms)")
