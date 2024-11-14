import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

def scrap_daryo():
    base_URL = "https://daryo.uz/"
    news_list_URL = "https://daryo.uz/yangiliklar"

    scrapped_data = []
    page = requests.get(news_list_URL)

    soup = BeautifulSoup(page.content, "html.parser")

    news_items = soup.find_all("article", class_="l-post grid-post grid-base-post mini__article")
    print(len(news_items))

    stop_crawling = False
    current_page = 1
    current_pagesize = 10

    while not stop_crawling:
        for news in news_items:
            news_date = news.find("time", class_="post-date").get_text().split(",")

            if news_date[0] == "Bugun":
                continue
            elif news_date[0] != "Kecha":
                stop_crawling = True
                break

            # article_description = news.find("div", class_="excerpt")
            # if article_description:
            #     article_description = article_description.find("p").get_text()
            # else:
            #     article_description = ""

            # print(article_description)

            article_link = soup.find("a", class_="image-link media-ratio ratio-is-custom").get("href")
            
            article_page = requests.get(base_URL + article_link)

            article_soup = BeautifulSoup(article_page.content, "html.parser")

            article_category = article_soup.find("a", "category term-color-1").get_text()

            article_title = article_soup.find("h1", class_="is-title post-title post-view-title").get_text()
            print(article_title)

            article_paras = article_soup.find("div", class_="the-post s-post-modern").find_all("p")

            page_pure_text = ""

            for paragraph in article_paras:
                
                page_pure_text = page_pure_text + paragraph.text

            page_pure_text = page_pure_text.replace('\n', '').replace('\xa0', '')

            row_news = {
                'Category': article_category,
                'Title': article_title,
                'Description': '',
                'Full Text': page_pure_text
            }

            scrapped_data.append(row_news)


        url = f"{news_list_URL}?page={current_page}&per-page={current_pagesize}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        news_items = soup.find_all("div", class_="post-meta post-meta-a has-below")
        current_page += 1
    
    return scrapped_data

scrap_daryo()