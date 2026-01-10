"""
Docstring for problems.maths.problem-2

# Count Digits in Number or Integer

--> Two Approaches:

1. Use Loop and Count each digit one by one. Time Complexity--> O(n) where n is length of integer 
2. Using Maths by Log of 10. Time Complexity --> 0(1)
3. Only in Python type conversion to string use Len function. But This is not recommended
   Time Complexity --> 0(n^2)

"""



# 1. Use Loop and Count each digit one by one

def approach1(num: int) -> int:
    copy_num = num
    length_count = 0
    while copy_num > 0:
        length_count += 1
        copy_num //= 10
    return length_count


# 2. Using Maths by Log of 10.

def approach2(num: int) -> int:
    return int(math.log10(num)) + 1

# 3. Using Maths by Log of 10.

def approach3(num: int) -> int:
    return len(str(num))

# main 
if __name__ == "__main__":
    num = int(input("Enter the Number: "))
    # Approach 1
    print("Count by Approach 1: ", approach1(num)) 
    # Approach 2
    import math  # importing math module of python
    print("Count by Approach 2: ", approach2(num)) 
    # Approach 3
    print("Count by Approach 3: ", approach3(num)) 
    
# Variation question's 

""" 
1. Problem statement (By Coding Ninjas)
Ninja want to add coding to his skill set so he started learning it. On the first day, he stuck to a problem in which he has given a long integer ‘X’ and had to count the number of digits in it.

Ninja called you for help as you are his only friend. Help him to solve the problem.

EXAMPLE:
Input: 'X' = 2

Output: 1

As only one digit is ‘2’ present in ‘X’ so answer is ‘1’.

Sample Input 1 :
2
89
870
Sample Output 1 :
2
3
Explanation Of Sample Input 1 :
In test case ‘1’. There are ‘2’ digits present in ‘89’ that is ‘8’ and ‘9’. So the answer is ‘2’.
In test case ‘2’. There are ‘3’ digits present in ‘870’ that is ‘8’, ‘7’ and ‘0’. So the answer is ‘3’.

"""
# Solution :   
from math import *

def countDigit(n: int) -> int:
   return int(log10(n)) + 1




""" 
2. Problem Statement (By GFG):
Given a positive integer n, count the number of digits in n that divide n evenly (i.e., without leaving a remainder). Return the total number of such digits.

A digit d of n divides n evenly if the remainder when n is divided by d is 0 (n % d == 0).
Digits of n should be checked individually. If a digit is 0, it should be ignored because division by 0 is undefined.


Input: n = 12
Output: 2
Explanation: 1, 2 when both divide 12 leaves remainder 0.

"""

# Solution :   
class Solution:
    def helper(self, n):
        copy_num = n
        res = 0
        while copy_num > 0:
            if copy_num % 10 == 0:
                pass
            elif n % (copy_num % 10) == 0:
                res += 1
            copy_num //= 10
        return res
            
    def evenlyDivides(self, n):
        evenly_division_digit_count = 0
        evenly_division_digit_count += self.helper(n)
        return evenly_division_digit_count