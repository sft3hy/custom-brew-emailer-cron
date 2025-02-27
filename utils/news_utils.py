from config import NEWS_API_KEY, ARTICLE_COUNT
import requests

def get_news(topic: str):
    print("Gathering news articles...")
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": topic,             # Topic to search for
        "country": "us",       # Only fetch articles from the US
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params)
    print("Gathered news articles")

    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        if len(articles) > ARTICLE_COUNT:
            articles = articles[:ARTICLE_COUNT]
        print(f"Articles returned for {topic}: {len(articles)}")
        return [
            {
                "title": article["title"],
                "description": article["description"],
                "url": article["url"],
                "publishedAt": article["publishedAt"],
                "urlToImage": article["urlToImage"]
            }
            for article in articles
        ]
    else:
        return {"error": f"Failed to fetch articles. Status code: {response.status_code}"}


