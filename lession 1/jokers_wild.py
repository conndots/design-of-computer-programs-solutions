#!/usr/bin/python
# -*- coding : utf-8 -*-

# CS 212, hw1-2: Jokers Wild
#
# -----------------
# User Instructions
#
# Write a function best_wild_hand(hand) that takes as
# input a 7-card hand and returns the best 5 card hand.
# In this problem, it is possible for a hand to include
# jokers. Jokers will be treated as 'wild cards' which
# can take any rank or suit of the same color. The 
# black joker, '?B', can be used as any spade or club
# and the red joker, '?R', can be used as any heart 
# or diamond.
#
# The itertools library may be helpful. Feel free to 
# define multiple functions if it helps you solve the
# problem. 
#
# -----------------
# Grading Notes
# 
# Muliple correct answers will be accepted in cases 
# where the best hand is ambiguous (for example, if 
# you have 4 kings and 3 queens, there are three best
# hands: 4 kings along with any of the three queens).

import itertools

CARD_STR = '--23456789TJQKA'

def replace_wildcards(card, available_suits):
    if card[0] != '?':
        return [card]
    suits = []
    if card[1] == 'R':
        if 'H' in available_suits:
            suits.append('H')
        if 'D' in available_suits:
            suits.append('D')
    elif card[1] == 'B':
        if 'C' in available_suits:
            suits.append('C')
        if 'S' in available_suits:
            suits.append('S')
    replacement = []
    for suit in suits:
        for i in range(2, 15):
            replacement.append(CARD_STR[i] + suit)
    return replacement

def wildless_hand_iter(hand):
    suits = []
    for card in filter(lambda c: c[0] != '?', hand):
        suits.append(card[1])
    suits_set = set(suits)
    return itertools.product(*map(lambda x: replace_wildcards(x, suits_set), hand))

def best_wild_hand(hand):
    "Try all values for jokers in all 5-card selections."
    # Your code here
    wildmax = max((best_hand(chand) for chand in wildless_hand_iter(hand)), key=hand_rank)
    return wildmax 

def best_hand(hand):
    return max(itertools.combinations(hand, 5), key=hand_rank)

# ------------------
# Provided Functions
# 
# You may want to use some of the functions which
# you have already defined in the unit to write 
# your best_hand function.

def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks(hand) 
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)
    
def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r,s in hand]
    return len(set(suits)) == 1

def straight(ranks):
    """Return True if the ordered 
    ranks form a 5-card straight."""
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def kind(n, ranks):
    """Return the first rank that this hand has 
    exactly n-of-a-kind of. Return None if there 
    is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n: return r
    return None

def two_pair(ranks):
    """If there are two pair here, return the two 
    ranks of the two pairs, else None."""
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None 

def test_best_wild_hand():
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    return 'test_best_wild_hand passes'

if __name__ == '__main__':
    #for hand in wildless_hand_iter(['?B','?R'], ['3H', '4D', '5C', '7S', '9C']):
    #    print(hand)
    print(best_wild_hand(['TD', 'TC', '5H', '5C', '7C', '?R', '?B']))
    #test_best_wild_hand()