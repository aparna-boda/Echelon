"""
Stack Data Structure Implementation

Problem Statement:
Implement a stack data structure with the following operations:
- push(item): Add an item to the top of the stack
- pop(): Remove and return the top item
- peek(): Return the top item without removing it
- is_empty(): Check if stack is empty
- size(): Return the number of items in the stack

Time Complexity: All operations O(1)
Space Complexity: O(n) where n is number of elements
"""

from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')


class StackEmptyError(Exception):
    """Exception raised when attempting to pop from an empty stack."""
    pass


class Stack(Generic[T]):
    """
    A generic stack implementation using a list.
    
    Attributes:
        _items: Internal list to store stack elements
    """
    
    def __init__(self) -> None:
        """Initialize an empty stack."""
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        """
        Add an item to the top of the stack.
        
        Args:
            item: The item to push onto the stack
        """
        self._items.append(item)
    
    def pop(self) -> T:
        """
        Remove and return the top item from the stack.
        
        Returns:
            The item at the top of the stack
            
        Raises:
            StackEmptyError: If the stack is empty
        """
        if self.is_empty():
            raise StackEmptyError("Cannot pop from an empty stack")
        return self._items.pop()
    
    def peek(self) -> T:
        """
        Return the top item without removing it.
        
        Returns:
            The item at the top of the stack
            
        Raises:
            StackEmptyError: If the stack is empty
        """
        if self.is_empty():
            raise StackEmptyError("Cannot peek at an empty stack")
        return self._items[-1]
    
    def is_empty(self) -> bool:
        """
        Check if the stack is empty.
        
        Returns:
            True if the stack is empty, False otherwise
        """
        return len(self._items) == 0
    
    def size(self) -> int:
        """
        Get the number of items in the stack.
        
        Returns:
            The number of items in the stack
        """
        return len(self._items)
    
    def clear(self) -> None:
        """Remove all items from the stack."""
        self._items.clear()
    
    def __str__(self) -> str:
        """String representation of the stack."""
        return f"Stack({self._items})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the stack."""
        return f"Stack(size={self.size()}, items={self._items})"
    
    def __len__(self) -> int:
        """Enable len() function on stack."""
        return self.size()


def is_balanced_parentheses(expression: str) -> bool:
    """
    Check if parentheses in an expression are balanced using a stack.
    
    Args:
        expression: String containing parentheses to check
        
    Returns:
        True if parentheses are balanced, False otherwise
        
    Example:
        >>> is_balanced_parentheses("((()))")
        True
        >>> is_balanced_parentheses("(()")
        False
    """
    stack = Stack[str]()
    opening = {'(', '[', '{'}
    closing = {')', ']', '}'}
    pairs = {'(': ')', '[': ']', '{': '}'}
    
    for char in expression:
        if char in opening:
            stack.push(char)
        elif char in closing:
            if stack.is_empty():
                return False
            top = stack.pop()
            if pairs[top] != char:
                return False
    
    return stack.is_empty()


def reverse_string_using_stack(text: str) -> str:
    """
    Reverse a string using a stack.
    
    Args:
        text: String to reverse
        
    Returns:
        Reversed string
    """
    stack = Stack[str]()
    
    # Push all characters onto stack
    for char in text:
        stack.push(char)
    
    # Pop all characters to build reversed string
    reversed_text = ""
    while not stack.is_empty():
        reversed_text += stack.pop()
    
    return reversed_text


# Test cases
if __name__ == "__main__":
    print("Stack Implementation Tests")
    print("=" * 70)
    
    # Test 1: Basic operations
    print("\nTest 1: Basic Stack Operations")
    stack = Stack[int]()
    
    print(f"Is empty: {stack.is_empty()}")  # True
    
    stack.push(1)
    stack.push(2)
    stack.push(3)
    print(f"After pushing 1, 2, 3: {stack}")
    print(f"Size: {stack.size()}")  # 3
    print(f"Peek: {stack.peek()}")  # 3
    
    popped = stack.pop()
    print(f"Popped: {popped}")  # 3
    print(f"After pop: {stack}")
    print(f"Size: {stack.size()}")  # 2
    
    # Test 2: String stack
    print("\nTest 2: String Stack")
    str_stack = Stack[str]()
    str_stack.push("Hello")
    str_stack.push("World")
    print(f"String stack: {str_stack}")
    print(f"Peek: {str_stack.peek()}")
    
    # Test 3: Balanced parentheses
    print("\nTest 3: Balanced Parentheses")
    test_cases = [
        ("()", True),
        ("([]{})", True),
        ("([)]", False),
        ("((()))", True),
        ("(()", False),
        ("{[()]}", True),
        ("", True),
    ]
    
    for expression, expected in test_cases:
        result = is_balanced_parentheses(expression)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{expression}' -> {result} (expected: {expected})")
    
    # Test 4: String reversal
    print("\nTest 4: String Reversal Using Stack")
    strings = ["hello", "Python", "12345", "Palindrome"]
    
    for s in strings:
        reversed_s = reverse_string_using_stack(s)
        print(f"'{s}' -> '{reversed_s}'")
    
    # Test 5: Error handling
    print("\nTest 5: Error Handling")
    empty_stack = Stack[int]()
    try:
        empty_stack.pop()
        print("✗ Should have raised StackEmptyError")
    except StackEmptyError as e:
        print(f"✓ Correctly raised exception: {e}")
    
    try:
        empty_stack.peek()
        print("✗ Should have raised StackEmptyError")
    except StackEmptyError as e:
        print(f"✓ Correctly raised exception: {e}")
    
    print("\nAll tests completed!")
