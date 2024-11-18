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

    # news_items = soup.find_all("article", class_="l-post grid-post grid-base-post mini__article")

    news_items = soup.find_all("h2", class_="is-title post-title")

    yesterday = datetime.now() - timedelta(days=1)
    today = datetime.now()

    yesterday = yesterday.strftime("/%Y/%m/%d")
    today = today.strftime("/%Y/%m/%d")

    stop_crawling = False
    current_page = 1
    current_pagesize = 10

    log_file = open("DaryoLogs.txt", "w")

    log_file.write("MAIN PAGE link: " + news_list_URL + "\n")

    while not stop_crawling:
        for news in news_items:
            article_link = news.find("a").get("href")

            news_date = article_link[:11]

            # if news_date == today:
            #     continue
            # elif news_date != yesterday:
            #     stop_crawling = True
            #     break

            # article_description = news.find("div", class_="excerpt")
            # if article_description:
            #     article_description = article_description.find("p").get_text()
            # else:
            #     article_description = ""

            # print(article_description)

            # article_link = news.find("a", class_="image-link media-ratio ratio-is-custom")
            
            
            article_page = requests.get(base_URL + article_link)
            log_file.write(base_URL + article_link + "\n")

            article_soup = BeautifulSoup(article_page.content, "html.parser")

            article_category = article_soup.find("a", "category term-color-1").get_text()

            article_title = article_soup.find("h1", class_="is-title post-title post-view-title").get_text()

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
        log_file.write("\n" + 20 * "-" + "\n" + "MAIN PAGE LINK: " + url + "\n")
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        news_items = soup.find_all("div", class_="post-meta post-meta-a has-below")
        print(len(news_items))
        current_page += 1
    
    return scrapped_data

scrap_daryo()