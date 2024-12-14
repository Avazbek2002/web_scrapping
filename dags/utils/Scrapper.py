from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import csv



class Scrapper:
    def __init__(self, URL, list_url):
        self.driver_list = self.driver_config()
        self.driver_page = self.driver_config()
        self.driver_page.implicitly_wait(10)
        self.driver_list.implicitly_wait(10)
        self.website_name = urlparse(URL).netloc.split('.')[0]
        self.log_file = open(f"{self.website_name}Logs.txt", "w", buffering=1, encoding='utf-8')

        self.csv_file = self.create_csv_file(f"{self.website_name}_scrap.csv")
    
    def create_csv_file(self, file_name):
        csv_file = open(file_name, "w")
        writer = csv.DictWriter(csv_file, fieldnames=['Category', 'Title', 'Description', 'FullText'])
        writer.writeheader()

        return writer

    def write_csv_file(self, article_title, article_category, article_description, page_pure_text):
        row_news = {
            'Title': article_title,
            'Category': article_category,
            'Description': article_description,
            'FullText': page_pure_text
        }
            
        self.csv_file.writerow(row_news)

    def driver_config(self):
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument("--headless")
        self.options.add_argument("-profile")
        self.options.add_argument("--allow-profiles-outside-user-dir")
        self.options.add_argument("--enable-profile-shortcut-manager")
        self.options.add_argument("--disable-blink-features=AutomationControlled")

        return webdriver.Chrome(options=self.options)
    
    def parse(self):
        return

