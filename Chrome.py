#! /usr/bin/python2
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)  # 使用无界面的Chrome浏览器

driver.get('http://admin:admin@192.168.1.1')
sleep(2)

driver.switch_to_frame("mainFrame")
elem_dh = driver.find_elements_by_xpath("/html/body/center/form/table[2]/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td[2]")
ele = elem_dh[0].text
print(ele)

driver.quit()
