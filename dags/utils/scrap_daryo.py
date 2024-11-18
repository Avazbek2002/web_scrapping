import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

def scrap_daryo():
    base_URL = "https://daryo.uz/"
    news_list_URL = "https://daryo.uz/yangiliklar"

    scrapped_data = []
    page = request_page(news_list_URL)

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
                
            article_page = request_page(base_URL + article_link)
            log_file.write(base_URL + article_link + "\n")

            article_soup = BeautifulSoup(article_page.content, "html.parser")
            
            if article_soup.find("div", class_="not-found"):
                print("not found")
                continue

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
        page = request_page(url)
        soup = BeautifulSoup(page.content, "html.parser")
        news_items = soup.find_all("div", class_="post-meta post-meta-a has-below")
        print(len(news_items))
        current_page += 1
    
    return scrapped_data

def request_page(link):
    try:
        extended_page = requests.get(link)
        # Check if the request was successful
        if extended_page.status_code == 200:
            print("Item page fetched successfully!")
        else:
            print(f"Failed to fetch the item page. Status code: {extended_page.status_code}")

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error occurred: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return extended_page

scrap_daryo()