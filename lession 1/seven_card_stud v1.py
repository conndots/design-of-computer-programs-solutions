#!/usr/bin/python
# -*- coding : utf-8 -*-

# CS 212, hw1-1: 7-card stud
#
# -----------------
# User Instructions
#
# Write a function best_hand(hand) that takes a seven
# card hand as input and returns the best possible 5
# card hand. The itertools library has some functions
# that may help you solve this problem.
#
# -----------------
# Grading Notes
# 
# Muliple correct answers will be accepted in cases 
# where the best hand is ambiguous (for example, if 
# you have 4 kings and 3 queens, there are three best
# hands: 4 kings along with any of the three queens).

import collections

class Card(object):
    def __init__(self, str):
        self._suit = str[1]
        self._no = '--23456789TJQKA'.index(str[0])
        self._str = str

    @property
    def suit(self):
        return self._suit

    def __len__(self):
        return 1

    def __getitem__(self, index):
        if index != 0:
            raise ValueError("Index out side the list")
        return self

    @property
    def no(self):
        return self._no
    
    @property
    def str(self):
        return self._str

class CardList(Card):
    def __init__(self, key, card=None):
        self.__cards = []
        if card:
            self.__cards.append(card)
        self._key = key

    def append(self, card, key_update=lambda x: x):
        self.__cards.append(card)
        self._key = key_update(self._key)

    def __len__(self):
        return len(self.__cards)

    def __getitem__(self, index):
        return self.__cards[index]

    @property
    def key(self):
        return self._key

    @property
    def suit(self):
        return self._cards[0].suit

    @property
    def no(self):
        return self._key

    def to_list(self):
        return list(self.__cards)

    @property
    def str(self):
        return [card.str for card in self.__cards].__str__()

def check_list_of_cards_key_equals(clists, keys):
    for cindex, clist in enumerate(clists):
        if clist.no != keys[cindex]:
            return False
    return True

def trans_2_cards(hand):
    return [Card(card) for card in hand]

def trans_2_hands(cards):
    return [card[0].str for card in cards]

def best_hand(hand):
    "From a 7-card hand, return the best 5 card hand." 
    # Your code here
    cards = trans_2_cards(hand)
    long_flush = get_long_flush(cards)
    min_hand_rank, min_rawhand = (5, sorted(long_flush, reverse=True, key=lambda x: x.no)) if long_flush else (-1, None)

    sorted_cardlists = group_to_cardlists_sorted_by_no(cards)

    if min_hand_rank == 5:
        flush_straight = best_straight(min_rawhand)
        if flush_straight: #flush_straight
            return trans_2_hands(flush_straight[:5])

    straight = best_straight(sorted_cardlists)
    min_hand_rank, min_rawhand = (4, straight) if straight and 4 > min_hand_rank else (min_hand_rank, min_rawhand)

    best_kind_hand_rank, best_kind_hand = best_kind(sorted_cardlists)
    if best_kind_hand_rank > min_hand_rank:
        return trans_2_hands(best_kind_hand)
    else: 
        return trans_2_hands(min_rawhand[:5])

#takes a sorted list of CardList as argument, return a list of cards
def best_kind(sclists):
    sorted_by_len = sorted(sclists, key=lambda x: len(x) + (x.no / 100), reverse=True)
    if len(sorted_by_len[0]) == 4:
        ret = sorted_by_len[0].to_list()
        ret.append(sclists[0] if sclists[0].no != sorted_by_len[0].no else sclists[1])
        return 7, ret
    ge_2_lists = list(filter(lambda x: len(x) >= 2, sclists))
    if len(sorted_by_len[0]) == 3:
        if(len(ge_2_lists) > 0):
            ret = sorted_by_len[0].to_list()
            ret.extend(ge_2_lists[0].to_list()[:2] if ge_2_lists[0].no != sorted_by_len[0].no \
                else ge_2_lists[1].to_list()[:2])
            return 6, ret
        ret = sorted_by_len[0].to_list()
        ret.extend(list(filter(lambda x : x.no != sorted_by_len[0].no, sclists))[:2])
        return 3, ret
    if len(ge_2_lists) >= 2:
        ret = ge_2_lists[0].to_list()
        ret.extend(ge_2_lists[1].to_list())
        ret.append(max(sorted_by_len[2:], key=lambda x: x.no, reverse=True))
        return 2, ret
    if len(ge_2_lists) == 1:
        ret = ge_2_lists[0].to_list()
        ret.extend(sorted_by_len[1: 5])
        return 1, ret
    return 0, sclists[:5]

#takes a list of Card or CardList 
def best_straight(cards):
    if len(cards) < 5:
        return None
    max_length = 1
    max_start = 0
    length = 1
    start = 0
    for i in range(1, len(cards)):
        if cards[i].no - 1 == cards[i - 1].no:
            length += 1
            if length > max_length:
                max_length = clength
                max_start = start
        else:
            start = i
            length = 1
    if max_length == 4 and cards[0].no == 14 and check_list_of_cards_key_equals(cards[-4:], [5, 4, 3, 2]):
        return cards[-4:].append(cards[0])
    if max_length < 5:
        return None
    return cards[max_start: max_start + 5]

def group_to_cardlists_sorted_by_no(cards):
    cards.sort(reverse=True, key = lambda x: x.no)
    sorted_lists = []
    last_cardlist = CardList(cards[0].no, cards[0])
    for i in range(1, len(cards)):
        if cards[i].no == last_cardlist.key:
            last_cardlist.append(cards[i], lambda x: x) 
        else:
            sorted_lists.append(last_cardlist)
            last_cardlist = CardList(cards[i].no, cards[i])

    sorted_lists.append(last_cardlist)        

    return sorted_lists

def get_long_flush(cards):
    suit2count = collections.defaultdict(lambda: [])
    for card in cards:
        suit2count[card.suit].append(card)
    for s, cards in suit2count.items():
        if len(cards) >= 5:
            return cards
    return None
    
def test_best_hand():
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    return 'test_best_hand passes'

if __name__ == '__main__':
    print(test_best_hand())
   # best_hand("TD TC TH 7C 7D 8C 8S".split())