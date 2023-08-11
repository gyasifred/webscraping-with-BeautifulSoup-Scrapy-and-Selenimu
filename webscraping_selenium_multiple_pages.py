import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.headless = True
options.add_argument('window-size=1920x1080')
web = "https://www.audible.com/search"
path = "/home/kgyasi/webscraping-with-BeautifulSoup-Scrapy-and-Selenium/chromedriver"
driver = webdriver.Chrome(path, options=options)
driver.get(web)
# driver.maximize_window()
container = driver.find_element_by_class_name("adbl-impression-container")
products = container.find_elements_by_xpath(
    './/li[contains(@class, "productListItem")]')
title = []
authors = []
length = []
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
driver.quit()
df = pd.DataFrame({"Title": title,
                   "Author": authors,
                   "Length": length})
df.to_csv("books.csv", index=False)
