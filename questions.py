"""
Question database for LeetCode practice tool.
Contains common LeetCode problems organized by category and difficulty.
"""

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
                    "The complement approach avoids nested loops"
                ]
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
                    "Update maximum profit as you go"
                ]
            }
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
                    "Skip duplicates to avoid duplicate triplets"
                ]
            }
        ]
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
                    "Two-pointer technique can save space"
                ]
            }
        ]
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
                    "Consider both iterative and recursive approaches"
                ]
            }
        ]
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
                    "Can also solve iteratively with BFS"
                ]
            }
        ]
    }
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