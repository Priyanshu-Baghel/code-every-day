# Extraction of Digits from given Number or Integer

n = int(input("Enter an Integer: "))


# Use Loop extract one by one. (Time Complexity -> 0(n)) 

copy_num = n
length_count = 0
while copy_num > 0:
    last_digit = copy_num % 10 
    # take module of 10 getting always last digit of a number
    print("Last Digit of Integer by each Iteration :", last_digit)
    copy_num //= 10
    
"""

# Input 
Enter an Integer: 123456

# Output 
Last Digit of Integer by each Iteration : 6
Last Digit of Integer by each Iteration : 5
Last Digit of Integer by each Iteration : 4
Last Digit of Integer by each Iteration : 3
Last Digit of Integer by each Iteration : 2
Last Digit of Integer by each Iteration : 1

"""
