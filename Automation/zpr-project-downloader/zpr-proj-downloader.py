#!/bin/python3
# Usage:
#       python3 zpr-proj-downloader.py [username] [password]
#
# Dependencies:
#   * requests module
#   * selenium module
#   * geckodriver for Firefox (or sth else)

import os, requests, sys
from selenium import webdriver

if not os.path.isdir('./projects'):
    os.mkdir('projects')

url = "http://eve.ii.pw.edu.pl:9009/students/ZPR/projects/"

browser = webdriver.Firefox()

browser.get(url)

id_field = browser.find_element_by_xpath("//input[@id='username']")
id_field.send_keys(sys.argv[1])

password_field = browser.find_element_by_xpath("//input[@id='password']")
password_field.send_keys(sys.argv[2])

submit_button = browser.find_element_by_xpath("//input[@name='submit']")
submit_button.click()

pick_zpr_button = browser.find_element_by_xpath("//input[@id='id_selection_7']")
pick_zpr_button.click()

for i in range(468, 1000):
    browser.get(url + str(i))
    content = browser.page_source
    if "This is not the page you were looking for" in content:
        print("Skipping: " + str(i))
        continue
    print("Found: " + str(i))
    file = open('projects/index' + str(i) + '.html', 'w')
    file.write(content)
    file.close()
