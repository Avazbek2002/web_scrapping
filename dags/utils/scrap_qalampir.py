import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def scrap_qalampir():
    URL="https://qalampir.uz"
    news_url_list="https://qalampir.uz/uz/latest"
    scrapped_data = []

    page = requests.get(news_url_list)

    soup = BeautifulSoup(page.content, "html.parser")

    news_items = soup.find_all("div", class_="col-lg-4 col-md-6")

    stop_crawling = False
    yesterday = datetime.now() - timedelta(days=1)
    formatted_date = yesterday.strftime("%d")

    while not stop_crawling:
        for news in news_items:
            texts = news.find("span", class_="date").get_text().strip().split()
            if len(texts) == 1:
                continue
            elif texts[0] != formatted_date:
                stop_crawling = True
                break

            news_url = news.find("a").get("href")
            
            news_page = requests.get(URL + news_url)

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

            scrapped_data.append(row_news)
        
        url = f"{URL}/uz/post/latest-ajax"
        params = {
            'id': 'latest',
            'limit': 80,
            'offset': 30
        }

        response = requests.get(url, params=params)
        page_soup = BeautifulSoup(response.content, "html.parser")
        news_items = page_soup.find_all("div", class_="col-lg-4 col-md-6")
    
    return scrapped_data