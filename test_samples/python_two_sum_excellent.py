"""
Two Sum Problem - Optimized Solution

Problem Statement:
Given an array of integers nums and an integer target, return indices of the 
two numbers such that they add up to target. You may assume that each input 
would have exactly one solution, and you may not use the same element twice.

Example:
    Input: nums = [2, 7, 11, 15], target = 9
    Output: [0, 1]
    Explanation: nums[0] + nums[1] == 9, so we return [0, 1]

Time Complexity: O(n)
Space Complexity: O(n)
"""

from typing import List, Optional


def two_sum(nums: List[int], target: int) -> Optional[List[int]]:
    """
    Find two numbers in array that sum to target using hash map approach.
    
    Args:
        nums: List of integers to search
        target: Target sum to find
        
    Returns:
        List containing indices of two numbers that sum to target,
        or None if no solution exists
        
    Raises:
        ValueError: If nums is empty or None
    """
    if not nums:
        raise ValueError("Input array cannot be empty")
    
    # Hash map to store number -> index mapping
    seen = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        
        # Check if complement exists in hash map
        if complement in seen:
            return [seen[complement], i]
        
        # Store current number and its index
        seen[num] = i
    
    return None


def validate_solution(nums: List[int], target: int, result: Optional[List[int]]) -> bool:
    """
    Validate that the solution is correct.
    
    Args:
        nums: Original input array
        target: Target sum
        result: Indices returned by two_sum
        
    Returns:
        True if solution is valid, False otherwise
    """
    if result is None or len(result) != 2:
        return False
    
    i, j = result
    return nums[i] + nums[j] == target


# Test cases
if __name__ == "__main__":
    test_cases = [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),
        ([3, 3], 6, [0, 1]),
        ([1, 5, 3, 7, 9], 12, [2, 4]),
    ]
    
    print("Running Two Sum Tests...")
    for nums, target, expected in test_cases:
        result = two_sum(nums, target)
        is_valid = validate_solution(nums, target, result)
        status = "✓" if is_valid and result == expected else "✗"
        print(f"{status} two_sum({nums}, {target}) = {result}")
    
    print("\nAll tests completed!")
