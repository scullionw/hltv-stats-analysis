#!/usr/bin/env python3
# coding: utf-8

# TODO: identical names (compare teams), rating per game to get variance

import requests
import bs4
import re
import sys
import functools
from varia import varia_names as vn

def player_id(name):
    QUERY_URL = 'http://www.hltv.org/?pageid=152&query='
    player_search_response = requests.get(QUERY_URL + name)
    player_page_soup = bs4.BeautifulSoup(player_search_response.text, 'html.parser')
    elem = player_page_soup.select('.searchListBox div a')[0].get('href')
    player_id_regex_1 = re.compile(r'/player/(\d+)-.*')
    player_id_regex_2 = re.compile(r'playerid=(\d+)')
    match = player_id_regex_1.search(elem)
    if match is None:
        match = player_id_regex_2.search(elem)
    
    return match.group(1)

def filter_num(time_filter, match_filter):
    time_dict = {
        'all': 0,
        '2012': 1,
        '2013': 2,
        '2014': 3,
        '2015': 4,
        '2016': 9,
        'p3m': 5,    
    }
    match_dict = {
        'all': 0,
        'online': 1792,
        'lan': 2048,
        'majors': 1536,
        'bigevents': 2816,   
    }
    final_filter = time_dict[time_filter] + match_dict[match_filter]
    
    return str(final_filter)
    
def player_stats_url(name, time_filter='all', match_filter='all'):
    base_url = 'http://www.hltv.org/?pageid=173'
    p_url = ''
    for p_name in vn(name):
        try:
            p_url = player_id(p_name)
            break
        except IndexError:
            pass
    if not p_url:
        raise Exception('PlayerNotFound')
    id_url = 'playerid=' + p_url
    filter_url = 'statsfilter=' + filter_num(time_filter, match_filter)
    
    return '&'.join([base_url, filter_url, id_url])

def stat_from_url(player_url, stat_string='rating'):
    stat_page = requests.get(player_url)
    soup = bs4.BeautifulSoup(stat_page.text, 'html.parser')
    re_string = r'\s*' + stat_string + r'\s*'
    name_elem = soup.find(string=re.compile(re_string, re.I))
    stat_elem = name_elem.parent.next_sibling.string
      
    return str(stat_elem)

@functools.lru_cache(maxsize=None)
def stats(player, stat='rating', time_filter='all', match_filter='all'):
    try:
        player_url = player_stats_url(player.lower(), time_filter, match_filter)
    except:
        return 'N/A'
    statistic = stat_from_url(player_url, stat)

    return statistic

def manual_entry():
    player = ''
    while not player:
        player = input('Player? ')
    print(player, '<--')
    stat = input('Statistic name? ')
    if not stat:
        stat = 'rating'
    print(stat,'<--')
    time_filter = input('Time period? ')
    if not time_filter:
        time_filter = 'all'
    print(time_filter,'<--')
    match_filter = input('For which type of matches? ')
    if not match_filter:
        match_filter = 'all'
    print(match_filter,'<--')
    print('scraping...')

    return player, stat, time_filter, match_filter

def main():
    
    if len(sys.argv) > 1:
        return stats(sys.argv[1], *sys.argv[2:5])
    else:
        player, stat, time_filter, match_filter = manual_entry()
        statistic = stats(player, stat, time_filter, match_filter)
        return  "--> {0}'s {1} during {2} for {3} matches was {4}".format(player, stat, time_filter, match_filter, statistic)
        
if __name__ == '__main__':
    sys.exit(main())



