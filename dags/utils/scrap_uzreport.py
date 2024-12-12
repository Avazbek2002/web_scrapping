from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv


driver = webdriver.Chrome()
driver_page = webdriver.Chrome()

newslist_URL = 'https://uzreport.news/news-feed'
URL = "https://uzreport.news/"

driver.implicitly_wait(10)

driver.get(newslist_URL)
actions = ActionChains(driver)

button = driver.find_element(By.XPATH, '//button[@class="btn default"]')
button.click()
news_list = driver.find_elements(By.XPATH, '//div[@class="row flex"]')

page_num = 1

# Initialize CSV file
csv_file = "scrap_uzreport.csv"
fieldnames = ['Category', 'Title', 'Description', 'FullText']
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

wait = WebDriverWait(driver, 10)


while True:
    for news in news_list:
        try:
            news_link = news.find_element(By.TAG_NAME, 'a').get_attribute("href")
            news_date = news.find_element(By.XPATH, '//li[@class="time"]').find_element(By.TAG_NAME, "a").text
            # news_category = news.find_element(By.XPATH, '//li[@class="rubric"]').find_element(By.TAG_NAME, 'a').text
            news_category = wait.until(
                EC.presence_of_element_located((By.XPATH, '//li[@class="rubric"]/a'))
            ).text
            driver_page.get(news_link)
            news_title = driver_page.find_element(By.XPATH, '//div[@class="row center_panel_row"]').find_element(By.TAG_NAME, "h1").text
            paragraphs = driver_page.find_element(By.XPATH, '//div[@class="center_panel"]').find_elements(By.TAG_NAME, "p")
            page_pure_text = ""
            for para in paragraphs:
                page_pure_text = page_pure_text + para.text
            
            row = {
                        'Category': '',
                        'Title': news_title,
                        'Description': '',
                        'FullText': page_pure_text
            }

            # Write to CSV
            with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerow(row)

        except Exception as e:
            print(f"Error processing news item: {e}")

    try:
        button = driver.find_element(By.XPATH, '//a[@class="button load-more"]')
        actions.move_to_element(button).perform()
        button.click()
        time.sleep(3)
        news_list = driver.find_elements(By.XPATH, '//div[@class="row flex"]')
        news_list = news_list[page_num * 10: ]
        page_num += 1   
        print(len(news_list))
    except Exception as e:
        print("No more pages to load or error occurred:", e)
        break
