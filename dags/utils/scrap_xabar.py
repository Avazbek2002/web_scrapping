import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def scrap_xabar():
    URL="https://xabar.uz"
    news_url_list="https://xabar.uz/uz/yangiliklar?load=60"
    scrapped_data = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/70.0.3538.77 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://google.com",
    }

    page = requests.get(news_url_list, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    news_items = soup.find_all("div", class_="media-info")[:60]

    stop_crawling = False
    day_before_yesterday = datetime.now() - timedelta(days=2)
    formatted_day_before_yesterday = day_before_yesterday.strftime("%d/%m")

    while not stop_crawling:
        for news in news_items:
            news_date = news.find("span", class_="date-time").get_text().split(",")
            
            if (len(news_date) == 1) or (news_date[0] == "bugun"):
                continue

            elif news_date[0] == formatted_day_before_yesterday:
                stop_crawling = True
                break
            
            page_url = news.find("p", class_="news__item-title").find("a").get("href")

            page = requests.get(page_url, headers=headers)

            article_soup = BeautifulSoup(page.content, "html.parser")
            
            article_category = article_soup.find("div", class_="article__category").find("a").get_text()

            article_title = article_soup.find("h2", class_="post__title").get_text()
            
            article_paras = article_soup.find_all("div", class_="post__body")

            article_description = news.find("p", class_="news__item-title").get_text().replace('\n', '')

            page_pure_text = ""

            for paragraph in article_paras:
                # Find all links in the paragraph

                links = paragraph.find_all('a')
                for link in links:
                    # Replace the link tag with just its text content
                    link.replace_with(link.get_text())
                
                page_pure_text = page_pure_text + paragraph.get_text()
            
            page_pure_text = page_pure_text.replace('\n', '').replace('\xa0', '')
            
            scrapped_data.append({
                'Category': article_category,
                'Title': article_title,
                'Description': article_description,
                'Full Text': page_pure_text
            })

                
    return scrapped_data
