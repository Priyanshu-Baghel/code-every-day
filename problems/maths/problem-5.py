"""
Docstring for problems.maths.problem-5

Problem Statement By GFG 

Difficult -> EASY

Armstrong Numbers

You are given a 3-digit number n, 
Find whether it is an Armstrong number or not.
An Armstrong number of three digits is a number such that the sum of the 
cubes of its digits is equal to the number itself. 
371 is an Armstrong number since 33 + 73 + 13 = 371. 

Examples:

Input: n = 153
Output: true
Explanation: 153 is an Armstrong number since 13 + 53 + 33 = 153. 

Input: n = 372
Output: false
Explanation: 372 is not an Armstrong number since 33 + 73 + 23 = 378. 

Input: n = 100
Output: false
Explanation: 100 is not an Armstrong number since 13 + 03 + 03 = 1. 

Constraints: 100 ≤ n <1000 
"""

# Solution 

class Solution:
    def armstrongNumber (self, n):
        copy_num = n
        sum_digits = 0
        
        while copy_num > 0:
            sum_digits += (copy_num % 10) ** 3
            copy_num //= 10 
        
        if n == sum_digits:
            return True
        
        return False