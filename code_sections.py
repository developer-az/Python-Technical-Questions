"""Module for breaking down code solutions into sections for Duolingo-style learning."""

import re
import random
from typing import List, Dict


class CodeSectionParser:
    """Parses Python code solutions into logical sections for progressive learning."""

    def __init__(self):
        self.function_patterns = [
            r"def\s+\w+\([^)]*\):",  # Function definitions
            r"if\s+[^:]+:",  # If statements
            r"for\s+[^:]+:",  # For loops
            r"while\s+[^:]+:",  # While loops
            r"try:",  # Try blocks
            r"except[^:]*:",  # Except blocks
            r"else:",  # Else blocks
            r"elif\s+[^:]+:",  # Elif blocks
        ]

    def parse_solution(self, solution: str) -> Dict:
        """
        Parse a code solution into sections for progressive learning.

        Args:
            solution: Raw solution string containing code and complexity info

        Returns:
            Dict containing parsed sections with metadata
        """
        # Separate code from complexity analysis
        lines = solution.strip().split("\n")
        code_lines = []
        complexity_lines = []

        in_complexity = False
        for line in lines:
            line = line.strip()
            if line.startswith("Time Complexity:") or line.startswith(
                "Space Complexity:"
            ):
                in_complexity = True

            if in_complexity:
                complexity_lines.append(line)
            elif line:  # Skip empty lines
                code_lines.append(line)

        # Parse code into logical sections
        sections = self._create_code_sections(code_lines)

        return {
            "sections": sections,
            "complexity_info": "\n".join(complexity_lines),
            "total_sections": len(sections),
            "complete_code": "\n".join(code_lines),
        }

    def _create_code_sections(self, code_lines: List[str]) -> List[Dict]:
        """Create logical sections from code lines."""
        sections = []
        current_section = []
        section_type = "setup"
        indent_level = 0

        for i, line in enumerate(code_lines):
            # Calculate indentation
            line_indent = len(line) - len(line.lstrip())

            # Check if this line starts a new logical section
            is_new_section = self._is_section_boundary(
                line, line_indent, indent_level, current_section
            )

            if is_new_section and current_section:
                # Finish current section
                sections.append(
                    self._create_section_dict(
                        current_section, section_type, len(sections)
                    )
                )
                current_section = []
                section_type = self._determine_section_type(line)
                indent_level = line_indent

            current_section.append(line)

            # Update section type based on content
            if not section_type or section_type == "setup":
                section_type = self._determine_section_type(line)

        # Add final section
        if current_section:
            sections.append(
                self._create_section_dict(current_section, section_type, len(sections))
            )

        return sections

    def _is_section_boundary(
        self, line: str, line_indent: int, prev_indent: int, current_section: List[str]
    ) -> bool:
        """Determine if a line represents a new logical section."""
        # Function definition always starts new section
        if re.match(r"def\s+\w+\([^)]*\):", line.strip()):
            return True

        # Control structures at same or lower indent start new sections
        if any(
            re.match(pattern, line.strip()) for pattern in self.function_patterns[1:]
        ):
            return line_indent <= prev_indent or len(current_section) > 3

        # Return statements often end sections
        if line.strip().startswith("return") and len(current_section) > 2:
            return False  # Include return in current section

        return False

    def _determine_section_type(self, line: str) -> str:
        """Determine the type of code section based on the line."""
        line = line.strip()

        if re.match(r"def\s+\w+\([^)]*\):", line):
            return "function_def"
        elif re.match(r"if\s+[^:]+:", line):
            return "conditional"
        elif re.match(r"for\s+[^:]+:", line):
            return "loop"
        elif re.match(r"while\s+[^:]+:", line):
            return "loop"
        elif "return" in line:
            return "return"
        elif "=" in line and not any(op in line for op in ["==", "!=", "<=", ">="]):
            return "assignment"
        else:
            return "logic"

    def _create_section_dict(
        self, lines: List[str], section_type: str, index: int
    ) -> Dict:
        """Create a section dictionary with metadata."""
        code = "\n".join(lines)

        return {
            "index": index,
            "type": section_type,
            "code": code,
            "lines": lines,
            "description": self._generate_section_description(lines, section_type),
            "key_concepts": self._extract_key_concepts(lines, section_type),
        }

    def _generate_section_description(self, lines: List[str], section_type: str) -> str:
        """Generate a human-readable description of the code section."""
        if section_type == "function_def":
            return "Function definition and parameters"
        elif section_type == "conditional":
            return "Conditional logic (if/else)"
        elif section_type == "loop":
            return "Loop iteration"
        elif section_type == "return":
            return "Return statement"
        elif section_type == "assignment":
            return "Variable assignment"
        else:
            return "Core logic"

    def _extract_key_concepts(self, lines: List[str], section_type: str) -> List[str]:
        """Extract key programming concepts from the section."""
        concepts = []
        code = "\n".join(lines).lower()

        # Common patterns
        if "hash" in code or "dict" in code or "{}" in code:
            concepts.append("Hash Map/Dictionary")
        if "for" in code and "enumerate" in code:
            concepts.append("Enumeration")
        if "if" in code and "in" in code:
            concepts.append("Membership Testing")
        if "return" in code:
            concepts.append("Return Values")
        if "max" in code or "min" in code:
            concepts.append("Min/Max Operations")
        if "len(" in code:
            concepts.append("Length Operations")

        return concepts


class MultipleChoiceGenerator:
    """Generates multiple choice options for code sections."""

    def __init__(self):
        self.common_distractors = {
            "function_def": [
                "def solution(arr, val):",
                "def solve(input_array, target_value):",
                "def algorithm(data, search_key):",
            ],
            "assignment": [
                "result = []",
                "output = {}",
                "answer = None",
                "temp = 0",
            ],
            "conditional": [
                "if item != target:",
                "if value > threshold:",
                "if not found:",
                "if element < minimum:",
            ],
            "loop": [
                "for item in collection:",
                "for val in range(n):",
                "for element in sorted(data):",
            ],
            "return": [
                "return result",
                "return output",
                "return answer",
                "return None",
            ],
        }

    def generate_choices(
        self, correct_section: Dict, all_sections: List[Dict]
    ) -> List[Dict]:
        """
        Generate multiple choice options for a code section.

        Args:
            correct_section: The correct section dict
            all_sections: All sections from the solution for context

        Returns:
            List of choice dicts with 'text', 'is_correct', and 'explanation'
        """
        choices = []
        # section_type = correct_section["type"]
        correct_code = correct_section["code"]

        # Add the correct choice
        choices.append(
            {
                "text": correct_code,
                "is_correct": True,
                "explanation": f"Correct! This {correct_section['description'].lower()}.",
            }
        )

        # Generate distractors based on section type
        distractors = self._generate_distractors(correct_section, all_sections)

        # Add distractors, ensuring we have enough
        added_distractors = 0
        for distractor in distractors:
            if added_distractors >= 3:  # Max 3 distractors
                break
            choices.append(
                {
                    "text": distractor["code"],
                    "is_correct": False,
                    "explanation": distractor["explanation"],
                }
            )
            added_distractors += 1

        # If we don't have enough distractors, add generic ones
        while len(choices) < 4:
            generic_distractor = self._generate_generic_distractor(
                correct_section, len(choices)
            )
            choices.append(
                {
                    "text": generic_distractor["code"],
                    "is_correct": False,
                    "explanation": generic_distractor["explanation"],
                }
            )

        # Shuffle choices so correct answer isn't always first
        random.shuffle(choices)

        return choices

    def _generate_distractors(
        self, correct_section: Dict, all_sections: List[Dict]
    ) -> List[Dict]:
        """Generate distractor options that are plausible but incorrect."""
        distractors = []
        section_type = correct_section["type"]
        # correct_lines = correct_section["lines"]

        # Type 1: Common wrong approaches for this section type
        if section_type in self.common_distractors:
            for wrong_code in self.common_distractors[section_type]:
                distractors.append(
                    {
                        "code": wrong_code,
                        "explanation": "This is a common alternative approach, but not correct for this specific problem.",
                    }
                )

        # Type 2: Modify the correct code with common mistakes
        distractors.extend(self._create_modified_versions(correct_section))

        # Type 3: Use similar code from other sections (if applicable)
        distractors.extend(
            self._create_section_variations(correct_section, all_sections)
        )

        return distractors

    def _create_modified_versions(self, section: Dict) -> List[Dict]:
        """Create modified versions of the correct code with common mistakes."""
        distractors = []
        code = section["code"]

        # Common Python mistakes
        if "in" in code and "hash_map" in code:
            wrong_code = code.replace("in hash_map", "== hash_map")
            distractors.append(
                {
                    "code": wrong_code,
                    "explanation": "This uses equality (==) instead of membership testing (in).",
                }
            )

        if "enumerate" in code:
            wrong_code = code.replace("enumerate(", "range(len(")
            if wrong_code != code:
                distractors.append(
                    {
                        "code": wrong_code,
                        "explanation": "This uses range(len()) instead of enumerate, making index access more complex.",
                    }
                )

        if "[" in code and "]" in code and "hash_map" in code:
            wrong_code = code.replace(
                "[hash_map[complement], i]", "[i, hash_map[complement]]"
            )
            if wrong_code != code:
                distractors.append(
                    {
                        "code": wrong_code,
                        "explanation": "This returns indices in wrong order.",
                    }
                )

        return distractors

    def _create_section_variations(
        self, section: Dict, all_sections: List[Dict]
    ) -> List[Dict]:
        """Create variations by adapting code from other sections."""
        distractors = []

        # This is a simplified approach - in a real implementation,
        # you'd want more sophisticated code transformation
        for other_section in all_sections:
            if (
                other_section["index"] != section["index"]
                and other_section["type"] == section["type"]
                and len(other_section["lines"]) <= len(section["lines"]) + 2
            ):

                distractors.append(
                    {
                        "code": other_section["code"],
                        "explanation": f"This code belongs to a different part of the solution.",
                    }
                )

        return distractors

    def _generate_generic_distractor(self, section: Dict, choice_number: int) -> Dict:
        """Generate a generic distractor when we don't have enough specific ones."""
        section_type = section["type"]

        generic_options = {
            "function_def": [
                "def helper_function():",
                "def utility_method(data):",
                "def process_input(values):",
            ],
            "assignment": [
                "temp_var = None",
                "counter = 0",
                "result_list = []",
            ],
            "conditional": [
                "if condition:",
                "if not valid:",
                "if found_match:",
            ],
            "loop": [
                "for item in items:",
                "for idx, val in enumerate(data):",
                "for x in range(n):",
            ],
            "return": [
                "return False",
                "return []",
                "return -1",
            ],
            "logic": [
                "# Process data here",
                "pass",
                "continue",
            ],
        }

        # Get appropriate generic options for this section type
        options = generic_options.get(section_type, generic_options["logic"])

        # Choose based on choice number to ensure variety
        selected_option = options[choice_number % len(options)]

        return {
            "code": selected_option,
            "explanation": "This is not the correct code for this specific section of the solution.",
        }
