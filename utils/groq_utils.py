from groq import Groq
import groq
import newspaper
import os
import json
from config import news_summarizer_system_prompt, SUMMARIZER_MODEL, CURATOR_MODEL, news_headline_picker_sys_prompt
import time

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

blank_html_string = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        .container {
            width: 100%;
            margin: 0 auto;
            max-width: 600px;
            background: #ffffff;
            padding: 5px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .img-container {
            width: 100%; /* Ensures it doesn't overflow the container */
            max-width: 100%; /* Keeps images responsive */
            text-align: center; /* Centers the image */
            overflow: hidden; /* Prevents overflow issues */
        }
        .img-container img {
            max-width: 100%; /* Ensures image resizes within the container */
            height: auto; /* Maintains aspect ratio */
            border-radius: 8px; /* Optional: rounds corners to match container */
            display: block; /* Removes extra spacing under image */
            margin: 0 auto; /* Centers the image horizontally */
        }
        .header {
            background: #007bff;
            color: #ffffff;
            text-align: center;
            padding: 20px;
            font-size: 24px;
            font-weight: bold;
            border-radius: 8px 8px 0 0;
        }
        .content {
            padding: 20px;
            color: #000;
            line-height: 1.6;
            border: 2px solid #ccc;
            border-radius: 0 0 8px 8px;
        }
        .footer {
            text-align: center;
            font-size: 12px;
            color: #777;
            padding: 20px;
            border-top: 1px solid #ddd;
            margin-top: 20px;
        }
        hr {
            border: none; /* Remove default border */
            border-top: 1px solid #ccc; /* Thin solid grey line */
            margin: 20px 0; /* Add spacing above and below */
        }
        @media screen and (max-width: 600px) {
            .container {
                margin: auto;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        
"""

def input_html_news(news_summaries: list, topic: str):
    html_to_input = f"<title>{topic} Custom Brew ☕️</title>"
    html_to_input += f'<div class="header">{topic} Custom Brew ☕️</div>'
    html_to_input += '<div class="content">'
    for article in news_summaries:
        print(article)
        print()
        html_to_input += f"<h2>{article['title']}</h2>"
        if 'urlToImage' in article.keys() and 'description' in article.keys():
            html_to_input += f"""
                <div class='img-container'>
                    <img src='{article['urlToImage']}' alt="{article['description']}" width='1080' height='700'>
                </div>
            """
        html_to_input += f"<p>{article['summary']}</p><hr>" 
    html_to_input += """</div>
    <div class="footer">
            LLM generated summaries - please verify facts.
        </div>
    </div>
</body>
</html>
"""
    final_output = blank_html_string + html_to_input
    return final_output

    

def extract_news_text(url):
    try:
        print(f"scraping {url}")
        article = newspaper.article(url)
        if article.text is None or article.text == "":
            return None
        return article.text
    except Exception as e:
        return None
    
def message_creator(sys_prompt: str, input_dict: dict):
    messages=[
            {
                "role": "system",
                "content": sys_prompt,
            },
            {
                "role": "user",
                "content": str(input_dict),
            }
        ]
    return messages

def curate_news(headlines: list, topic: str):
    print("Curating headlines")
    try:
        chat_completion = client.chat.completions.create(
        messages=message_creator(sys_prompt=news_headline_picker_sys_prompt,
                                 input_dict={
                                    "headlines": headlines,
                                    "topic": topic,
                                    }
                                ),
        model=CURATOR_MODEL,
        response_format={
            "type": "json_object"
        },
        )
    # see if chat_completion returns an error code
    except groq.InternalServerError as e:
        print(f"Internal Server Error: {e}")
        print("trying again...")
        time.sleep(3)
        chat_completion = client.chat.completions.create(
        messages=message_creator(sys_prompt=news_headline_picker_sys_prompt,
                                 input_dict={
                                    "headlines": headlines,
                                    "topic": topic,
                                    }
                                ),
        model=CURATOR_MODEL,
        response_format={
            "type": "json_object"
        },
        )
    response = json.loads(str(chat_completion.choices[0].message.content))
    print(f"headlines: {str(response)}")

    return response

def generate_summary(article_url: str) -> str:
    article = extract_news_text(article_url)
    if article is None:
        return None
    print(f"generating summary for {article_url}")
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
    response = str(chat_completion.choices[0].message.content)
    if response == "NONE":
        return None
    paragraphs = response.split('\n\n')
    cleaned_html_output = ""
    for p in paragraphs:
        cleaned_html_output += f"<p>{p}</p>"
    return cleaned_html_output