#!/usr/bin/python3

''' This web-scraping script collects data from the Coronavirus section of the
    worldometers.info website and presents it on the screen. '''

import requests
from   bs4 import BeautifulSoup
import lxml


# Field length size (in characters) for fields we print
fls = [24, 12, 10, 10, 10, 12, 15, 12, 12, 10, 12, 12]

def retrieve_html():
    source = requests.get('https://www.worldometers.info/coronavirus/#countries.com')
    return (BeautifulSoup(source.text, 'lxml'))

#
# Extract column labels from html and print them out.
#
def print_headings (tr):

    ll = []                    # list of labels
    lt = []                    # table of list of labels (top line and bottom line)

    ths = tr.find_all('th')    # Locate all header tags and save
    for th in ths:
        for c in th.children:
            if str(type(c)) == "<class 'bs4.element.NavigableString'>":
                ll.append(c)
        lt.append(ll)          # Put list into table
        ll = []

    x = lt.pop()               # Last list member is not needed

    print()
    for l, fl in zip(lt, fls): # Print first line of lables
        print(f'{str(l[0]).strip(" "):>{fl}}', end='')
    print()
    for l, fl in zip(lt, fls): # Print second line of labels
        print(f'{str(l[1]).strip(" "):>{fl}}', end='')
    print()

#
# Remove the first element from a bs4.element.ResultSet variable
#
def remove_first_element(trs):
    trs.reverse()
    trs.pop()
    trs.reverse()

#
# Extract data and print it
#
def print_data (trs):
    remove_first_element(trs)
    for tr in trs:
        tds = tr.find_all('td')    # Find all the cells (columns) in a row
        for td, fl in zip(tds, fls):
            val = str(td.text).strip('\n').strip(' ')
            print(f'{val:>{fl}}', end="")
        print()

def retrieve_and_print():
    soup = retrieve_html()
    for day in 'today', 'yesterday':
        id_string = 'nav-' + day
        attrs_value = id_string + '-tab'
        day_div = soup.find('div', id=id_string, attrs={"aria-labelledby": attrs_value})
        trs = day_div.find_all('tr')
        print_headings (BeautifulSoup(str(trs[0]), 'html.parser'))
        print_data (trs)


if __name__ == "__main__":
    retrieve_and_print()
