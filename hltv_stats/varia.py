#!/usr/bin/env python3
# coding: utf-8

import re
import itertools
import sys

LETTERS = {
    'a':'4',
    'e':'3',
    'i':'1',
    'o':'0'
}

def bi_dict(half_dict):
    """Returns a two-way dictionary of the input dictionary"""
    rev_dict = {value:key for key,value in half_dict.items()} # 
    return {**half_dict, **rev_dict}

def joinkeys(dic):
    """Returns a concatenated string of all keys"""
    joined_keys = '['
    for key in dic.keys():
        joined_keys += str(key)
    return joined_keys + ']'

def position_list(substring, string):
    """Returns list of positions where substring is found in string"""
    return [match.start() for match in re.finditer(substring, string)]

def all_combinations(iterable):
    """Returns a list of tuples which of all combinations from a list of positions"""
    combs = []
    length = len(iterable)
    for size in range(1,length + 1):
        for subset in itertools.combinations(iterable, size):
            combs.append(subset)
    return combs

def varia_names(name, m_dict=LETTERS):
    """Returns list of names similar to argument, including argument as index 0"""
    twoway_dict = bi_dict(m_dict)
    re_from_dict = joinkeys(twoway_dict)
    all_combs = all_combinations(position_list(re_from_dict, name))
    list_name = list(name)
    all_names = [list_name]
    for positions in all_combs:
        new_name = list_name[:]
        for position_str in positions:
            position = int(position_str)
            letter = new_name[position]
            new_name[position] = str(twoway_dict[letter])
        all_names.append(new_name)
    return [''.join(name_list) for name_list in all_names]

def main():
    pass

if __name__ == '__main__':
    sys.exit(main())

