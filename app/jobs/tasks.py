import newspaper
from newspaper import Article
from app.config import database


def scrape_news(database=database):
    url = "https://astanatimes.com/"

    astana_times_paper = newspaper.build(url, language="en")

    articles = astana_times_paper.articles[:10]

    for article in articles:
        article.download()
        article.parse()

        article_data = {
            "url": article.url,
            "title": article.title,
            "authors": article.authors,
            "publish_date": article.publish_date.strftime("%H:%M %d:%m:%Y"),
            "image": article.image,
            "text": article.text
        }
        database["news"].insert_one(article_data)

