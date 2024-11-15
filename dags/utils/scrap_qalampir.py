import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv

def scrap_qalampir():
    URL = "https://qalampir.uz"
    news_url_list = "https://qalampir.uz/uz/latest"
    csv_file = "qalampir_news.csv"

    # Prepare CSV file
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Category', 'Title', 'Full Text'])
        writer.writeheader()

        page = request_page(news_url_list)
        soup = BeautifulSoup(page.content, "html.parser")
        news_items = soup.find_all("div", class_="col-lg-4 col-md-6")

        stop_crawling = False
        yesterday = datetime.now() - timedelta(days=1)
        formatted_date = yesterday.strftime("%d")

        offset = 30
        load_articles = 30

        while not stop_crawling:
            for news in news_items:
                texts = news.find("span", class_="date").get_text().strip().split()
                if len(texts) == 1:
                    continue
                elif texts[0] != formatted_date:
                    stop_crawling = True
                    break

                news_url = news.find("a").get("href")

                news_page = request_page(URL + news_url)
                article_soup = BeautifulSoup(news_page.content, "html.parser")

                page_title = article_soup.find("div", class_="title").get_text()
                page_content = article_soup.find("div", class_="content-main-titles")
                page_category = article_soup.find("div", class_="content-main-hero-info content-main-hero-info-top").find("p").get_text()
                page_paragrpahs = page_content.find_all("p")

                page_pure_text = ""

                for para in page_paragrpahs:
                    page_pure_text = page_pure_text + para.get_text()

                    links = para.find_all('a')
                    for link in links:
                        # Replace the link tag with just its text content
                        link.replace_with(link.get_text())

                page_pure_text = page_pure_text.replace('\n', '').replace('\xa0', '')

                row_news = {
                    'Category': page_category,
                    'Title': page_title,
                    'Full Text': page_pure_text
                }

                # Write row to CSV
                writer.writerow(row_news)

            url = f"{URL}/uz/post/latest-ajax"
            params = {
                'id': 'latest',
                'limit': load_articles,
                'offset': offset
            }

            offset += load_articles
            response = request_page(url, params=params)
            page_soup = BeautifulSoup(response.content, "html.parser")
            news_items = page_soup.find_all("div", class_="col-lg-4 col-md-6")
            print(len(news_items))

    print(f"Data has been written to {csv_file}")

def request_page(link, params=None):
    try:
        extended_page = requests.get(link, params=params)
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

# Run the function
scrap_qalampir()
