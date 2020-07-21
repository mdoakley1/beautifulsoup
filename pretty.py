#!/usr/bin/python3

'''
    Simple script to read a web page and create a file with the corresponding
    formatted ("pretty") html. Example:
    
        ./pretty.py   http://google.com
'''

import sys
import requests
from bs4 import BeautifulSoup
import lxml

try:
    url = sys.argv[1]
except IndexError:
    url = input('Enter url : ')

print ('Retrieving: ', url)


source = requests.get(url)
pretty = BeautifulSoup(source.text, 'lxml').prettify()
print('Lines     : ', pretty.count('\n'))

with open('pretty.html', 'w') as f:
    f.write(pretty)
    print('pretty.html written')

exit()
