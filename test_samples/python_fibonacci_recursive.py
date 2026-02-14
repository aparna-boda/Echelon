# Fibonacci - Inefficient Recursive Implementation
# This is a poor implementation due to exponential time complexity

def fib(n):
    if n<=1:
        return n
    return fib(n-1)+fib(n-2)

# Test
print(fib(5))
print(fib(10))
print(fib(15))
# Don't try fib(40) - it will take forever!
