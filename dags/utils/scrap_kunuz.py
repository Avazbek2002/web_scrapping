import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta


def scrap_kunuz():
    URL = "https://kun.uz"
    news_list_URL = "https://kun.uz/news/list"
    scrapped_data = []

    
    try:
        page = requests.get(news_list_URL)
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

    soup = BeautifulSoup(page.content, "html.parser")

    news_items = soup.find_all("div", class_="small-cards__default-link")

    stop_crawling = False
    yesterday = datetime.now() - timedelta(days=1)

    yesterday = yesterday.strftime("%d.%m.%Y")

    log_file = open("KunUzLogs.txt", "w")

    log_file.write("MAIN PAGE link: " + news_list_URL + "\n")


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

            # fetch the article from the website
            try:
                item_page = requests.get(URL + itam_page_link)
                # Check if the request was successful
                if item_page.status_code == 200:
                    print("Item page fetched successfully!")
                else:
                    print(f"Failed to fetch the item page. Status code: {item_page.status_code}")
                    continue

            except requests.exceptions.ConnectionError as e:
                print(f"Connection error occurred: {e}")
            except requests.exceptions.Timeout as e:
                print(f"Request timed out: {e}")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")

            log_file.write(URL + itam_page_link + "\n")

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

        
        extend_page_link = soup.find(id="lpagination")
        extend_page_link = extend_page_link.get("href")

        try:
            extended_page = requests.get(URL + extend_page_link)
            # Check if the request was successful
            if extended_page.status_code == 200:
                print("Item page fetched successfully!")
            else:
                print(f"Failed to fetch the item page. Status code: {extended_page.status_code}")
                continue

        except requests.exceptions.ConnectionError as e:
            print(f"Connection error occurred: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Request timed out: {e}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        log_file.write("\n" + 20 * "-" + "\n" + "MAIN PAGE LINK: " + URL + extend_page_link + "\n")

        soup = BeautifulSoup(extended_page.content, "html.parser")
        news_items = soup.find_all("div", class_="small-cards__default-link")
    
    log_file.close()
    
    return scrapped_data

scrap_kunuz()