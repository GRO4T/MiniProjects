from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options

from time import sleep

SEMESTER = 3
KODY_PRZEDMIOTOW = []

#initialise the browser
options = Options()
options.headless = False #run in headless mode (invisible)
driver = webdriver.Firefox(options=options) #global browser handler

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
    driver.execute_script('''window.open(''' + PLAN_URL + ''',"_blank");''') #otwiera nową kartę
    driver.switch_to.window(driver.window_handles[1])

def ParsePlanModelowy():
    #wait till page is ready
    try:
        table = WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
        ExtractTable(table)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return True
    except TimeoutException:
        return False

def ExtractTable(table):
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
                    ExtractKodPrzedmiotu()
            except:
                pass

def ExtractKodPrzedmiotu():
    sleep(1)
    driver.switch_to.window(driver.window_handles[2])
    tables = driver.find_elements_by_tag_name("table") #wyszukujemy wszystkie elementy typu table, a nastepnie wybieramy tabele z kodem przedmiotu
    rows = tables[2].find_elements_by_tag_name("tr") # znajdujaca sie pod indeksem 2
    kod_przedmiotu = rows[0].find_elements_by_tag_name("td")
    print(kod_przedmiotu[1].text)
    KODY_PRZEDMIOTOW.append(kod_przedmiotu[1].text)
    driver.close() # powrot do strony planu modelowego
    driver.switch_to.window(driver.window_handles[1])

def CreatePlan():
    driver.get("https://usosweb.usos.pw.edu.pl/kontroler.php?_action=home/plany/index")
    sleep(1)
    nowy_plan_textfield = driver.find_element_by_class_name("text")
    nowy_plan_textfield.send_keys("sem" + str(SEMESTER))
    submit = driver.find_element_by_css_selector("input[value='Utwórz']")
    submit.submit()
    FillPlan()

def FillPlan():
    for code in KODY_PRZEDMIOTOW:
        sleep(0.5)
        dodaj_zawartosc = driver.find_element_by_xpath("//*[text()='dodaj nową zawartość']")
        dodaj_zawartosc.click()
        AddPrzedmiot(code)
    #zapisz zmiany
    save_button = driver.find_element_by_xpath("//input[@value='Zapisz zmiany']")
    save_button.click()

def AddPrzedmiot(kod_przedmiotu):
    #dodaj zawartość
    sleep(1)
    pattern_elem_list = driver.find_elements_by_name("_pattern")
    pattern_elem_list[2].send_keys(kod_przedmiotu) # na indeksie numer 2 znajduje się pole do którego chcemy podać kod przedmiotu
    ok_button_list = driver.find_elements_by_xpath("//input[@value='OK']")
    ok_button_list[4].click()

    #sprawdz czy zapytanie nie było dwuznaczne (np. są 2 podobne przedmioty do wyboru)
    try:
        sleep(1)
        niejednoznacza = driver.find_element_by_xpath("//input[@value='Szukaj ponownie']")
        print("Request ambiguous")
        odd_rows = driver.find_elements_by_class_name("odd_row")
        wybierz_kontynuuj = odd_rows[0].find_elements_by_tag_name("td")[-1]
        wybierz_kontynuuj.find_element_by_tag_name("a").click()
    except Exception as e:
        print(e)
        pass
    #wybierz realizację
    sleep(1)
    container = driver.find_element_by_class_name("wrtext")
    wybierz = container.find_elements_by_tag_name("a")
    wybierz[0].click()

    #rozbij
    rozbij_button_list = driver.find_elements_by_xpath("//*[text()='rozbij']")
    rozbij_button_list[-1].click()
    zapisz = driver.find_element_by_class_name("submit")
    zapisz.click()


Login()
while not ParsePlanModelowy():
    pass
CreatePlan()

