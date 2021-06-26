# coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from django.utils.encoding import smart_str, smart_unicode

# set chromedriver
DRIVER_PATH = '../chromedriver'
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
# get website
driver.get("https://prod.chronorace.be/virtualchallenge/challengeregistration.aspx?chal=3&lng=EN")

# Small counter so you can see how far you've got with scraping
result = []
count = 0

# Infinite loop
while True:
    print("START RUN: " + count.__str__())
    # Search table for TR's
    elements = driver.find_elements_by_css_selector("#allResultsTable > tbody tr")
    # for every TR
    for element in elements:
        # search voor TD elements
        row = element.find_elements_by_css_selector('td')
        row_elements = []
        # loop over all TD's
        for rowElement in row:
            # save TD in an array
            row_elements.append(smart_str(rowElement.text))
        # add array to result
        result.append(row_elements)
    try:
        # Search for 'next' button with class "disabled"
        # If there is none found, throw an error and stop the loop
        driver.find_element_by_css_selector("#allResultsTable_next.disabled")
        # Loop stoppen
        break
    except NoSuchElementException:
        # When an error occurs
        # Click the item
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#allResultsTable_next"))).click()
        count = count + 1
        # Print to see what happened
    print("END OF RUN: Total '" + len(result).__str__())

#Data opslagen
print("START: Saving file")
df = pd.DataFrame(result)
df.to_csv('chronoresults.csv')
print("We done fam")

driver.quit()
