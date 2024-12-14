from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from datetime import datetime, timedelta
from Scrapper import Scrapper
import requests
import time

URL = "https://batafsil.uz/"
news_list_url = "https://batafsil.uz/all_news/"

class BatafsilScrapper(Scrapper):

    def parse(self):

        yesterday = (datetime.now() - timedelta(days=1)).strftime("%d")
        today = (datetime.now()).strftime("%d")
        page_num = 1
        self.driver_list.get(news_list_url)
        wait = WebDriverWait(self.driver_list, 10)
        actions = ActionChains(self.driver_list)

        button = self.driver_list.find_element(By.XPATH, ".//a[@class='btn btn-load-more js-btn-load-more']")

        news_list = self.driver_list.find_element(By.XPATH, ".//div[@class='_news-list']").find_elements(By.TAG_NAME, "article")

        stop_scrapping = False

        while not stop_scrapping:
            for news in news_list:
                actions.move_to_element(news).perform()

                news_link = news.find_element(By.XPATH, ".//h3/a").get_attribute("href")

                self.log_file.write(news_link + "\n")

            
                # news_date = news.find_element(By.XPATH, ".//div[@class='post-date']/time").text.split()[0]

                            
                # if news_date == today:
                #     continue
                # elif news_date != yesterday:
                #     stop_scrapping = True
                #     break

                self.driver_page.get(news_link)
                
                news_title = self.driver_page.find_element(By.XPATH, ".//div[@class='inhype-post-details']/h1").text
                
                paragraphs = self.driver_page.find_element(By.XPATH, ".//div[@class='detail-text']").find_elements(By.TAG_NAME, "p")

                news_category = self.driver_page.find_element(By.XPATH, ".//span[@class='cat-title']").text

                page_pure_text = ''

                for para in paragraphs:
                    page_pure_text = page_pure_text + para.text
                
                all_the_text = f"{news_category} !@ {news_title} !@ {page_pure_text}"

                payload = {
                    "text": all_the_text
                }

                response = requests.post(url="http://172.16.117.62:8088/cyr2lat/", json=payload)

                converted_text = response.json()["converted"]

                [news_category, news_title, page_pure_text] = converted_text.split("!@")

                print(news_category.strip() + " " + news_title.strip())
                
                self.write_csv_file(news_title.strip(), news_category.strip(), '', page_pure_text.strip())
            

            
            actions.move_to_element(button).perform()

            button.click()

            time.sleep(5)

            news_list = self.driver_list.find_element(By.XPATH, ".//div[@class='_news-list']").find_elements(By.TAG_NAME, "article")[page_num * 9 :]

            print("Next page ----------------->>>>>>")

            self.log_file.write("Next page ----------------->>>>>> \n")

            print(len(news_list) )
            page_num += 1

        return

scrapper = BatafsilScrapper(URL, news_list_url)
scrapper.parse()