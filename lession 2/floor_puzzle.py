#------------------
# User Instructions
#
# Hopper, Kay, Liskov, Perlis, and Ritchie live on 
# different floors of a five-floor apartment building. 
#
# Hopper does not live on the top floor. 
# Kay does not live on the bottom floor. 
# Liskov does not live on either the top or the bottom floor. 
# Perlis lives on a higher floor than does Kay. 
# Ritchie does not live on a floor adjacent to Liskov's. 
# Liskov does not live on a floor adjacent to Kay's. 
# 
# Where does everyone live?  
# 
# Write a function floor_puzzle() that returns a list of
# five floor numbers denoting the floor of Hopper, Kay, 
# Liskov, Perlis, and Ritchie.

import itertools
import time

def adjacent(p0, p1):
	return abs(p0 - p1) == 1

def floor_puzzle1():
    # Your code here
    return next((Hopper, Kay, Liskov, Perlis, Ritchie) 
    	for Hopper in range(1, 5)
    	for Kay in range(2, 5)
    	if Kay != Hopper
    	for Liskov in set(range(2, 5)) - {Kay, Hopper}
    	#if Liskov not in { Kay, Hopper}
    	if not adjacent(Liskov, Kay)
    	for Perlis in set(range(3, 6)) - {Kay, Liskov, Hopper}
    	#if Perlis not in {Liskov, Kay, Hopper}
    	if Perlis > Kay
    	for Ritchie in set(range(1, 6)) - {Perlis, Liskov, Kay, Hopper}
    	#if Ritchie not in {Liskov, Kay, Hopper, Perlis}
    	if not adjacent(Ritchie, Liskov)
    	)

def floor_puzzle():
    # Your code here
    return next((Hopper, Kay, Liskov, Perlis, Ritchie) 
    	for Hopper in range(1, 5)
    	for Kay in range(2, 5)
    	if Kay != Hopper
    	for Liskov in range(2, 5)
    	if Liskov not in { Kay, Hopper}
    	if not adjacent(Liskov, Kay)
    	for Perlis in range(3, 6)
    	if Perlis not in {Liskov, Kay, Hopper}
    	if Perlis > Kay
    	for Ritchie in range(1, 6)
		if Ritchie not in {Liskov, Kay, Hopper, Perlis}
		if not adjacent(Ritchie, Liskov)
    	)

def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result."
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result

def average(numbers):
    "Return the average (arithmetic mean) of a sequence of numbers."
    return sum(numbers) / float(len(numbers))

def timedcalls(n, fn, *args):
    """Call fn(*args) repeatedly: n times if n is an int, or up to
    n seconds if n is a float; return the min, avg, and max time"""
    if isinstance(n, int):
        times = [timedcall(fn, *args)[0] for _ in range(n)]
    else:
        times = []
        total = 0.0
        while total < n:
            t = timedcall(fn, *args)[0]
            total += t
            times.append(t)
    return min(times), average(times), max(times)

if __name__ == '__main__':
	print(timedcalls(100000, floor_puzzle))
	print(timedcalls(100000, floor_puzzle1))
	print(floor_puzzle())