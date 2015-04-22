# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes 
# a string as input and returns the i and j indices that 
# correspond to the beginning and end indices of the longest 
# palindrome in the string. 
#
# Grading Notes:
# 
# You will only be marked correct if your function runs 
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    # Your code here
    if len(text) == 0:
        return 0, 0
    text = text.lower()
    max_slice_st = 0
    max_slice_end = 1
    max_len = 1

    start = 0
    while start < len(text) - 1:
        left = start
        end = -1
        for right in reversed(range(start, len(text))):
            if left >= right:
                break
            if text[right] == text[left]:
                if end == -1:
                    end = right + 1
                left += 1
            else:
                end = -1
                left = start
        if end - start > max_len:
            max_slice_st = start
            max_slice_end = end
            max_len = end - start
        start += 1
    return max_slice_st, max_slice_end
def test():
    L = longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    assert L('aaaaaaaaaaaaaaa.') == (0, 15)
    return 'tests pass'

print(test())