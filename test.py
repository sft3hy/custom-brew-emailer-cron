import requests
from config import NEWS_API_KEY
import json
import os

categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]

# Ensure directory exists
os.makedirs("category-sources", exist_ok=True)

for category in categories:
    url = "https://newsapi.org/v2/top-headlines/sources"
    params = {
        "country": "us",
        "category": category,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params).json()  # Parse JSON properly
    with open(f"category-sources/{category}.json", "w") as f:
        json.dump(response, f, indent=4)  # Pretty print with indentation
