"""
Two Sum Problem — Excellent Solution

Given an array of integers nums and an integer target,
return indices of the two numbers that add up to target.
"""

from typing import Optional


def two_sum(nums: list[int], target: int) -> Optional[list[int]]:
    """Find two indices whose values sum to target.

    Uses a hash map for O(n) time complexity.

    Args:
        nums: List of integers.
        target: Target sum.

    Returns:
        List of two indices, or None if no solution exists.

    Raises:
        TypeError: If inputs are not the expected types.
    """
    if not isinstance(nums, list) or not isinstance(target, int):
        raise TypeError("nums must be a list and target must be an int")

    if len(nums) < 2:
        return None

    seen: dict[int, int] = {}

    for index, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            return [seen[complement], index]
        seen[value] = index

    return None


def test_two_sum_basic():
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]


def test_two_sum_middle():
    assert two_sum([3, 2, 4], 6) == [1, 2]


def test_two_sum_duplicates():
    assert two_sum([3, 3], 6) == [0, 1]


def test_two_sum_negatives():
    assert two_sum([-1, -2, -3, -4, -5], -8) == [2, 4]


def test_two_sum_no_solution():
    assert two_sum([1, 2, 3], 100) is None


def test_two_sum_empty():
    assert two_sum([], 5) is None


def test_two_sum_single():
    assert two_sum([5], 5) is None


if __name__ == "__main__":
    test_two_sum_basic()
    test_two_sum_middle()
    test_two_sum_duplicates()
    test_two_sum_negatives()
    test_two_sum_no_solution()
    test_two_sum_empty()
    test_two_sum_single()
    print("All tests passed!")
