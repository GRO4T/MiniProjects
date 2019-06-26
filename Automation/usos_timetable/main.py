from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options

from time import sleep

timeout = 0.25 #timeout in seconds

SEMESTER = 3
KODY_PRZEDMIOTOW = []

#initialise the browser
options = Options()
options.headless = False #run in headless mode (invisible)
driver = webdriver.Firefox(options=options) #global browser handler

def WaitUntilDocReady(timeoutInSeconds, elem = 'div'): #elem is name of the crucial element to wait for
    try:
        elem = WebDriverWait(driver, timeoutInSeconds).until(EC.presence_of_element_located((By.CSS_SELECTOR, elem)))
        print('Page is Ready!')
        return True
    except TimeoutException:
        return False
def Login():
    USOS_URL = "https://cas.usos.pw.edu.pl/cas/login?service=https%3A%2F%2Fusosweb.usos.pw.edu.pl%2Fkontroler.php%3F_action%3Dlogowaniecas%2Findex&locale=pl"
    PLAN_URL = '\"http://www.elka.pw.edu.pl/Studia/Zalaczniki-i-formularze/Zalaczniki/Plany-modelowe-12/Informatyka-do-roku-2018-2019\"'
    LOGIN="99013100214"
    PASSWORD = "grzyby40"

    #USOS
    driver.get(USOS_URL)
    username = driver.find_element_by_id("username")
    username.send_keys(LOGIN)
    password = driver.find_element_by_id("password")
    password.send_keys(PASSWORD)
    submit = driver.find_element_by_name("submit")
    submit.send_keys(Keys.RETURN)
    #PLAN MODELOWY
    driver.execute_script('''window.open(''' + PLAN_URL + ''',"_blank");''')

def ParsePlanModelowy():
    sleep(2)
    driver.switch_to.window(driver.window_handles[1])
    table = driver.find_element_by_tag_name("table")
    rows = table.find_elements_by_tag_name("tr")
    for row in rows:
        columns = row.find_elements_by_tag_name("td")
        i = -1
        for col in columns:
            try:
                i += 1
                href = col.find_element_by_tag_name("a")
                if (i == SEMESTER):
                    href.click()
                    print("clicked" + href.text)
                    ExtractKodPrzedmiotu()
            except:
                pass
    sleep(1)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def ExtractKodPrzedmiotu():
    sleep(1)
    driver.switch_to.window(driver.window_handles[2])
    tables = driver.find_elements_by_tag_name("table")
    rows = tables[2].find_elements_by_tag_name("tr")
    kod_przedmiotu = rows[0].find_elements_by_tag_name("td")
    print(kod_przedmiotu[1].text)
    KODY_PRZEDMIOTOW.append(kod_przedmiotu[1].text)
    driver.close()
    driver.switch_to.window(driver.window_handles[1])

Login()
ParsePlanModelowy()
driver.get("https://usosweb.usos.pw.edu.pl/kontroler.php?_action=home/plany/index")
sleep(1)
kod_input = driver.find_element_by_class_name("text")
name = "fsda" + str(SEMESTER)
kod_input.send_keys(name)
submit = driver.find_element_by_class_name("submit")
submit.send_keys(Keys.RETURN)

#for code in KODY_PRZEDMIOTOW:
#    print("code")
#    driver.get("https://usosweb.usos.pw.edu.pl/kontroler.php?_action=home/plany/dodajWpisLista&plan_id=5112")
#
#    sleep(1)
