import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

sample_news_summary = """
Teacher Marc Fogel is back in the US after prisoner swap with Russia. The call between Trump and
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
Ensure the summary is coherent, engaging, and easy to read, and stay on topic with no extra unrelated details.
Output 1-3 short plain text paragraphs that summarize the article, and split the paragraphs with two newlines (\n\n).
Keep the paragraphs relatively short (no more than 4 sentences) to maintain an engaging tone.
Do NOT include a header or title for the summary, OMIT any uses of '##'

Example Output:
{sample_news_summary}
"""


SUMMARY_COUNT=7
SUMMARIZER_MODEL="gemma2-9b-it"
TIME_BETWEEN_JOB_CHECK=10