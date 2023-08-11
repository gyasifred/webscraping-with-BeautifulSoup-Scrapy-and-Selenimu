from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd



website = "https://www.adamchoi.co.uk/overs/detailed"
path = "/home/kgyasi/webscraping-with-BeautifulSoup-Scrapy-and-Selenium/chromedriver"
driver = webdriver.Chrome(path)
driver.get(website)
all_matches_buttom = driver.find_element(By.XPATH, "//label[@analytics-event = 'All matches']")
all_matches_buttom.click()
season_22_23= driver.find_element(By.XPATH, '//*[@id="season"]/option[2]')
season_22_23.click()
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
             'Scores': score, "Away": away_team })
print(df.head())
df.to_csv("epl_matches.csv", index=False)