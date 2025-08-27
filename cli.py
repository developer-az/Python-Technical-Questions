import argparse


def load_questions():
    """Load sample coding questions with solutions."""
    return [
        {
            "id": 1,
            "title": "Two Sum",
            "difficulty": "Easy",
            "description": (
                "Given an array of integers, return indices of the "
                "two numbers such that they add up to a specific target."
            ),
            "example": "Input: nums = [2,7,11,15], target = 9\\nOutput: [0,1]",
            "solutions": [
                {
                    "id": 1,
                    "title": "Hash Map Solution",
                    "description": "Use a hash map to store complements",
                    "code": """def two_sum(nums, target):
    # Create a hash map to store complements
    seen = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        
        # If complement exists in hash map, we found our pair
        if complement in seen:
            return [seen[complement], i]
        
        # Store current number and its index
        seen[num] = i
    
    return []  # No solution found

# Test cases
print(two_sum([2, 7, 11, 15], 9))  # Output: [0, 1]
print(two_sum([3, 2, 4], 6))       # Output: [1, 2]
print(two_sum([3, 3], 6))          # Output: [0, 1]""",
                    "time_complexity": "O(n)",
                    "space_complexity": "O(n)",
                    "approach": "Hash Map"
                },
                {
                    "id": 2,
                    "title": "Brute Force Solution",
                    "description": "Check all possible pairs",
                    "code": """def two_sum_brute_force(nums, target):
    n = len(nums)
    
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    
    return []  # No solution found

# Test cases
print(two_sum_brute_force([2, 7, 11, 15], 9))  # Output: [0, 1]
print(two_sum_brute_force([3, 2, 4], 6))       # Output: [1, 2]
print(two_sum_brute_force([3, 3], 6))          # Output: [0, 1]""",
                    "time_complexity": "O(n²)",
                    "space_complexity": "O(1)",
                    "approach": "Brute Force"
                }
            ]
        },
        {
            "id": 2,
            "title": "Fibonacci Sequence",
            "difficulty": "Easy",
            "description": "Calculate the nth Fibonacci number.",
            "example": "Input: n = 5\\nOutput: 5 (sequence: 0,1,1,2,3,5)",
            "solutions": [
                {
                    "id": 1,
                    "title": "Recursive Solution",
                    "description": "Simple recursive approach",
                    "code": """def fibonacci_recursive(n):
    # Base cases
    if n <= 1:
        return n
    
    # Recursive case
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

# Test cases
print(fibonacci_recursive(5))   # Output: 5
print(fibonacci_recursive(8))   # Output: 21
print(fibonacci_recursive(10))  # Output: 55""",
                    "time_complexity": "O(2^n)",
                    "space_complexity": "O(n)",
                    "approach": "Recursion"
                },
                {
                    "id": 2,
                    "title": "Dynamic Programming Solution",
                    "description": "Optimized with memoization",
                    "code": """def fibonacci_dp(n):
    # Base cases
    if n <= 1:
        return n
    
    # Initialize DP array
    dp = [0] * (n + 1)
    dp[1] = 1
    
    # Fill DP array
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]

# Test cases
print(fibonacci_dp(5))   # Output: 5
print(fibonacci_dp(8))   # Output: 21
print(fibonacci_dp(10))  # Output: 55""",
                    "time_complexity": "O(n)",
                    "space_complexity": "O(n)",
                    "approach": "Dynamic Programming"
                },
                {
                    "id": 3,
                    "title": "Space Optimized Solution",
                    "description": "Use only two variables",
                    "code": """def fibonacci_optimized(n):
    # Base cases
    if n <= 1:
        return n
    
    # Use only two variables
    prev, curr = 0, 1
    
    for i in range(2, n + 1):
        prev, curr = curr, prev + curr
    
    return curr

# Test cases
print(fibonacci_optimized(5))   # Output: 5
print(fibonacci_optimized(8))   # Output: 21
print(fibonacci_optimized(10))  # Output: 55""",
                    "time_complexity": "O(n)",
                    "space_complexity": "O(1)",
                    "approach": "Space Optimized"
                }
            ]
        },
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Python Technical Questions Practice Tool"
    )
    parser.add_argument(
        "--list", action="store_true", help="List all available questions"
    )
    parser.add_argument(
        "--question",
        type=int,
        help="Show specific question by ID",
    )
    args = parser.parse_args()

    questions = load_questions()

    if args.list:
        print("Available Questions:")
        for q in questions:
            print(f"  {q['id']}: {q['title']} ({q['difficulty']})")
    elif args.question:
        question = next(
            (q for q in questions if q["id"] == args.question),
            None,
        )
        if question:
            print(f"Question {question['id']}: {question['title']}")
            print(f"Difficulty: {question['difficulty']}")
            print(f"Description: {question['description']}")
            print(f"Example: {question['example']}")
        else:
            print(f"Question {args.question} not found")
    else:
        print("Python Technical Questions Practice Tool")
        print("Use --help for available options")


if __name__ == "__main__":
    main()
