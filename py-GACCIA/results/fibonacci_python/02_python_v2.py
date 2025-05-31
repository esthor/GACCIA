```python
from typing import List
from pydantic import BaseModel, Field, PositiveInt, conint, ValidationError


class FibonacciResult(BaseModel):
    """
    Represents the result of a Fibonacci calculation.
    """
    index: int = Field(..., ge=0, description="The position in the Fibonacci sequence (non-negative integer).")
    value: int = Field(..., description="The nth Fibonacci number.")


def fibonacci(n: int) -> int:
    """
    Calculates the nth Fibonacci number using recursion.

    Args:
        n (int): The position in the Fibonacci sequence (must be a non-negative integer).

    Returns:
        int: The nth Fibonacci number.

    Raises:
        ValueError: If n is negative or not an integer.

    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(5)
        5
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer")
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def run_fibonacci_demo(start: int = 0, end: int = 10) -> List[FibonacciResult]:
    """
    Runs a demonstration of the recursive Fibonacci function for a range of values.

    Args:
        start (int, optional): The starting index (inclusive, default 0).
        end (int, optional): The ending index (exclusive, default 10).

    Returns:
        List[FibonacciResult]: A list of FibonacciResult objects for each calculated index.

    Raises:
        ValueError: If start or end are not valid non-negative integers,
                    or if end is not greater than start.
    """
    if not isinstance(start, int) or start < 0:
        raise ValueError("Start must be a non-negative integer")
    if not isinstance(end, int) or end <= start:
        raise ValueError("End must be an integer greater than start")

    results: List[FibonacciResult] = []
    for i in range(start, end):
        result = FibonacciResult(index=i, value=fibonacci(i))
        results.append(result)
    return results


if __name__ == "__main__":
    for result in run_fibonacci_demo(0, 10):
        print(f"fib({result.index}) = {result.value}")
```