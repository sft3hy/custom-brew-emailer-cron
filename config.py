import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

sample_news_summary = """
Teacher Marc Fogel back in US after prisoner swap with Russia. The call between Trump and
Putin came after Fogel, an American arrested for flying into Moscow with medically prescribed 
marijuana in 2021, returned to US soil as part of a prisoner exchange. To secure Fogel's freedom,
the Trump administration agreed to release Alexander Vinnik, a Russian citizen and the 
co-founder of Bitcoin exchange BTC-e, which US authorities say was used by criminals 
for ransomware schemes, identity theft, and drug trafficking. Vinnik, who pleaded guilty
to conspiracy to commit money laundering, will leave $100 million worth of digital assets 
in the US as part of the deal, per NBC.
"""

news_summarizer_system_prompt = f"""
You are a news summarization system that generates concise, well-structured summaries of news articles.

Requirements:
Extract and summarize the key points of the article while maintaining clarity and accuracy.
Provide a descriptive title for the summary.
Ensure the summary is coherent, engaging, and easy to read, and stay on topic with no extra unrelated details.
Output 3 plain text paragraphs that summarize the article.

Example Output:
{sample_news_summary}
"""

formatter_system_prompt = """
You are an HTML formatter for email content. You will receive raw text output from an LLM and convert it into well-structured, visually appealing HTML for email display.  

### Requirements:
- **Do not modify the text content**—only enhance its formatting.
- **Use clean, inline-compatible HTML and CSS**, ensuring proper rendering in email clients.
- **Apply custom styling** for headers, bold text, and layout:
  - Convert `**bold text**` to `<strong>bold text</strong>`.
  - Use semantic HTML elements for structure.
  - Ensure responsive design for mobile compatibility.
  - If you encounter multiple articles that cover the same event, only include the first article's content.
  - Keep the lines that look like '<a href="{article["url"]}" target="_blank">{article["title"]}</a><br><br><br>' to maintain the correct links to the articles
- **Output only valid HTML and CSS**, with NO EXPLANATION AT THE BEGINNING OR END.

### Example Output:
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Title</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        .container {
            max-width: 600px;
            background: #ffffff;
            padding: 5px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
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
            color: #333;
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
        <div class="header">{Topic} Custom Brew ☕️</div>
        <div class="content">
            <h2>News article 1 title</h2>
            <p>Example news article 1 summary</p>
            <hr>
            <h2>News article 2 title</h2>
            <p>Example news article 2 summary</p>
            <hr>
            <h2>News article 3 title</h2>
            <p>Example news article 3 summary</p>
        </div>
        <div class="footer">
            LLM generated summaries - please verify facts.
        </div>
    </div>
</body>
</html>
"""


EMAIL_SEND_TIME="14:26"
SUMMARY_COUNT=3
SUMMARIZER_MODEL="gemma2-9b-it"
FORMATTER_MODEL="llama-3.3-70b-versatile"
TIME_BETWEEN_JOB_CHECK=10