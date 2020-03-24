#!/usr/bin/python3

import os
from   selenium import webdriver

#
# Outsie this script use chrome to right-click on element to inspect
#

driver = webdriver.Firefox()
driver.get("http://econpy.pythonanywhere.com/ex/001.html")

# /html/body/div[2]/div
buyers = driver.find_elements_by_xpath('//div[@title="buyer-name"]')
prices = driver.find_elements_by_xpath('//span[@class="item-price"]')

#for b, p in enumerate (zip (buyers, prices)):
#    print (b, p[0].text, p[1].text)

for b, p in zip (buyers, prices):
    print (b.text, p.text)

driver.close()
