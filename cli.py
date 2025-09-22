import argparse
from questions import get_all_questions
import copy


def load_questions():
    """Load all coding questions from the questions database."""
    all_questions = get_all_questions()

    # Make a deep copy to avoid modifying the original data
    questions_copy = copy.deepcopy(all_questions)

    # Convert to the format expected by CLI (add example field from problem)
    for question in questions_copy:
        if "example" not in question and "problem" in question:
            # Extract example from problem text if it contains "Example:"
            problem_text = question["problem"]
            if "Example:" in problem_text:
                example_start = problem_text.find("Example:")
                example_text = problem_text[example_start:].split("\n\n")[0]
                question["example"] = example_text.replace("Example:\n", "").replace(
                    "Example:", ""
                )
            else:
                question["example"] = "See problem description for examples"

        # Convert solution format if needed
        if "solution" in question and "solutions" not in question:
            question["solutions"] = [
                {
                    "id": 1,
                    "title": "Solution",
                    "description": "Primary solution approach",
                    "code": question["solution"],
                    "time_complexity": "See solution comments",
                    "space_complexity": "See solution comments",
                    "approach": "Standard approach",
                }
            ]

    return questions_copy


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
            print(f"Category: {question.get('category', 'General')}")
            # Use 'problem' field if available, fallback to 'description'
            description = question.get("problem", question.get("description", ""))
            print(f"Description: {description}")
            print(f"Example: {question['example']}")
        else:
            print(f"Question {args.question} not found")
    else:
        print("Python Technical Questions Practice Tool")
        print("Use --help for available options")


if __name__ == "__main__":
    main()
