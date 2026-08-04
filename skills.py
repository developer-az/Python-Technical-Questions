"""Skill and method taxonomy for progressive interview training.

Hierarchy (gym / sports form metaphor):
  Pillar  →  Skill  →  Method  →  Problem (reps)

Clicking a method on a problem drills up to the parent skill,
then the pillar — each level aggregates techniques and reps.
"""

from __future__ import annotations

from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Taxonomy
# ---------------------------------------------------------------------------

PILLARS: Dict[str, Dict] = {
    "fundamentals": {
        "id": "fundamentals",
        "name": "Fundamentals",
        "tagline": "Scan, store, and rearrange data under pressure",
        "description": (
            "The base layer of interview form: hash maps, two pointers, "
            "windows, and greedy scans. Master these before stacking "
            "heavier patterns on top."
        ),
        "skill_ids": ["array_patterns", "string_patterns"],
    },
    "structures": {
        "id": "structures",
        "name": "Data Structures",
        "tagline": "Move through lists and trees with intent",
        "description": (
            "Pointer gymnastics on linked lists, traversal discipline on "
            "trees, and stack discipline for nesting. Form here is about "
            "knowing where you are in the structure at every step."
        ),
        "skill_ids": ["linked_list_patterns", "tree_patterns", "stack_patterns"],
    },
    "algorithms": {
        "id": "algorithms",
        "name": "Algorithms",
        "tagline": "Compose optimal decisions from subproblems",
        "description": (
            "Dynamic programming and related decision frameworks. "
            "These are compound lifts — they assume you already own "
            "the fundamentals of scanning and state tracking."
        ),
        "skill_ids": ["dp_patterns"],
    },
}

SKILLS: Dict[str, Dict] = {
    "array_patterns": {
        "id": "array_patterns",
        "name": "Array Patterns",
        "pillar_id": "fundamentals",
        "description": (
            "Index-based scanning techniques: complement lookup, "
            "converging pointers, prefix/suffix products, and single-pass "
            "greedy tracking."
        ),
        "method_ids": [
            "hash_map",
            "two_pointers",
            "prefix_products",
            "greedy_scan",
        ],
    },
    "string_patterns": {
        "id": "string_patterns",
        "name": "String Patterns",
        "pillar_id": "fundamentals",
        "description": (
            "Character-level form: cleaning while scanning, window "
            "expansion/contraction, anagram grouping, and bracket matching."
        ),
        "method_ids": [
            "two_pointers",
            "sliding_window",
            "hash_map",
            "stack",
            "sorting",
        ],
    },
    "linked_list_patterns": {
        "id": "linked_list_patterns",
        "name": "Linked List Patterns",
        "pillar_id": "structures",
        "description": (
            "Pointer rewiring, sorted merges, and cycle detection. "
            "Every move should leave the list in a known state."
        ),
        "method_ids": [
            "linked_list_reverse",
            "merge_lists",
            "floyd_cycle",
            "two_pointers",
        ],
    },
    "tree_patterns": {
        "id": "tree_patterns",
        "name": "Tree Patterns",
        "pillar_id": "structures",
        "description": (
            "Recursive DFS, level-order BFS, and BST invariant checks. "
            "Build the habit of stating what each call returns."
        ),
        "method_ids": ["dfs_recursion", "bfs_level_order", "bst_invariants"],
    },
    "stack_patterns": {
        "id": "stack_patterns",
        "name": "Stack Patterns",
        "pillar_id": "structures",
        "description": (
            "LIFO discipline for nesting and deferred matching. "
            "Push when you open a problem; pop when you resolve it."
        ),
        "method_ids": ["stack"],
    },
    "dp_patterns": {
        "id": "dp_patterns",
        "name": "Dynamic Programming",
        "pillar_id": "algorithms",
        "description": (
            "Define state, recurrence, and base cases before coding. "
            "1D and 2D tables, then strip space when the recurrence allows."
        ),
        "method_ids": ["dp_1d", "dp_2d", "space_optimization"],
    },
}

METHODS: Dict[str, Dict] = {
    "hash_map": {
        "id": "hash_map",
        "name": "Hash Map Lookup",
        "summary": "Trade space for O(1) complement / grouping lookups",
        "form_cues": [
            "Decide the key you will look up later before the loop",
            "Store the value you need on the answer path (index, count, list)",
            "Check the map before inserting when order matters",
        ],
        "parent_skill_ids": ["array_patterns", "string_patterns"],
    },
    "two_pointers": {
        "id": "two_pointers",
        "name": "Two Pointers",
        "summary": "Converge or walk dual indices instead of nested loops",
        "form_cues": [
            "Sort first when the problem cares about values, not indices",
            "Move the pointer that repairs the invariant (too small / too big)",
            "Skip duplicates deliberately when uniqueness is required",
        ],
        "parent_skill_ids": [
            "array_patterns",
            "string_patterns",
            "linked_list_patterns",
        ],
    },
    "sliding_window": {
        "id": "sliding_window",
        "name": "Sliding Window",
        "summary": "Expand and contract a contiguous range while tracking state",
        "form_cues": [
            "Name the window invariant out loud (e.g. all unique chars)",
            "Expand with the right pointer; shrink with the left",
            "Update the answer whenever the window is valid",
        ],
        "parent_skill_ids": ["string_patterns"],
    },
    "prefix_products": {
        "id": "prefix_products",
        "name": "Prefix / Suffix Products",
        "summary": "Precompute left and right aggregates to avoid division",
        "form_cues": [
            "First pass builds left-only products into the result",
            "Second pass multiplies by a running right product",
            "Watch the identity element (1 for products, 0 for sums)",
        ],
        "parent_skill_ids": ["array_patterns"],
    },
    "greedy_scan": {
        "id": "greedy_scan",
        "name": "Greedy Single Pass",
        "summary": "Track a running extremum and update the answer in one scan",
        "form_cues": [
            "Identify the one piece of history you must remember",
            "Update that history before or after the answer — be consistent",
            "Prove a later choice never needs discarded history",
        ],
        "parent_skill_ids": ["array_patterns"],
    },
    "stack": {
        "id": "stack",
        "name": "Stack Matching",
        "summary": "Push openings, pop on closings, reject mismatches",
        "form_cues": [
            "Map every closer to its opener",
            "Empty stack on a closer is always wrong",
            "Non-empty stack at the end means unmatched openers",
        ],
        "parent_skill_ids": ["stack_patterns", "string_patterns"],
    },
    "sorting": {
        "id": "sorting",
        "name": "Sorting as Preprocess",
        "summary": "Impose order so equal items cluster or pointers can move",
        "form_cues": [
            "Ask whether relative order of originals must be preserved",
            "Use sorted keys for grouping when values are permutations",
            "Sorting often unlocks two-pointer follow-ups",
        ],
        "parent_skill_ids": ["string_patterns"],
    },
    "linked_list_reverse": {
        "id": "linked_list_reverse",
        "name": "In-place List Reverse",
        "summary": "Rewire next pointers with three references: prev, curr, next",
        "form_cues": [
            "Save next before you overwrite curr.next",
            "Advance prev and curr together after the rewire",
            "Return prev — it is the new head",
        ],
        "parent_skill_ids": ["linked_list_patterns"],
    },
    "merge_lists": {
        "id": "merge_lists",
        "name": "Merge Sorted Lists",
        "summary": "Walk two sorted chains and always take the smaller head",
        "form_cues": [
            "Use a dummy head so you never special-case the first node",
            "Advance only the list you took from",
            "Attach the remaining tail in one shot",
        ],
        "parent_skill_ids": ["linked_list_patterns"],
    },
    "floyd_cycle": {
        "id": "floyd_cycle",
        "name": "Floyd Cycle Detection",
        "summary": "Slow/fast pointers find a cycle; reset finds the entrance",
        "form_cues": [
            "Fast moves 2, slow moves 1 — meeting proves a cycle",
            "Reset one pointer to head; same speed finds the entrance",
            "Null-check fast and fast.next before every leap",
        ],
        "parent_skill_ids": ["linked_list_patterns"],
    },
    "dfs_recursion": {
        "id": "dfs_recursion",
        "name": "DFS Recursion",
        "summary": "Define the return value of a subtree call before coding it",
        "form_cues": [
            "Base case for null (and sometimes leaf) first",
            "Combine left and right results with a clear rule",
            "State whether the function returns a value or mutates",
        ],
        "parent_skill_ids": ["tree_patterns"],
    },
    "bfs_level_order": {
        "id": "bfs_level_order",
        "name": "BFS Level Order",
        "summary": "Process a queue level by level using size snapshots",
        "form_cues": [
            "Capture level_size = len(queue) before the inner loop",
            "Enqueue children only after dequeuing the parent",
            "One list per level keeps the answer structured",
        ],
        "parent_skill_ids": ["tree_patterns"],
    },
    "bst_invariants": {
        "id": "bst_invariants",
        "name": "BST Invariants",
        "summary": "Tighten allowed (low, high) bounds as you descend",
        "form_cues": [
            "Every node must sit strictly inside its inherited range",
            "Left child inherits (low, node.val); right inherits (node.val, high)",
            "Fail fast on the first violated bound",
        ],
        "parent_skill_ids": ["tree_patterns"],
    },
    "dp_1d": {
        "id": "dp_1d",
        "name": "1D Dynamic Programming",
        "summary": "dp[i] depends on a short window of earlier answers",
        "form_cues": [
            "Name what dp[i] means in one sentence",
            "Write base cases that make the recurrence safe",
            "Iterate in an order that fills dependencies first",
        ],
        "parent_skill_ids": ["dp_patterns"],
    },
    "dp_2d": {
        "id": "dp_2d",
        "name": "2D Dynamic Programming",
        "summary": "Table over two sequences or two changing dimensions",
        "form_cues": [
            "Rows and columns map to prefixes of each input",
            "Diagonal / left / up choices encode match vs skip",
            "Initialize the 0th row and column from base cases",
        ],
        "parent_skill_ids": ["dp_patterns"],
    },
    "space_optimization": {
        "id": "space_optimization",
        "name": "DP Space Optimization",
        "summary": "Keep only the previous row or rolling variables",
        "form_cues": [
            "If recurrence only needs dp[i-1], drop the full table",
            "Swap or copy rolling arrays carefully each iteration",
            "Confirm the answer cell still lands in the kept state",
        ],
        "parent_skill_ids": ["dp_patterns"],
    },
}

# Primary method first; additional methods are supporting techniques.
QUESTION_METHODS: Dict[int, List[str]] = {
    1: ["hash_map"],
    2: ["greedy_scan"],
    3: ["two_pointers", "sorting"],
    4: ["two_pointers"],
    5: ["linked_list_reverse"],
    6: ["dfs_recursion"],
    7: ["prefix_products"],
    8: ["two_pointers"],
    9: ["two_pointers", "greedy_scan"],
    10: ["stack"],
    11: ["sliding_window", "hash_map"],
    12: ["hash_map", "sorting"],
    13: ["merge_lists"],
    14: ["floyd_cycle", "two_pointers"],
    15: ["dfs_recursion"],
    16: ["bfs_level_order"],
    17: ["bst_invariants", "dfs_recursion"],
    18: ["dp_1d"],
    19: ["dp_1d"],
    20: ["dp_1d"],
    21: ["dp_2d", "space_optimization"],
}

# Starter code scaffolds per language for the practice IDE.
LANGUAGE_STARTERS: Dict[str, Dict[str, str]] = {
    "python": {
        "label": "Python",
        "mode": "python",
        "extension": "py",
        "comment": "#",
    },
    "javascript": {
        "label": "JavaScript",
        "mode": "javascript",
        "extension": "js",
        "comment": "//",
    },
    "java": {
        "label": "Java",
        "mode": "text/x-java",
        "extension": "java",
        "comment": "//",
    },
    "cpp": {
        "label": "C++",
        "mode": "text/x-c++src",
        "extension": "cpp",
        "comment": "//",
    },
}


def get_pillar(pillar_id: str) -> Optional[Dict]:
    return PILLARS.get(pillar_id)


def get_skill(skill_id: str) -> Optional[Dict]:
    return SKILLS.get(skill_id)


def get_method(method_id: str) -> Optional[Dict]:
    return METHODS.get(method_id)


def get_methods_for_question(question_id: int) -> List[Dict]:
    """Return method dicts (primary first) for a question."""
    ids = QUESTION_METHODS.get(question_id, [])
    return [METHODS[mid] for mid in ids if mid in METHODS]


def get_primary_method_id(question_id: int) -> Optional[str]:
    ids = QUESTION_METHODS.get(question_id, [])
    return ids[0] if ids else None


def get_questions_for_method(method_id: str, questions: List[Dict]) -> List[Dict]:
    """Filter questions that teach a given method."""
    return [q for q in questions if method_id in QUESTION_METHODS.get(q.get("id"), [])]


def get_skill_tree(questions: Optional[List[Dict]] = None) -> Dict:
    """Full tree with counts for the skills UI."""
    questions = questions or []
    q_by_id = {q["id"]: q for q in questions}

    def method_payload(method_id: str) -> Dict:
        method = METHODS[method_id]
        qids = [
            qid
            for qid, mids in QUESTION_METHODS.items()
            if method_id in mids and qid in q_by_id
        ]
        return {
            **method,
            "question_ids": qids,
            "question_count": len(qids),
            "questions": [
                {
                    "id": qid,
                    "title": q_by_id[qid]["title"],
                    "difficulty": q_by_id[qid]["difficulty"],
                    "category": q_by_id[qid].get("category"),
                }
                for qid in qids
            ],
        }

    pillars = []
    for pillar in PILLARS.values():
        skills = []
        for skill_id in pillar["skill_ids"]:
            skill = SKILLS[skill_id]
            methods = [method_payload(mid) for mid in skill["method_ids"]]
            # Unique questions across methods in this skill
            seen = set()
            skill_questions = []
            for m in methods:
                for q in m["questions"]:
                    if q["id"] not in seen:
                        seen.add(q["id"])
                        skill_questions.append(q)
            skills.append(
                {
                    **skill,
                    "methods": methods,
                    "question_count": len(skill_questions),
                    "questions": skill_questions,
                }
            )
        pillars.append(
            {
                **pillar,
                "skills": skills,
                "question_count": sum(s["question_count"] for s in skills),
            }
        )

    return {
        "pillars": pillars,
        "method_count": len(METHODS),
        "skill_count": len(SKILLS),
        "pillar_count": len(PILLARS),
    }


def get_method_detail(method_id: str, questions: List[Dict]) -> Optional[Dict]:
    """Method page payload: cues, parents, related problems, drill-up links."""
    method = METHODS.get(method_id)
    if not method:
        return None

    related = get_questions_for_method(method_id, questions)
    parents = []
    for skill_id in method["parent_skill_ids"]:
        skill = SKILLS[skill_id]
        pillar = PILLARS[skill["pillar_id"]]
        parents.append(
            {
                "skill": {
                    "id": skill["id"],
                    "name": skill["name"],
                    "description": skill["description"],
                },
                "pillar": {
                    "id": pillar["id"],
                    "name": pillar["name"],
                    "tagline": pillar["tagline"],
                },
            }
        )

    siblings = {}
    for skill_id in method["parent_skill_ids"]:
        skill = SKILLS[skill_id]
        siblings[skill_id] = [
            {
                "id": mid,
                "name": METHODS[mid]["name"],
                "summary": METHODS[mid]["summary"],
            }
            for mid in skill["method_ids"]
            if mid != method_id
        ]

    return {
        "method": method,
        "parents": parents,
        "siblings_by_skill": siblings,
        "questions": [
            {
                "id": q["id"],
                "title": q["title"],
                "difficulty": q["difficulty"],
                "category": q.get("category"),
                "primary": QUESTION_METHODS.get(q["id"], [None])[0] == method_id,
            }
            for q in related
        ],
        "question_count": len(related),
    }


def get_skill_detail(skill_id: str, questions: List[Dict]) -> Optional[Dict]:
    """Skill page payload aggregating its methods upward toward the pillar."""
    skill = SKILLS.get(skill_id)
    if not skill:
        return None

    pillar = PILLARS[skill["pillar_id"]]
    methods = []
    seen = set()
    aggregated_questions = []
    for mid in skill["method_ids"]:
        detail = get_method_detail(mid, questions)
        if not detail:
            continue
        methods.append(
            {
                "id": mid,
                "name": detail["method"]["name"],
                "summary": detail["method"]["summary"],
                "form_cues": detail["method"]["form_cues"],
                "question_count": detail["question_count"],
                "questions": detail["questions"],
            }
        )
        for q in detail["questions"]:
            if q["id"] not in seen:
                seen.add(q["id"])
                aggregated_questions.append(q)

    sibling_skills = [
        {"id": sid, "name": SKILLS[sid]["name"]}
        for sid in pillar["skill_ids"]
        if sid != skill_id
    ]

    return {
        "skill": skill,
        "pillar": {
            "id": pillar["id"],
            "name": pillar["name"],
            "tagline": pillar["tagline"],
            "description": pillar["description"],
        },
        "methods": methods,
        "questions": aggregated_questions,
        "question_count": len(aggregated_questions),
        "sibling_skills": sibling_skills,
    }


def annotate_question(question: Dict) -> Dict:
    """Attach method metadata onto a question dict (non-mutating copy fields)."""
    methods = get_methods_for_question(question["id"])
    return {
        **question,
        "methods": [
            {
                "id": m["id"],
                "name": m["name"],
                "summary": m["summary"],
                "primary": i == 0,
            }
            for i, m in enumerate(methods)
        ],
        "primary_method": (
            {
                "id": methods[0]["id"],
                "name": methods[0]["name"],
                "summary": methods[0]["summary"],
            }
            if methods
            else None
        ),
    }


def starter_template(language: str, question: Dict) -> str:
    """Generate a commented starter scaffold for the practice IDE."""
    title = question.get("title", "Problem")
    methods = get_methods_for_question(question["id"])
    method_line = ", ".join(m["name"] for m in methods) or "General"
    primary = methods[0] if methods else None
    cue = primary["form_cues"][0] if primary else "State the invariant before coding"

    if language == "javascript":
        return (
            f"// {title}\n"
            f"// Method: {method_line}\n"
            f"// Form cue: {cue}\n"
            f"// Write technique notes as // comments — they become study notes.\n\n"
            f"function solve(/* args */) {{\n"
            f"  // TODO: implement\n"
            f"  return null;\n"
            f"}}\n"
        )
    if language == "java":
        return (
            f"// {title}\n"
            f"// Method: {method_line}\n"
            f"// Form cue: {cue}\n"
            f"// Write technique notes as // comments — they become study notes.\n\n"
            f"class Solution {{\n"
            f"    public Object solve(/* args */) {{\n"
            f"        // TODO: implement\n"
            f"        return null;\n"
            f"    }}\n"
            f"}}\n"
        )
    if language == "cpp":
        return (
            f"// {title}\n"
            f"// Method: {method_line}\n"
            f"// Form cue: {cue}\n"
            f"// Write technique notes as // comments — they become study notes.\n\n"
            f"#include <bits/stdc++.h>\n"
            f"using namespace std;\n\n"
            f"class Solution {{\n"
            f"public:\n"
            f"    // TODO: implement\n"
            f"}};\n"
        )
    # python default
    return (
        f"# {title}\n"
        f"# Method: {method_line}\n"
        f"# Form cue: {cue}\n"
        f"# Write technique notes as # comments — they become study notes.\n\n"
        f"def solve(*args):\n"
        f"    # TODO: implement\n"
        f"    pass\n"
    )
