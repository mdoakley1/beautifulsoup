#!/usr/bin/python3

import os
from   selenium import webdriver
from   selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("https://www.facebook.com")
ids = driver.find_elements_by_xpath('//*[@id]')

user = driver.find_element_by_name('email')
user.click()
user.send_keys('moakley.email@gmail.com')

pwd = driver.find_element_by_name('pass')
pwd.click()
pwd.send_keys('/jun282018')
#pwd.send_keys(Keys.RETURN)

lbut = driver.find_element_by_xpath("//*[@id='loginbutton']")
lbut.click()

input()
driver.close()
