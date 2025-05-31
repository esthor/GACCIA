
/**
 * Calculates the nth Fibonacci number using recursion.
 *
 * @param n - The position in the Fibonacci sequence (must be a non-negative integer).
 * @returns The nth Fibonacci number.
 * @throws RangeError if n is negative or not an integer.
 *
 * @example
 * fibonacci(0); // 0
 * fibonacci(1); // 1
 * fibonacci(5); // 5
 */
export function fibonacci(n: number): number {
  if (!Number.isInteger(n) || n < 0) {
    throw new RangeError('Input must be a non-negative integer');
  }
  if (n < 2) {
    return n;
  }
  return fibonacci(n - 1) + fibonacci(n - 2);
}

/**
 * Result type for a calculated Fibonacci number.
 */
export interface FibonacciResult {
  index: number;
  value: number;
}

/**
 * Runs a demonstration of the recursive Fibonacci function for a range of values.
 *
 * @param start - The starting index (inclusive, default 0).
 * @param end - The ending index (exclusive, default 10).
 * @returns An array of FibonacciResult objects for each calculated index.
 */
export function runFibonacciDemo(
  start: number = 0,
  end: number = 10
): FibonacciResult[] {
  if (!Number.isInteger(start) || start < 0) {
    throw new RangeError('Start must be a non-negative integer');
  }
  if (!Number.isInteger(end) || end <= start) {
    throw new RangeError('End must be an integer greater than start');
  }
  const results: FibonacciResult[] = [];
  for (let i = start; i < end; ++i) {
    results.push({ index: i, value: fibonacci(i) });
  }
  return results;
}

// Example usage / demo (can be removed or commented out if used as a module):
if (import.meta.main ?? false) {
  for (const { index, value } of runFibonacciDemo(0, 10)) {
    // eslint-disable-next-line no-console
    console.log(`fib(${index}) = ${value}`);
  }
}
