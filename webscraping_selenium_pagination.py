import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.headless = False
options.add_argument('window-size=1920x1080')
web = "https://www.audible.com/adblbestsellers?ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=1bb99d4d-8ec8-42a3-bb35-704e849c2bc6&pf_rd_r=1AP97ZH38BQ2TBD212V0&pageLoadId=IMRdKQWkl5gs4wQN&creativeId=1642b4d1-12f3-4375-98fa-4938afc1cedc"
path = "/home/kgyasi/webscraping-with-BeautifulSoup-Scrapy-and-Selenium/chromedriver"
driver = webdriver.Chrome(path, options=options)
driver.get(web)
driver.maximize_window()

# pagination
pagination = driver.find_element_by_xpath(
    '//ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements_by_tag_name('li')
last_page = int(pages[-2].text)
title = []
authors = []
length = []
cnt = 1
while cnt <= last_page:
    # Implicit Wait
    #time.sleep(2)
    # container = driver.find_element_by_class_name('adbl-impression-container ')
    # Explicit Wait
    container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container ')))
    # products = container.find_elements_by_xpath('.//li[contains(@class, "productListItem")]')
    products = WebDriverWait(container, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/li[contains(@class, "productListItem")]')))
    for product in products:
        heading = product.find_element_by_xpath(
            ".//h3[contains(@class, 'bc-heading')]").text
        title.append(heading)
        author = product.find_element_by_xpath(
            ".//li[contains(@class, 'authorLabel')]").text
        authors.append(author.split(":")[1].strip())
        audio_len = product.find_element_by_xpath(
            ".//li[contains(@class, 'runtimeLabel')]").text
        length.append(audio_len.split(":")[1].strip())
    cnt += 1
    try:
        next_page = driver.find_element_by_xpath(
            '//span[contains(@class, "nextButton")]')
        next_page.click()
    except:
        pass
driver.quit()
df = pd.DataFrame({"Title": title,
                   "Author": authors,
                   "Length": length})
df.to_csv("books.csv", index=False)
