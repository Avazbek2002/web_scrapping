import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv

def scrap_zarnews():
    URL = "https://zarnews.uz/uz/yangiliklar/qisqacha"

    scrapped_data = []

    csv_file = "zarnews.csv"
    
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Category', 'Title', 'Description', 'Full Text'])
        writer.writeheader()

        page = request_page(URL)

        soup = BeautifulSoup(page.content, "html.parser")

        news_items = soup.find_all("article", class_="post-list-small__entry clearfix")[:-6]

        day_before_yesterday = (datetime.now() - timedelta(days=2)).strftime("%d/%m")

        log_file = open("zarnewsLogs.txt", "w")

        log_file.write("MAIN PAGE link: " + URL + "\n")

        stop_crawling = False

        offset = 20
        page_order = 2

        while not stop_crawling:
            for news in news_items:
                news_date = news.find("li", class_="entry__meta-date").get_text().strip().split(",")

                # # if yesterday
                # if len(news_date) == 1 or news_date[0] == "Bugun":
                #     continue
                # elif news_date[0] == day_before_yesterday:
                #     stop_crawling = True
                #     break

                article_link = news.find("a").get("href")

                log_file.write(article_link + "\n")

                article_page = request_page(article_link)

                article_soup = BeautifulSoup(article_page.content, "html.parser")

                article_title = article_soup.find("h1", class_="single-post__entry-title").get_text().strip()

                article_category = article_soup.find("li", class_="entry__meta-comments").find("a").get_text().strip()

                article_paras = article_soup.find("div", class_="entry__article").find_all("p")

                page_pure_text = ""

                for paragraph in article_paras:
                    text = paragraph.text.replace("🔹", "").strip()

                    page_pure_text = page_pure_text + text

                row_news = {
                    'Category': article_category,
                    'Title': article_title,
                    'Description': "",
                    'Full Text': page_pure_text
                }

                writer.writerow(row_news)

                scrapped_data.append(row_news)
            
            extended_link = f"https://zarnews.uz/uz/yangiliklar/qisqacha?load={page_order * 20}"

            log_file.write("\n" + 20 * "-" + "\n" + "MAIN PAGE LINK: " + extended_link + "\n")

            article_page = request_page(extended_link)

            article_soup = BeautifulSoup(article_page.content, "html.parser")

            news_items = article_soup.find_all("div", class_="post-list-small__body")[:-6][offset:]
    
    return news_items



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


scrap_zarnews()