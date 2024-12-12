from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()

newslist_URL = 'https://uzreport.news/news-feed'
URL = "https://uzreport.news/"

driver.implicitly_wait(3)

driver.get(newslist_URL)

news_list = driver.find_elements(By.XPATH, '//div[@class="row flex"]')

for news in news_list:
    news_preview = news.find_element(By.TAG_NAME, 'a')
    news_link = news_preview.get_attribute("href")
    news_title = news_preview.text
    date = news.find_element(By.XPATH, '//li[@class="time"]').find_element(By.TAG_NAME, "a").text
    # driver.get(news_link)
    print(date)