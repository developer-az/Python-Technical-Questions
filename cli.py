import argparse


def load_questions():
    """Load sample coding questions."""
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
        },
        {
            "id": 2,
            "title": "Fibonacci Sequence",
            "difficulty": "Easy",
            "description": "Calculate the nth Fibonacci number.",
            "example": "Input: n = 5\\nOutput: 5 (sequence: 0,1,1,2,3,5)",
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
