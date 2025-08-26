def fibonacci(n):
    """Calculate fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def main():
    """Test the fibonacci function."""
    for i in range(10):
        print(f"fib({i}) = {fibonacci(i)}")


if __name__ == "__main__":
    main()
