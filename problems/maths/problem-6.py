"""
Docstring for problems.maths.problem-6

Problem Statement By GFG 

Difficult -> EASY

Number of factors

Find the number of factors for a given integer n.

Examples:

Input: n = 5
Output: 2
Explanation: 5 has 2 factors 1 and 5

Input: n = 25
Output: 3
Explanation: 25 has 3 factors 1, 5, 25 

Constraints: 1 ≤ n ≤ 10^5

"""

# Solution's

# My Solution and its brute force
class Solution:
    def countFactors (self, n):
        factor = 0
        for i in range(1,n+1):  # 0(n)
            if n % i == 0:
                factor += 1
        return factor
    
# Better Approach
class Solution:
    def countFactors (self, n):
        factor = 2
        for i in range(2,n//2):  # 0(n/2) because half of the number can't be factor
            if n % i == 0:
                factor += 1
        return factor
    
# Optimal Approach
"""
number is 36 then factor are

factor 
num        factor-1       factor-2
36      /     1     --->    36
36      /     2     --->    18
36      /     3     --->    12
36      /     4     --->    9
36      /     6     --->    6
"""


from math import sqrt 

class Solution:
    def countFactors (self, n):
        factor = 2
        for i in range(2,int(sqrt(n))+1): # 0(sqrt(n)) because factor are repeaqting
            if n % i == 0:
                factor += 1
                if  n//i != i:
                    factor += 1
        return factor