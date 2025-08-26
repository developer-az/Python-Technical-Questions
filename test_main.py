from main import fibonacci


def test_fibonacci_base_cases():
    """Test fibonacci base cases."""
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1


def test_fibonacci_sequence():
    """Test fibonacci sequence values."""
    assert fibonacci(5) == 5
    assert fibonacci(8) == 21
    assert fibonacci(10) == 55
