import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import csv

URL = "https://www.gazeta.uz"
news_list_URL = "https://www.gazeta.uz/oz/archive/"

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/70.0.3538.77 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://google.com",
    }


log_file = open("gazetaLogs.txt", "w")

log_file.write("MAIN PAGE link: " + news_list_URL + "\n")

csv_file = "gazeta_scrap.csv"
page_order = 2

# function to request a page with certain link
def request_page(link, headers):
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


# function to scrap the article page
def scrap_article_page(link):
    
    article_page = request_page(link, headers)
    log_file.write(link + article_link + "\n")

    article_title = article_page.find(id="article_title").get_text().strip()

    article_description = article_page.find("div", class_="js-mediator-article").find("h4").get_text().strip()

    article_paras = article_page.find("div", class_="js-mediator-article article-text").find_all("p")

    article_category = article_page.find("span", itemprop="name").get_text().strip()
            
    page_pure_text = ""

    for para in article_paras:
        text = para.text.replace("\"Gazeta.uz\"da reklama", " ").strip()

        page_pure_text = page_pure_text + text

    row_news = {
        'Category': article_category,
        'Title': article_title,
        'Description': article_description,
        'Full Text': page_pure_text
    }
    
    return row_news



soup = request_page(news_list_URL, headers=headers)
news_items = soup.find_all("div", class_="nblock")
stop_crawling = False

yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y/%m/%d")
today = datetime.now().strftime("%Y/%m/%d")
the_day_before_yesterday = (datetime.now() - timedelta(days=2)).strftime("%Y/%m/%d")


with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Category', 'Title', 'Description', 'Full Text'])
    writer.writeheader()

    while not stop_crawling:
        for news in news_items:
            article_link = news.find("a").get("href")
            article_date = article_link[4:14]

            # if today == article_date:
            #     continue
            # elif article_date == the_day_before_yesterday:
            #     stop_crawling = True
            #     break
            
            row_news = scrap_article_page(URL + article_link)

            writer.writerow(row_news)

        extended_link = f"https://www.gazeta.uz/oz/archive?page={page_order}"
        log_file.write("\n" + 20 * "-" + "\n" + "MAIN PAGE LINK: " + extended_link + "\n")

        soup = request_page(extended_link, headers)

        news_items = soup.find_all("div", class_="nblock")
        page_order += 1




            


