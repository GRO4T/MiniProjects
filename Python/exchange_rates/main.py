from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options

from time import sleep

timeout = 0.25 #timeout in seconds

#initialise the browser
options = Options()
options.headless = True #run in headless mode (invisible)
driver = webdriver.Firefox(options=options) #global browser handler

def Google(phrase):
    driver.get("https://www.google.com/")
    search_box = driver.find_element_by_name("q")
    search_box.clear()
    search_box.send_keys(phrase)
    search_box.send_keys(Keys.RETURN)

def WaitUntilDocReady(timeoutInSeconds):
    try:
        elem = WebDriverWait(driver, timeoutInSeconds).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.dDoNo.vk_bk')))
        print('Page is Ready!')
        return True
    except TimeoutException:
        return False

def SearchForExchangeRates(currencyA, currencyB = 'pln'):
    Google(currencyA + ' to ' + currencyB)
    while not WaitUntilDocReady(timeout):
        print('Waiting for the page to load')

    exchange = driver.find_element_by_css_selector('div.dDoNo.vk_bk')
    print(currencyA.upper() + ' = ' + exchange.text)

SearchForExchangeRates('usd')
SearchForExchangeRates('euro')
SearchForExchangeRates('gbp')

driver.close()
