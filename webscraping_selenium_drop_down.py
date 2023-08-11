from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import pandas as pd


website = "https://www.adamchoi.co.uk/overs/detailed"
path = "/home/kgyasi/webscraping-with-BeautifulSoup-Scrapy-and-Selenium/chromedriver"
driver = webdriver.Chrome(path)
driver.get(website)
all_matches_buttom = driver.find_element(
    By.XPATH, "//label[@analytics-event = 'All matches']")
all_matches_buttom.click()

# select dropdown and select element inside by visible text
country_dropdown = Select(driver.find_element_by_id('country'))
country_dropdown.select_by_visible_text('Spain')
# implicit wait (useful in JavaScript driven websites when elements need seconds to load and avoid error "ElementNotVisibleException")
time.sleep(3)

# season dropdown
season_dropdown = Select(driver.find_element_by_id('season'))
season_dropdown.select_by_visible_text('21/22')
time.sleep(5)

matches = driver.find_elements(By.TAG_NAME, "tr")
date = []
home_team = []
score = []
away_team = []
for match in matches:
    date.append(match.find_element(By.XPATH, "./td[1]").text)
    home_team.append(match.find_element(By.XPATH, "./td[2]").text)
    score.append(match.find_element(By.XPATH, "./td[3]").text)
    away_team.append(match.find_element(By.XPATH, "./td[4]").text)

df = pd.DataFrame({'Date': date, 'Home': home_team,
                   'Scores': score, "Away": away_team})
print(df.head())
df.to_csv("laliga_matches.csv", index=False)
