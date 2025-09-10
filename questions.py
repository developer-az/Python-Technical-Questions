"""Question database for LeetCode practice tool.
Contains common LeetCode problems organized by category and difficulty."""

QUESTIONS = {
    "arrays": {
        "easy": [
            {
                "id": 1,
                "title": "Two Sum",
                "difficulty": "Easy",
                "category": "Arrays",
                "problem": """Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

Example:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].""",
                "solution": """def two_sum(nums, target):
    hash_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in hash_map:
            return [hash_map[complement], i]
        hash_map[num] = i
    return []

Time Complexity: O(n)
Space Complexity: O(n)""",
                "hints": [
                    "Think about using a hash map to store numbers you've seen",
                    "For each number, check if its complement (target - number) exists",
                    "The complement approach avoids nested loops",
                ],
            },
            {
                "id": 2,
                "title": "Best Time to Buy and Sell Stock",
                "difficulty": "Easy",
                "category": "Arrays",
                "problem": """You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

Example:
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.""",
                "solution": """def max_profit(prices):
    if not prices:
        return 0
    
    min_price = prices[0]
    max_profit = 0
    
    for price in prices[1:]:
        if price < min_price:
            min_price = price
        else:
            max_profit = max(max_profit, price - min_price)
    
    return max_profit

Time Complexity: O(n)
Space Complexity: O(1)""",
                "hints": [
                    "Keep track of the minimum price seen so far",
                    "For each price, calculate profit if we sell at that price",
                    "Update maximum profit as you go",
                ],
            },
        ],
        "medium": [
            {
                "id": 3,
                "title": "3Sum",
                "difficulty": "Medium",
                "category": "Arrays",
                "problem": """Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Example:
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]""",
                "solution": """def three_sum(nums):
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
    
    return result

Time Complexity: O(n²)
Space Complexity: O(1)""",
                "hints": [
                    "Sort the array first to enable two-pointer technique",
                    "Fix one element and use two pointers for the remaining two",
                    "Skip duplicates to avoid duplicate triplets",
                ],
            },
            {
                "id": 7,
                "title": "Product of Array Except Self",
                "difficulty": "Medium",
                "category": "Arrays",
                "problem": """Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.

Example:
Input: nums = [1,2,3,4]
Output: [24,12,8,6]""",
                "solution": """def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    
    # Forward pass: store products of all elements to the left
    for i in range(1, n):
        result[i] = result[i-1] * nums[i-1]
    
    # Backward pass: multiply by products of all elements to the right
    right_product = 1
    for i in range(n-1, -1, -1):
        result[i] *= right_product
        right_product *= nums[i]
    
    return result

Time Complexity: O(n)
Space Complexity: O(1) - not counting output array""",
                "hints": [
                    "Think about left products and right products separately",
                    "First pass: calculate product of all elements to the left",
                    "Second pass: multiply by product of all elements to the right",
                ],
            },
            {
                "id": 8,
                "title": "Container With Most Water",
                "difficulty": "Medium",
                "category": "Arrays",
                "problem": """You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container that can hold the most water.

Return the maximum amount of water a container can store.

Example:
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.""",
                "solution": """def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        # Calculate current area
        width = right - left
        current_height = min(height[left], height[right])
        current_area = width * current_height
        max_water = max(max_water, current_area)
        
        # Move the pointer with smaller height
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_water

Time Complexity: O(n)
Space Complexity: O(1)""",
                "hints": [
                    "Use two pointers approach starting from both ends",
                    "Always move the pointer with the smaller height",
                    "Area is determined by the shorter of the two lines",
                ],
            },
        ],
        "hard": [
            {
                "id": 9,
                "title": "Trapping Rain Water",
                "difficulty": "Hard",
                "category": "Arrays",
                "problem": """Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

Example:
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.""",
                "solution": """def trap(height):
    if not height or len(height) < 3:
        return 0
    
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0
    
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    
    return water

Time Complexity: O(n)
Space Complexity: O(1)""",
                "hints": [
                    "Think about what determines how much water can be trapped at each position",
                    "Water level at any point is min(max_left, max_right) - current_height",
                    "Two pointers approach can solve this efficiently",
                ],
            }
        ],
    },
    "strings": {
        "easy": [
            {
                "id": 4,
                "title": "Valid Palindrome",
                "difficulty": "Easy",
                "category": "Strings",
                "problem": """A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.

Given a string s, return true if it is a palindrome, or false otherwise.

Example:
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.""",
                "solution": """def is_palindrome(s):
    # Convert to lowercase and keep only alphanumeric
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    
    # Check if it's equal to its reverse
    return cleaned == cleaned[::-1]

# Alternative two-pointer approach:
def is_palindrome_two_pointer(s):
    left, right = 0, len(s) - 1
    
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True

Time Complexity: O(n)
Space Complexity: O(1) for two-pointer approach""",
                "hints": [
                    "Consider only alphanumeric characters",
                    "Convert to lowercase for comparison",
                    "Two-pointer technique can save space",
                ],
            },
            {
                "id": 10,
                "title": "Valid Parentheses",
                "difficulty": "Easy",
                "category": "Strings",
                "problem": """Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

Example:
Input: s = "()[]{}"
Output: true

Example:
Input: s = "([)]"
Output: false""",
                "solution": """def is_valid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            # It's a closing bracket
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            # It's an opening bracket
            stack.append(char)
    
    return not stack

Time Complexity: O(n)
Space Complexity: O(n)""",
                "hints": [
                    "Use a stack to keep track of opening brackets",
                    "When you see a closing bracket, check if it matches the most recent opening bracket",
                    "The string is valid if the stack is empty at the end",
                ],
            },
        ],
        "medium": [
            {
                "id": 11,
                "title": "Longest Substring Without Repeating Characters",
                "difficulty": "Medium",
                "category": "Strings",
                "problem": """Given a string s, find the length of the longest substring without repeating characters.

Example:
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.

Example:
Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.""",
                "solution": """def length_of_longest_substring(s):
    char_map = {}
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        if s[right] in char_map and char_map[s[right]] >= left:
            # Move left pointer to avoid duplicate
            left = char_map[s[right]] + 1
        
        char_map[s[right]] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length

Time Complexity: O(n)
Space Complexity: O(min(m, n)) where m is charset size""",
                "hints": [
                    "Use sliding window technique with two pointers",
                    "Keep track of character positions in a hash map",
                    "When you find a duplicate, move the left pointer",
                ],
            },
            {
                "id": 12,
                "title": "Group Anagrams",
                "difficulty": "Medium",
                "category": "Strings",
                "problem": """Given an array of strings strs, group the anagrams together. You can return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

Example:
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]""",
                "solution": """def group_anagrams(strs):
    from collections import defaultdict
    
    groups = defaultdict(list)
    
    for s in strs:
        # Sort the string to get the key
        key = ''.join(sorted(s))
        groups[key].append(s)
    
    return list(groups.values())

# Alternative approach using character count:
def group_anagrams_count(strs):
    from collections import defaultdict
    
    groups = defaultdict(list)
    
    for s in strs:
        count = [0] * 26
        for char in s:
            count[ord(char) - ord('a')] += 1
        groups[tuple(count)].append(s)
    
    return list(groups.values())

Time Complexity: O(n * k log k) where k is max string length
Space Complexity: O(n * k)""",
                "hints": [
                    "Anagrams have the same characters when sorted",
                    "Use sorted string as key in hash map",
                    "Alternative: use character frequency as key",
                ],
            },
        ],
    },
    "linked_lists": {
        "easy": [
            {
                "id": 5,
                "title": "Reverse Linked List",
                "difficulty": "Easy",
                "category": "Linked Lists",
                "problem": """Given the head of a singly linked list, reverse the list, and return the reversed list.

Example:
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]""",
                "solution": """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    prev = None
    current = head
    
    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp
    
    return prev

# Recursive approach:
def reverse_list_recursive(head):
    if not head or not head.next:
        return head
    
    reversed_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    
    return reversed_head

Time Complexity: O(n)
Space Complexity: O(1) iterative, O(n) recursive""",
                "hints": [
                    "Keep track of previous, current, and next nodes",
                    "Reverse the direction of each link as you traverse",
                    "Consider both iterative and recursive approaches",
                ],
            },
            {
                "id": 13,
                "title": "Merge Two Sorted Lists",
                "difficulty": "Easy",
                "category": "Linked Lists",
                "problem": """You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.

Example:
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]""",
                "solution": """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_two_lists(list1, list2):
    dummy = ListNode(0)
    current = dummy
    
    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
    
    # Attach remaining nodes
    current.next = list1 or list2
    
    return dummy.next

# Recursive approach:
def merge_two_lists_recursive(list1, list2):
    if not list1:
        return list2
    if not list2:
        return list1
    
    if list1.val <= list2.val:
        list1.next = merge_two_lists_recursive(list1.next, list2)
        return list1
    else:
        list2.next = merge_two_lists_recursive(list1, list2.next)
        return list2

Time Complexity: O(n + m)
Space Complexity: O(1) iterative, O(n + m) recursive""",
                "hints": [
                    "Use a dummy node to simplify edge cases",
                    "Compare values and always pick the smaller one",
                    "Don't forget to attach remaining nodes at the end",
                ],
            },
        ],
        "medium": [
            {
                "id": 14,
                "title": "Linked List Cycle II",
                "difficulty": "Medium",
                "category": "Linked Lists",
                "problem": """Given the head of a linked list, return the node where the cycle begins. If there is no cycle, return null.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer.

Example:
Input: head = [3,2,0,-4], pos = 1
Output: tail connects to node index 1
Explanation: There is a cycle in the linked list, where tail connects to the second node.""",
                "solution": """class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def detect_cycle(head):
    if not head or not head.next:
        return None
    
    # Phase 1: Detect if cycle exists using Floyd's algorithm
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle
    
    # Phase 2: Find the start of the cycle
    start = head
    while start != slow:
        start = start.next
        slow = slow.next
    
    return start

Time Complexity: O(n)
Space Complexity: O(1)""",
                "hints": [
                    "Use Floyd's cycle detection algorithm (two pointers)",
                    "First detect if cycle exists, then find cycle start",
                    "Mathematical proof: distance from head to cycle start equals distance from meeting point to cycle start",
                ],
            }
        ],
    },
    "trees": {
        "easy": [
            {
                "id": 6,
                "title": "Maximum Depth of Binary Tree",
                "difficulty": "Easy",
                "category": "Trees",
                "problem": """Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

Example:
Input: root = [3,9,20,null,null,15,7]
Output: 3""",
                "solution": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_depth(root):
    if not root:
        return 0
    
    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)
    
    return max(left_depth, right_depth) + 1

# Iterative approach using queue:
from collections import deque

def max_depth_iterative(root):
    if not root:
        return 0
    
    queue = deque([(root, 1)])
    max_depth = 0
    
    while queue:
        node, depth = queue.popleft()
        max_depth = max(max_depth, depth)
        
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    
    return max_depth

Time Complexity: O(n)
Space Complexity: O(h) where h is height of tree""",
                "hints": [
                    "Think recursively: depth is 1 + max of left and right subtrees",
                    "Base case: empty tree has depth 0",
                    "Can also solve iteratively with BFS",
                ],
            },
            {
                "id": 15,
                "title": "Same Tree",
                "difficulty": "Easy",
                "category": "Trees",
                "problem": """Given the roots of two binary trees p and q, write a function to check if they are the same or not.

Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.

Example:
Input: p = [1,2,3], q = [1,2,3]
Output: true

Example:
Input: p = [1,2], q = [1,null,2]
Output: false""",
                "solution": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def is_same_tree(p, q):
    # Base cases
    if not p and not q:
        return True
    if not p or not q:
        return False
    
    # Check current nodes and recurse
    return (p.val == q.val and 
            is_same_tree(p.left, q.left) and 
            is_same_tree(p.right, q.right))

# Iterative approach:
from collections import deque

def is_same_tree_iterative(p, q):
    queue = deque([(p, q)])
    
    while queue:
        node1, node2 = queue.popleft()
        
        if not node1 and not node2:
            continue
        if not node1 or not node2:
            return False
        if node1.val != node2.val:
            return False
        
        queue.append((node1.left, node2.left))
        queue.append((node1.right, node2.right))
    
    return True

Time Complexity: O(n)
Space Complexity: O(h) recursive, O(n) iterative""",
                "hints": [
                    "Check if both nodes are null (base case)",
                    "Check if one is null but other isn't (different structure)",
                    "Compare values and recursively check left and right subtrees",
                ],
            },
        ],
        "medium": [
            {
                "id": 16,
                "title": "Binary Tree Level Order Traversal",
                "difficulty": "Medium",
                "category": "Trees",
                "problem": """Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).

Example:
Input: root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]""",
                "solution": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def level_order(root):
    if not root:
        return []
    
    from collections import deque
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level_values = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level_values.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level_values)
    
    return result

Time Complexity: O(n)
Space Complexity: O(w) where w is maximum width of tree""",
                "hints": [
                    "Use BFS (breadth-first search) with a queue",
                    "Process nodes level by level",
                    "Keep track of how many nodes are in each level",
                ],
            },
            {
                "id": 17,
                "title": "Validate Binary Search Tree",
                "difficulty": "Medium",
                "category": "Trees",
                "problem": """Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:
- The left subtree of a node contains only nodes with keys less than the node's key.
- The right subtree of a node contains only nodes with keys greater than the node's key.
- Both the left and right subtrees must also be binary search trees.

Example:
Input: root = [2,1,3]
Output: true

Example:
Input: root = [5,1,4,null,null,3,6]
Output: false""",
                "solution": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def is_valid_bst(root):
    def validate(node, min_val, max_val):
        if not node:
            return True
        
        if node.val <= min_val or node.val >= max_val:
            return False
        
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))

# Alternative in-order traversal approach:
def is_valid_bst_inorder(root):
    def inorder(node):
        if not node:
            return []
        return inorder(node.left) + [node.val] + inorder(node.right)
    
    values = inorder(root)
    return values == sorted(values) and len(values) == len(set(values))

Time Complexity: O(n)
Space Complexity: O(h) where h is height of tree""",
                "hints": [
                    "Each node must be within a valid range",
                    "Left subtree values must be less than current node",
                    "Right subtree values must be greater than current node",
                    "Alternative: in-order traversal should give sorted sequence",
                ],
            },
        ],
    },
    "dynamic_programming": {
        "easy": [
            {
                "id": 18,
                "title": "Climbing Stairs",
                "difficulty": "Easy",
                "category": "Dynamic Programming",
                "problem": """You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Example:
Input: n = 2
Output: 2
Explanation: There are two ways to climb to the top.
1. 1 step + 1 step
2. 2 steps

Example:
Input: n = 3
Output: 3
Explanation: There are three ways to climb to the top.
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step""",
                "solution": """def climb_stairs(n):
    if n <= 2:
        return n
    
    # dp[i] represents number of ways to reach step i
    prev2, prev1 = 1, 2
    
    for i in range(3, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current
    
    return prev1

# Alternative DP array approach:
def climb_stairs_dp_array(n):
    if n <= 2:
        return n
    
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]

Time Complexity: O(n)
Space Complexity: O(1) optimized, O(n) with DP array""",
                "hints": [
                    "This is similar to Fibonacci sequence",
                    "To reach step n, you can come from step n-1 or n-2",
                    "ways(n) = ways(n-1) + ways(n-2)",
                ],
            },
            {
                "id": 19,
                "title": "House Robber",
                "difficulty": "Easy",
                "category": "Dynamic Programming",
                "problem": """You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.

Example:
Input: nums = [1,2,3,1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.

Example:
Input: nums = [2,7,9,3,1]
Output: 12
Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
Total amount you can rob = 2 + 9 + 1 = 12.""",
                "solution": """def rob(nums):
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    
    # prev2: max money up to i-2, prev1: max money up to i-1
    prev2, prev1 = 0, nums[0]
    
    for i in range(1, len(nums)):
        current = max(prev1, prev2 + nums[i])
        prev2, prev1 = prev1, current
    
    return prev1

# Alternative DP array approach:
def rob_dp_array(nums):
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    
    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
    
    for i in range(2, len(nums)):
        dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    
    return dp[-1]

Time Complexity: O(n)
Space Complexity: O(1) optimized, O(n) with DP array""",
                "hints": [
                    "For each house, decide whether to rob it or not",
                    "If you rob current house, you can't rob the previous one",
                    "max_money[i] = max(max_money[i-1], max_money[i-2] + nums[i])",
                ],
            },
        ],
        "medium": [
            {
                "id": 20,
                "title": "Coin Change",
                "difficulty": "Medium",
                "category": "Dynamic Programming",
                "problem": """You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.

Example:
Input: coins = [1,3,4], amount = 6
Output: 2
Explanation: 6 = 3 + 3

Example:
Input: coins = [2], amount = 3
Output: -1""",
                "solution": """def coin_change(coins, amount):
    # dp[i] represents minimum coins needed for amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1

# Alternative BFS approach:
from collections import deque

def coin_change_bfs(coins, amount):
    if amount == 0:
        return 0
    
    queue = deque([0])
    visited = {0}
    level = 0
    
    while queue:
        level += 1
        for _ in range(len(queue)):
            current = queue.popleft()
            
            for coin in coins:
                next_amount = current + coin
                if next_amount == amount:
                    return level
                if next_amount < amount and next_amount not in visited:
                    visited.add(next_amount)
                    queue.append(next_amount)
    
    return -1

Time Complexity: O(amount * coins)
Space Complexity: O(amount)""",
                "hints": [
                    "Use bottom-up DP approach",
                    "For each amount, try all possible coins",
                    "dp[amount] = min(dp[amount - coin] + 1) for all valid coins",
                ],
            },
            {
                "id": 21,
                "title": "Longest Common Subsequence",
                "difficulty": "Medium",
                "category": "Dynamic Programming",
                "problem": """Given two strings text1 and text2, return the length of their longest common subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.

A common subsequence of two strings is a subsequence that is common to both strings.

Example:
Input: text1 = "abcde", text2 = "ace" 
Output: 3  
Explanation: The longest common subsequence is "ace" and its length is 3.

Example:
Input: text1 = "abc", text2 = "abc"
Output: 3
Explanation: The longest common subsequence is "abc" and its length is 3.""",
                "solution": """def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    
    # dp[i][j] represents LCS length for text1[:i] and text2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]

# Space optimized version:
def longest_common_subsequence_optimized(text1, text2):
    m, n = len(text1), len(text2)
    
    # Use only two rows instead of full 2D array
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = max(prev[j], curr[j-1])
        prev, curr = curr, prev
    
    return prev[n]

Time Complexity: O(m * n)
Space Complexity: O(m * n), O(n) optimized""",
                "hints": [
                    "Use 2D DP where dp[i][j] represents LCS for first i chars of text1 and first j chars of text2",
                    "If characters match, add 1 to diagonal value",
                    "If characters don't match, take max of left and top values",
                ],
            },
        ],
    },
}


def get_all_questions():
    """Return all questions as a flat list."""
    all_questions = []
    for category in QUESTIONS.values():
        for difficulty in category.values():
            all_questions.extend(difficulty)
    return all_questions


def get_questions_by_category(category):
    """Get all questions from a specific category."""
    if category in QUESTIONS:
        questions = []
        for difficulty in QUESTIONS[category].values():
            questions.extend(difficulty)
        return questions
    return []


def get_questions_by_difficulty(difficulty):
    """Get all questions of a specific difficulty."""
    questions = []
    for category in QUESTIONS.values():
        if difficulty in category:
            questions.extend(category[difficulty])
    return questions


def get_categories():
    """Get list of available categories."""
    return list(QUESTIONS.keys())


def get_difficulties():
    """Get list of available difficulties."""
    difficulties = set()
    for category in QUESTIONS.values():
        difficulties.update(category.keys())
    return sorted(list(difficulties))
