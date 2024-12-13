from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from datetime import datetime, timedelta
import Scrapper
import time
import csv

URL = "https://batafsil.uz/"
news_list_url = "https://batafsil.uz/all_news/"

class BatafsilScrapper(Scrapper):
    def __init__(self, URL, news_list_url):
        super().__init__(URL, news_list_url)
    def scrap():
        return