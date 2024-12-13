import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import csv
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/70.0.3538.77 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://google.com",
}

URL = "https://oz.sputniknews.uz"
news_list_url = "https://oz.sputniknews.uz/archive"

log_file = open("sputnikLogs.txt", "w")

log_file.write("MAIN PAGE link: " + news_list_url + "\n")

csv_file = "sputnik_scrap.csv"

# function to request a page with certain link
def request_page(link, headers):
    soup = ""
    try:
        page = requests.get(link, headers=headers)

        soup = BeautifulSoup(page.content, "html.parser")

        # Check if the request was successful
        if page.status_code == 200:
            print("Item page fetched successfully!")
        else:
            print(f"Failed to fetch the item page. Status code: {page.status_code}")

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error occurred: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return soup


soup = request_page(news_list_url, headers=headers)
news_items = soup.find_all("div", class_="list__item")
stop_crawling = False

yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
today = datetime.now().strftime("%Y/%m/%d")
the_day_before_yesterday = (datetime.now() - timedelta(days=2)).strftime("%Y%m%d")

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Category', 'Title', 'Description', 'Full Text'])
    writer.writeheader()

    while not stop_crawling:
        for news in news_items:
            time.sleep(2)
            article_link = news.find("a").get("href")

            if not article_link.startswith("https"):
                article_link = URL + article_link

            article_date = article_link[1:9]

            # if today == article_date:
            #     continue
            # elif article_date == the_day_before_yesterday:
            #     stop_crawling = True
            #     break


            article_page = request_page(article_link, headers).find("div", class_="article")
            log_file.write(URL + article_link + "\n")

            article_title = article_page.find("h1", class_="article__title").get_text().strip()

            article_category = article_page.find("li", class_="tag").find("a").get_text()

            print(article_title)

            article_description = article_page.find("div", class_="article__announce-text")
            
            if not article_description:
                article_description = ''
            else:
                article_description = article_description.get_text().strip()

            

            article_paras = article_page.find_all("div", class_="article__block")

            page_pure_text = ""

            for i, para in enumerate(article_paras):
                if para.get("data-type") == "article":
                    continue
                if para.get("data-type") == "media":
                    continue
                if para.get("data-type") == "photolenta":
                    continue

                if i == 0:
                    text = re.sub(r'^.*?— Sputnik\.', '', para.text).strip()
                else:
                    text = para.text.strip()

                page_pure_text = page_pure_text + text

            row_news = {
                'Category': article_category,
                'Title': article_title,
                'Description': article_description,
                'Full Text': page_pure_text
            }
            
            writer.writerow(row_news)

        time.sleep(2)
        extended_link = soup.find("div", class_="list-items-loaded")

        if extended_link:
            extended_link = extended_link.get("data-next-url")
        else:
            extended_link = soup.find("div", class_="list__more").get("data-url")

        log_file.write("\n" + 20 * "-" + "\n" + "MAIN PAGE LINK: " + news_list_url + extended_link + "\n")

        soup = request_page(URL + extended_link, headers)

        news_items = soup.find_all("div", class_="list__item")

        print(len(news_items))