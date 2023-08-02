from app.config import database
from bs4 import BeautifulSoup
import requests


def scrape_news(database=database):
    database.drop_collection("news")
    print("job started")
    url = "https://astanatimes.com/"

    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")

        recent_news_div = soup.find("div", class_="five columns recent")

        news_a_tags = recent_news_div.findAll("a", title=True)[:10]
        news_urls = []

        for news_a_tag in news_a_tags:
            news_url = news_a_tag.get("href")
            news_urls.append(news_url)

        for news_url in news_urls:
            news_page = requests.get(news_url)
            news_page_soup = BeautifulSoup(news_page.text, "html.parser")
            eight_columns_div = news_page_soup.find("div", class_="eight columns")
            post_div = eight_columns_div.find("div", class_="post")

            text_paragraphs = post_div.findAll("p")

            text_list = []
            for p_tag in text_paragraphs:
                text_list.append(p_tag.get_text())

            title_tag = news_page_soup.find("h1")
            title = title_tag.get_text()

            author_tag = news_page_soup.find("p", class_="byline")

            date_string = author_tag.contents[-1].strip()
            author = author_tag.findAll("a")[0].get_text()

            img_tag = news_page_soup.findAll("img")[2]
            img_url = img_tag.get("src")

            news_data = {
                "url": news_url,
                "title": title,
                "author": author,
                "published_date": date_string,
                "text_list": text_list,
                "image_url": img_url,
            }
            database.news.insert_one(news_data)
