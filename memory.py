"""Spaced-repetition memory engine for durable algorithm pattern learning.

Cognitive model this implements:
  1. Encoding   — schema + dual-code pattern cards (form the chunk)
  2. Retrieval  — active recall before re-exposure (strengthen the trace)
  3. Interleave — mix related methods (discrimination learning)
  4. Spacing    — SM-2 expanding intervals against the forgetting curve
  5. Elaboration— learner restates the invariant in their own words
  6. Transfer   — apply the chunk on a fresh problem (not rote replay)

Curriculum is data-driven: any new method/problem in skills.py / questions
automatically enters the review graph — scales without rewriting the UI.
"""

from __future__ import annotations

import json
import math
import os
import threading
import time
from typing import Dict, List, Optional, Tuple

from skills import METHODS, QUESTION_METHODS, SKILLS, get_method

PHASES = ("encode", "retrieve", "apply", "consolidate")


def _now() -> float:
    return time.time()


DEFAULT_MEMORY_PATH = None  # legacy; persistence lives in store.user_store


class MemoryStore:
    """Adapter over UserStore so session builders keep a store= API."""

    def __init__(self, path: str = None):
        # path kept for tests that pass a temp file — use isolated UserStore
        if path:
            from store import UserStore

            self._store = UserStore(path)
        else:
            from store import user_store

            self._store = user_store

    def ensure_card(self, kind: str, ref_id: str):
        return self._store.ensure_card(kind, ref_id)

    def get_card(self, kind: str, ref_id: str):
        return self._store.get_card(kind, ref_id)

    def mark_encoded(self, kind: str, ref_id: str):
        return self._store.mark_encoded(kind, ref_id)

    def review(self, kind: str, ref_id: str, rating: str):
        return self._store.review(kind, ref_id, rating)

    def save_elaboration(self, method_id: str, text: str):
        return self._store.save_elaboration(method_id, text)

    def get_elaboration(self, method_id: str):
        return self._store.get_elaboration(method_id)

    def mastery_summary(self):
        return self._store.mastery_summary()

    def method_states(self):
        return self._store.method_states()


memory_store = MemoryStore()


# ---------------------------------------------------------------------------
# Pattern encoding content (dual coding + retrieval cues)
# Extensible: add entries as new methods appear in skills.METHODS
# ---------------------------------------------------------------------------

PATTERN_CARDS: Dict[str, Dict] = {
    "hash_map": {
        "trigger": "Need a past value's index/count in O(1) while scanning once",
        "schema": "Key → remembered fact. Look up before you insert when order matters.",
        "visual": {
            "kind": "map",
            "frames": [
                {"label": "see 2", "map": "{2:0}", "action": "store"},
                {"label": "see 7, need 2", "map": "{2:0}", "action": "hit → [0,1]"},
            ],
        },
        "micro_trace": "nums=[2,7], target=9 → store 2@0 → at 7, need=2 → found",
        "failure": "Inserting before the lookup (misses self-pair rules) or using value as key when you need index",
        "retrieve_prompt": "You are scanning an array once. What do you store, and when do you look it up?",
        "retrieve_answer": "Store each number→index. Before storing, look up (target − current).",
        "transfer_hint": "Same chunk as Group Anagrams: key is the signature, value is the bucket.",
    },
    "two_pointers": {
        "trigger": "Sorted (or sortable) sequence; need a pair/window defined by two ends",
        "schema": "Left and right indices. Move the one that repairs the invariant.",
        "visual": {
            "kind": "pointers",
            "frames": [
                {"arr": "[1,2,4,7]", "L": 0, "R": 3, "note": "sum too big → R--"},
                {"arr": "[1,2,4,7]", "L": 0, "R": 2, "note": "sum too small → L++"},
            ],
        },
        "micro_trace": "sorted; L/R converge while skipping duplicates when uniqueness required",
        "failure": "Forgetting to skip duplicates, or moving both pointers on a hit",
        "retrieve_prompt": "Sum is too large with L and R on a sorted array. Which pointer moves?",
        "retrieve_answer": "Move R left (shrink the large side). Move L right when sum is too small.",
        "transfer_hint": "Same repair logic on strings (palindrome) and containers (height).",
    },
    "sliding_window": {
        "trigger": "Longest/shortest contiguous segment with a running constraint",
        "schema": "Expand right; shrink left while invariant is broken; update answer when valid.",
        "visual": {
            "kind": "window",
            "frames": [
                {"s": "a b c a", "L": 0, "R": 2, "note": "unique — expand"},
                {"s": "a b c a", "L": 1, "R": 3, "note": "dup a — shrink"},
            ],
        },
        "micro_trace": "Track counts in a map; when a count breaks the rule, advance L",
        "failure": "Updating the answer outside the valid window, or shrinking too far",
        "retrieve_prompt": "Name the three verbs of a sliding window in order.",
        "retrieve_answer": "Expand (right) → shrink (left while invalid) → update answer when valid.",
        "transfer_hint": "Constraint can be uniqueness, sum ≤ k, or at most K distinct.",
    },
    "prefix_products": {
        "trigger": "Each answer[i] depends on all other elements without division / extra O(n) maps",
        "schema": "Left-pass writes prefix; right-pass multiplies suffix.",
        "visual": {
            "kind": "prefix",
            "frames": [
                {"label": "left pass", "note": "result[i]=∏ left of i"},
                {"label": "right pass", "note": "× running ∏ right of i"},
            ],
        },
        "micro_trace": "[1,2,3,4] → left [1,1,2,6] → × right → [24,12,8,6]",
        "failure": "Off-by-one on the identity element (1 for products)",
        "retrieve_prompt": "Why two passes instead of one?",
        "retrieve_answer": "One pass can only see one side; the second folds the other side in.",
        "transfer_hint": "Prefix sums are the additive twin of this chunk.",
    },
    "greedy_scan": {
        "trigger": "Optimal choice depends on one running extremum, not future branches",
        "schema": "Remember the one fact that future decisions need; update answer as you go.",
        "visual": {
            "kind": "scan",
            "frames": [
                {"label": "min so far", "note": "history = 1 number"},
                {"label": "profit now", "note": "answer = max(answer, price−min)"},
            ],
        },
        "micro_trace": "Buy/sell stock: track min price, refresh best profit each day",
        "failure": "Keeping history you never use — means the greedy proof is unclear",
        "retrieve_prompt": "What is the single piece of history a greedy scan is allowed to keep?",
        "retrieve_answer": "Only the running extremum (or state) that the optimality proof says matters.",
        "transfer_hint": "Rain water / container problems often reduce to the same extremum scan.",
    },
    "stack": {
        "trigger": "Nesting, matching, or deferred resolution of openings",
        "schema": "Push openings; on closer, pop and match; empty stack must mean balanced.",
        "visual": {
            "kind": "stack",
            "frames": [
                {"stack": "[(]", "note": "saw ) → pop ( match"},
                {"stack": "[]", "note": "end empty → valid"},
            ],
        },
        "micro_trace": "Map closers→openers; reject on mismatch or leftover opens",
        "failure": "Not handling empty-stack pop; forgetting leftover opens at end",
        "retrieve_prompt": "When is an empty stack a failure mid-scan?",
        "retrieve_answer": "When you see a closer and there is nothing to pop — unmatched close.",
        "transfer_hint": "Monotonic stacks are the same LIFO chunk with a different push rule.",
    },
    "sorting": {
        "trigger": "Equality/order unlocks grouping or two-pointer afterward",
        "schema": "Impose order so equals cluster or pointers can move monotonically.",
        "visual": {
            "kind": "sort",
            "frames": [{"label": "unsorted", "note": "chaos"}, {"label": "sorted", "note": "equals adjacent"}],
        },
        "micro_trace": "Anagrams: sort chars → signature key; 3Sum: sort then two pointers",
        "failure": "Sorting when original indices are required without saving them",
        "retrieve_prompt": "What does sorting buy you before two pointers?",
        "retrieve_answer": "Monotonic movement: knowing which side to shrink when the sum is wrong.",
        "transfer_hint": "Sorting is a preprocess chunk — almost always paired with another method.",
    },
    "linked_list_reverse": {
        "trigger": "Need the list in opposite link direction in-place",
        "schema": "Three refs: prev, curr, next. Save next → rewire → advance.",
        "visual": {
            "kind": "list",
            "frames": [
                {"label": "save next", "note": "nxt = curr.next"},
                {"label": "rewire", "note": "curr.next = prev"},
                {"label": "advance", "note": "prev,curr = curr,nxt"},
            ],
        },
        "micro_trace": "Return prev — it is the new head when curr becomes null",
        "failure": "Losing next before overwrite; returning curr instead of prev",
        "retrieve_prompt": "Name the three references and the order of operations.",
        "retrieve_answer": "prev, curr, next — save next, rewire curr→prev, advance prev/curr.",
        "transfer_hint": "Same three-ref dance appears in reverse-k-group.",
    },
    "merge_lists": {
        "trigger": "Two (or more) already-sorted sequences must become one sorted sequence",
        "schema": "Dummy head; always take the smaller front; append the remainder.",
        "visual": {
            "kind": "merge",
            "frames": [
                {"label": "compare heads", "note": "attach smaller"},
                {"label": "tail rest", "note": "one pointer finishes"},
            ],
        },
        "micro_trace": "Dummy avoids special-casing the first node",
        "failure": "Forgetting to attach the leftover tail",
        "retrieve_prompt": "Why use a dummy head?",
        "retrieve_answer": "So the first real node is attached like every other — no null edge case.",
        "transfer_hint": "k-way merge is the same chunk with a heap of heads.",
    },
    "floyd_cycle": {
        "trigger": "Detect a cycle or find its entrance without extra memory",
        "schema": "Fast×2 / slow×1 meet ⇒ cycle; reset one to head, same speed ⇒ entrance.",
        "visual": {
            "kind": "cycle",
            "frames": [
                {"label": "meet", "note": "fast laps slow"},
                {"label": "reset", "note": "head + meet → entrance"},
            ],
        },
        "micro_trace": "Null-check fast and fast.next before every leap",
        "failure": "Returning the meeting point instead of the entrance",
        "retrieve_prompt": "After slow and fast meet, what do you do to find the entrance?",
        "retrieve_answer": "Put one pointer at head; move both one step until they meet.",
        "transfer_hint": "Same dual-speed idea finds the middle of a list.",
    },
    "dfs_recursion": {
        "trigger": "Answer for a node is a pure function of answers for its children",
        "schema": "Base null/leaf → combine left/right with a named rule → return.",
        "visual": {
            "kind": "tree",
            "frames": [
                {"label": "base", "note": "null → 0 / True"},
                {"label": "combine", "note": "f(left), f(right)"},
            ],
        },
        "micro_trace": "Max depth = 1 + max(left, right); Same tree = vals equal and children same",
        "failure": "Mutating when you meant to return; missing the null base case",
        "retrieve_prompt": "Before coding DFS, what sentence must you write?",
        "retrieve_answer": "What one call returns for a subtree (in one sentence).",
        "transfer_hint": "BST checks are DFS with tightened bounds as extra arguments.",
    },
    "bfs_level_order": {
        "trigger": "Need nodes grouped by distance from root / level by level",
        "schema": "Queue; snapshot level_size; drain that many; enqueue children.",
        "visual": {
            "kind": "bfs",
            "frames": [
                {"label": "size=n", "note": "freeze level width"},
                {"label": "drain n", "note": "collect; push kids"},
            ],
        },
        "micro_trace": "One list per level keeps structure without a depth argument",
        "failure": "Not snapshotting size — levels bleed together",
        "retrieve_prompt": "Why capture len(queue) before the inner loop?",
        "retrieve_answer": "So you only process the nodes that belonged to this level at start.",
        "transfer_hint": "Shortest path in unweighted graphs is the same BFS chunk.",
    },
    "bst_invariants": {
        "trigger": "Validate or search under binary-search-tree ordering rules",
        "schema": "Each node must lie in (low, high); left gets (low, val); right gets (val, high).",
        "visual": {
            "kind": "bounds",
            "frames": [
                {"label": "node 5", "note": "(-∞, ∞)"},
                {"label": "left 3", "note": "(-∞, 5)"},
                {"label": "right 7", "note": "(5, ∞)"},
            ],
        },
        "micro_trace": "Fail fast on the first violated bound",
        "failure": "Using ≤/≥ inconsistently with problem's duplicate policy",
        "retrieve_prompt": "What bounds does the right child inherit?",
        "retrieve_answer": "(node.val, high) — everything right must be greater than node.",
        "transfer_hint": "Insert/delete in a BST is the same bound walk with mutation.",
    },
    "dp_1d": {
        "trigger": "Optimal answer at i depends on a short window of earlier answers",
        "schema": "Name dp[i] → write base cases → recurrence → iterate dependency order.",
        "visual": {
            "kind": "dp1",
            "frames": [
                {"label": "dp[i]", "note": "meaning in one sentence"},
                {"label": "recurrence", "note": "from dp[i-1]…"},
            ],
        },
        "micro_trace": "Climb stairs: dp[i]=dp[i-1]+dp[i-2]",
        "failure": "Iterating before bases exist; unclear dp meaning",
        "retrieve_prompt": "What are the three sentences you write before any DP code?",
        "retrieve_answer": "State meaning, base cases, recurrence (and iteration order).",
        "transfer_hint": "House Robber / Coin Change share this 1D chunk with different recurrences.",
    },
    "dp_2d": {
        "trigger": "Two sequences / two changing dimensions define the state",
        "schema": "dp[i][j] over prefixes; match → diagonal+1; else max/min of skip options.",
        "visual": {
            "kind": "dp2",
            "frames": [
                {"label": "cell", "note": "prefixes i,j"},
                {"label": "match", "note": "diag+1 else max(L,U)"},
            ],
        },
        "micro_trace": "LCS: equal chars take diagonal; else max(left, up)",
        "failure": "Wrong initialization of 0th row/col",
        "retrieve_prompt": "In LCS, when do you take the diagonal?",
        "retrieve_answer": "When text1[i-1]==text2[j-1] — extend the common subsequence.",
        "transfer_hint": "Edit distance is the same table with different cell costs.",
    },
    "space_optimization": {
        "trigger": "Recurrence only needs the previous row/a few scalars",
        "schema": "Keep rolling state; swap carefully; confirm answer cell still lands in kept state.",
        "visual": {
            "kind": "roll",
            "frames": [
                {"label": "full table", "note": "O(m·n)"},
                {"label": "two rows", "note": "O(n)"},
            ],
        },
        "micro_trace": "LCS optimized: prev/curr rows swap each i",
        "failure": "Aliasing prev and curr to the same array",
        "retrieve_prompt": "When is it safe to drop the full DP table?",
        "retrieve_answer": "When every recurrence reference lands in the rolling window you kept.",
        "transfer_hint": "1D DP often collapses further to two variables (Fibonacci shape).",
    },
}


def get_pattern_card(method_id: str) -> Optional[Dict]:
    method = get_method(method_id)
    if not method:
        return None
    card = PATTERN_CARDS.get(method_id, {})
    return {
        "method": method,
        "trigger": card.get("trigger", method.get("summary")),
        "schema": card.get("schema", method.get("summary")),
        "visual": card.get("visual", {"kind": "generic", "frames": []}),
        "micro_trace": card.get("micro_trace", ""),
        "failure": card.get("failure", ""),
        "form_cues": method.get("form_cues", []),
        "retrieve_prompt": card.get(
            "retrieve_prompt", "State the invariant of this method in one sentence."
        ),
        "retrieve_answer": card.get(
            "retrieve_answer", method.get("form_cues", [""])[0]
        ),
        "transfer_hint": card.get("transfer_hint", ""),
        "parent_skill_ids": method.get("parent_skill_ids", []),
    }


def _interleave(items: List[Dict], key_fn) -> List[Dict]:
    """Fisher-Yates-free round-robin by key to avoid blocked practice."""
    buckets: Dict[str, List[Dict]] = {}
    order: List[str] = []
    for item in items:
        k = key_fn(item)
        if k not in buckets:
            buckets[k] = []
            order.append(k)
        buckets[k].append(item)
    out: List[Dict] = []
    while any(buckets.values()):
        for k in order:
            if buckets[k]:
                out.append(buckets[k].pop(0))
    return out


def build_session(
    questions: List[Dict],
    *,
    store: Optional[MemoryStore] = None,
    limit: int = 6,
) -> Dict:
    """Build an interleaved learn session: due reviews + new encodes.

    Priority:
      1. Due method cards (retrieval)
      2. Unseen methods (encoding) — curriculum order by pillar
      3. Due problems for transfer
    """
    store = store or memory_store
    now = _now()
    q_by_id = {q["id"]: q for q in questions}

    method_items = []
    for mid, method in METHODS.items():
        card = store.get_card("method", mid)
        skill_id = (method.get("parent_skill_ids") or ["unknown"])[0]
        pillar_id = SKILLS.get(skill_id, {}).get("pillar_id", "unknown")
        due = float(card.get("due_at", 0)) <= now
        unseen = not card.get("seen_encode")
        priority = 0
        if due and int(card.get("repetitions", 0)) > 0:
            priority = 0  # review first
            role = "retrieve"
        elif unseen or int(card.get("repetitions", 0)) == 0:
            priority = 1
            role = "encode"
        elif due:
            priority = 2
            role = "retrieve"
        else:
            continue
        method_items.append(
            {
                "kind": "method",
                "role": role,
                "ref_id": mid,
                "priority": priority,
                "skill_id": skill_id,
                "pillar_id": pillar_id,
                "stability": card.get("stability", 0),
                "title": method["name"],
                "card": get_pattern_card(mid),
            }
        )

    method_items.sort(key=lambda x: (x["priority"], x["stability"]))
    # Interleave by skill so we don't drill one pattern to boredom
    picked = _interleave(method_items[: limit * 2], lambda x: x["skill_id"])[:limit]

    # Attach a transfer problem for apply phase when possible
    steps = []
    for item in picked:
        mid = item["ref_id"]
        related = [
            qid
            for qid, mids in QUESTION_METHODS.items()
            if mid in mids and qid in q_by_id
        ]
        # Prefer problems not yet fluent
        related.sort(
            key=lambda qid: store.get_card("problem", qid).get("stability", 0)
        )
        transfer = None
        if related:
            qid = related[0]
            q = q_by_id[qid]
            transfer = {
                "id": qid,
                "title": q["title"],
                "difficulty": q["difficulty"],
                "category": q.get("category"),
            }
        steps.append(
            {
                **item,
                "phases": list(PHASES),
                "transfer_problem": transfer,
                "elaboration": store.get_elaboration(mid),
            }
        )

    summary = store.mastery_summary()
    return {
        "built_at": now,
        "step_count": len(steps),
        "steps": steps,
        "mastery": summary,
        "science": {
            "spacing": "Reviews expand only after successful retrieval (SM-2).",
            "retrieval": "You must answer before the cue is shown again.",
            "interleaving": "Methods from different skills are mixed to force discrimination.",
            "elaboration": "Restating the invariant in your words builds a stable schema.",
            "transfer": "Each chunk ends on a real problem so memory stays usable in interviews.",
        },
    }


def session_step_payload(method_id: str, questions: List[Dict]) -> Optional[Dict]:
    """Full payload for one method's four-phase learn card."""
    card = get_pattern_card(method_id)
    if not card:
        return None
    store = memory_store
    mem = store.get_card("method", method_id)
    related = [
        q
        for q in questions
        if method_id in QUESTION_METHODS.get(q["id"], [])
    ]
    return {
        "pattern": card,
        "memory": mem,
        "elaboration": store.get_elaboration(method_id),
        "related_problems": [
            {
                "id": q["id"],
                "title": q["title"],
                "difficulty": q["difficulty"],
                "primary": QUESTION_METHODS.get(q["id"], [None])[0] == method_id,
            }
            for q in related
        ],
        "parents": [
            {
                "skill_id": sid,
                "skill_name": SKILLS[sid]["name"],
                "pillar_id": SKILLS[sid]["pillar_id"],
            }
            for sid in card["method"]["parent_skill_ids"]
            if sid in SKILLS
        ],
        "phases": list(PHASES),
    }
