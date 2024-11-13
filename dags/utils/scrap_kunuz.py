import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta


def scrap_kunuz():
    URL = "https://kun.uz"
    news_list_URL = "https://kun.uz/news/list"
    scrapped_data = []
    page = requests.get(news_list_URL)

    soup = BeautifulSoup(page.content, "html.parser")

    news_items = soup.find_all("div", class_="small-cards__default-link")

    stop_crawling = False
    yesterday = datetime.now() - timedelta(days=1)

    yesterday = yesterday.strftime("%d.%m.%Y")

    while not stop_crawling:
        for item in news_items:
            page_stats_string = item.find("p").get_text()
            page_stats = [part.strip() for part in re.split('[|/]', page_stats_string)]
            if len(page_stats) < 3:
                continue

            elif len(page_stats) == 3:
                if page_stats[2] != yesterday:
                    stop_crawling = True
                    break

            itam_page_link = item.find("a", class_="small-cards__default-text").get("href")


            item_page = requests.get(URL + itam_page_link)
            page_content = BeautifulSoup(item_page.content, "html.parser")

            page_stats_string = page_content.find("div", class_="news-inner__content-stats").find("span").get_text()

            page_stats = [part.strip() for part in re.split('[|/]', page_stats_string)]

            page_category = page_stats[0]

            page_title = page_content.find("h1", class_="news-inner__content-title").get_text()

            page_description_element = page_content.find("p", class_="news-inner__content-desc")
            page_description = ""
            if page_description_element:
                page_description = page_description_element.get_text()

            page_text = page_content.find("div", class_="news-inner__content-page")
            page_paragraphs = page_text.find_all("p")

            page_pure_text = ""

            for paragraph in page_paragraphs:
                # Find all links in the paragraph
                links = paragraph.find_all('a')
                for link in links:
                    # Replace the link tag with just its text content
                    link.replace_with(link.get_text())
                
                page_pure_text = page_pure_text + paragraph.get_text()
            
            page_pure_text = page_pure_text.replace('\n', '').replace('\xa0', '')

            row_news = {
                'Category': page_category,
                'Title': page_title,
                'Description': page_description,
                'Full Text': page_pure_text
            }

            scrapped_data.append(row_news)

            # Optional: Print confirmation for each item processed
            print(f"Saved article: {page_title}")
        
        extend_page_link = soup.find(id="lpagination")
        print("result of extended page: " + str(extend_page_link))
        extend_page_link = extend_page_link.get("href")
        extended_page = requests.get(URL + extend_page_link)

        soup = BeautifulSoup(extended_page.content, "html.parser")
        news_items = soup.find_all("div", class_="small-cards__default-link")
    
    return scrapped_data
