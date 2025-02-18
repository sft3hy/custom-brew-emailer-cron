from groq import Groq
import newspaper
import os
from config import news_summarizer_system_prompt, SUMMARIZER_MODEL, FORMATTER_MODEL, formatter_system_prompt

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def extract_news_text(url):
    try:
        print(f"scraping {url}")
        article = newspaper.article(url)
        with open("scraped_news.txt", "w") as file:
            file.write(article.text)
        return article.text
    except Exception as e:
        return f"Error extracting article: {e}"


def generate_summary(article_url: str) -> str:
    article = extract_news_text(article_url)
    print(f"generating summary for {article_url}")
    print()
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": news_summarizer_system_prompt,
        },
        {
            "role": "user",
            "content": f"summarize this article in an engaging tone: {article}",
        }
    ],
    model=SUMMARIZER_MODEL,
    )
    response = chat_completion.choices[0].message.content
    return response

def format_summaries(llm_output: str) -> str:
    print("Formatting summaries into beautiful html for viewing pleasure")
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": formatter_system_prompt,
        },
        {
            "role": "user",
            "content": f"here is your input text: {llm_output}",
        }
    ],
    model=FORMATTER_MODEL,
    )
    response = chat_completion.choices[0].message.content
    return response