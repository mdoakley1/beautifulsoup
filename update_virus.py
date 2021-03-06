#!/usr/bin/python3

''' This web-scraping script collects data from the Coronavirus section of the
    worldometers.info website and presents it on the screen and updates a
    mysql database with the new data. '''

import datetime                     # pip3 install datetime
import requests                     # pip3 install requests
from   bs4 import BeautifulSoup     # pip3 install bs4
import lxml                         # pip3 install lxml
import mysql.connector              # pip3 install  mysql-connector-python

fls = [24, 12, 10, 10, 10, 12, 15, 12, 12, 10, 12, 12]  # Field widths

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
    x = lt.pop(0)              # First list member is not needed

    print()
    for l, fl in zip(lt, fls): # Print first line of lables
        print(f'{str(l[0]).strip(" "):>{fl}}', end='')
    print()
    for l, fl in zip(lt, fls): # Print second line of labels
        print(f'{str(l[1]).strip(" "):>{fl}}', end='')
    print()

#
# Extract data and print it
#
def print_data (trs, mydb, cursor):

    column_names = "(name, total_cases, new_cases, total_deaths, new_deaths, recovered, \
    active_cases, critical, cases_per_1M, deaths_per_1M, total_tests, test_per_1M, date)"

    yesterday = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')

    trs.pop(0)
    for tr in trs:
        tds = tr.find_all('td')    # Find all the cells (columns) in a row
        tds.pop(0)
        column_vals = []
        for td, fl in zip(tds, fls):
            val = str(td.text).strip('\n').strip(' ')
            print(f'{val:>{fl}}', end="")
            if val == "" or val == 'N/A':
                column_vals.append('NULL')
            else:
                column_vals.append(val.replace('+', '').replace(',', ''))
        print()

        if column_vals[0] != 'Total:':
            column_vals.append(yesterday)
            sql = ("INSERT INTO country_data " + column_names + " VALUES " + str(tuple(column_vals))).replace("'NULL'", "NULL")
            cursor.execute(sql)
            mydb.commit()



def retrieve_and_print():

    mydb = myconnection = mysql.connector.connect(host='localhost',
                                                  database='virus',
                                                  user='dba',
                                                  password='dba',
                                                  auth_plugin='mysql_native_password')
    cursor = mydb.cursor()

    soup = retrieve_html()
    day_div = soup.find('div', id='nav-yesterday', attrs={"aria-labelledby": "nav-yesterday-tab"})
    trs = day_div.find_all('tr')
    print_headings (BeautifulSoup(str(trs[0]), 'html.parser'))
    print_data (trs, mydb, cursor)


if __name__ == "__main__":
    retrieve_and_print()
