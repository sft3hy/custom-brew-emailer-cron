from utils.email_utils import send_email
from utils.groq_utils import generate_summary, input_html_news, curate_news
from utils.news_utils import get_news
from utils.gsheet_utils import get_all_user_data
from datetime import datetime

TEST_WITH_MYSELF = False

dummy = [{'source': {'id': 'the-washington-post', 'name': 'The Washington Post'}, 'author': 'Dan Diamond', 'title': 'Trump takes a victory lap at a rain-splattered Daytona 500 - The Washington Post', 'description': 'NASCAR is Trump country, White House officials have said, and attendees on Sunday warmly welcomed the president in a brief visit.', 'url': 'https://www.washingtonpost.com/politics/2025/02/16/trump-nascar-daytona-500/', 'urlToImage': 'https://www.washingtonpost.com/wp-apps/imrs.php?src=https://arc-anglerfish-washpost-prod-washpost.s3.amazonaws.com/public/LMUQNTPDZTKJXD6ZGGXIBXGEWY_size-normalized.jpg&w=1440', 'publishedAt': '2025-02-17T00:31:17Z', 'content': 'DAYTONA INTERNATIONAL SPEEDWAY The crowd cheered, the cars roared, and President Donald Trump again basked in the pomp and pageantry of one of Americas premier sporting events.\r\nLast weekend, he was … [+6103 chars]'}, {'source': {'id': 'espn', 'name': 'ESPN'}, 'author': 'Dave McMenamin', 'title': 'LeBron out for All-Star Game, ending 20-year run - ESPN', 'description': 'Lakers star LeBron James will not play in the NBA All-Star Game on Sunday night because of lingering discomfort in his left foot and ankle.', 'url': 'https://www.espn.com/nba/story/_/id/43879532/lakers-lebron-james-nba-all-star-game-foot-ankle-discomfort', 'urlToImage': 'https://a3.espncdn.com/combiner/i?img=%2Fphoto%2F2025%2F0217%2Fr1452836_1296x729_16%2D9.jpg', 'publishedAt': '2025-02-17T00:04:00Z', 'content': 'SAN FRANCISCO -- LeBron James will not play in the NBA All-Star Game, the Los Angeles Lakers forward said before the game Sunday, because of lingering discomfort in his left foot and ankle.\r\nJames, 4… [+852 chars]'}, {'source': {'id': None, 'name': 'pgatour.com'}, 'author': 'Alistair Cameron and GolfWRX', 'title': 'Winners bag: Ludvig Åberg wins with new driver, golf ball at The Genesis Invitational - PGA TOUR', 'description': 'Ludvig Åberg captured his second win on the PGA TOUR with an emphatic back-nine 32 at The Genesis Invitational to come from behind at Torrey Pines’ South Course', 'url': 'https://www.pgatour.com/article/news/winners-bag/2025/02/16/winners-bag-ludvig-aberg-wins-for-first-time-with-new-driver-golf-ball-at-the-genesis-invitational', 'urlToImage': 'https://res.cloudinary.com/pgatour-prod/w_1200,h_628,c_fill,f_auto,q_auto/pgatour/news/editorial/2025/02/16/Aberg_WITB.jpg', 'publishedAt': '2025-02-16T23:26:27Z', 'content': 'Written by Alistair Cameron and GolfWRXGolfWRX.com\r\nLudvig Åberg captured his second win on the PGA TOUR with an emphatic back-nine 32 at The Genesis Invitational to come from behind at Torrey Pines … [+2191 chars]'}, {'source': {'id': None, 'name': 'CBS Sports'}, 'author': '', 'title': "2025 Genesis Invitational purse, prize money: Payouts, Ludvig Åberg's winner's share from $20 million pool - CBS Sports", 'description': "One of the largest winner's check of the entire season is up for grabs this week on the PGA Tour", 'url': 'https://www.cbssports.com/golf/news/2025-genesis-invitational-purse-prize-money-payouts-ludvig-abergs-winners-share-from-20-million-pool/', 'urlToImage': 'https://sportshub.cbsistatic.com/i/r/2025/02/15/6747c53d-5424-49d6-b057-6c984f3ccee6/thumbnail/1200x675/3eafa0b8ef88967e9d7d210ccfd90153/genesis-invitational-trophy-2024-g.jpg', 'publishedAt': '2025-02-16T23:11:00Z', 'content': "The field may have been small at the 2025 Genesis Invitational, but the top prize was as big as ever. The largest winner's check of the PGA Tour's young season will be written to Ludvig Åberg, who sc… [+2423 chars]"}, {'source': {'id': None, 'name': 'New York Post'}, 'author': 'Zach Braziller', 'title': 'No. 9 St. John’s in Big East driver’s seat after defense keys narrow win over No. 24 Creighton - New York Post ', 'description': 'This was the dream when the Red Storm hired Rick Pitino.', 'url': 'https://nypost.com/2025/02/16/sports/no-9-st-johns-in-big-east-drivers-seat-after-defense-keys-win-over-no-24-creighton/', 'urlToImage': 'https://nypost.com/wp-content/uploads/sites/2/2025/02/newspress-collage-0ooqhw9ry-1739745315301.jpg?quality=75&strip=all&1739727366&w=1024', 'publishedAt': '2025-02-16T22:46:00Z', 'content': 'A sold-out Madison Square Garden crowd on its feet. \r\nLets Go Johnnies, chants bouncing off the building’s walls. \r\nA gritty victory that will go a long way toward St. Johns winning its first Big Eas… [+1911 chars]'}]

# Function to test sending emails
def send_email_tester(email, topic):
    print(f"Generating email for {email} about {topic}")
    a_bunch_of_news = get_news(topic=topic)
    curated_articles = curate_news(a_bunch_of_news, topic)
    # news_info = dummy
    articles = []
    for article in curated_articles:
        article_info = {}
        article_info['summary'] = f"""{generate_summary(article['url']).replace('**', '')} <br><br> <a href='{article["url"]}' target="_blank">{article["title"]}</a><br>"""
        article_info['title'] = article['title']
        articles.append(article_info)
    formatted_email = input_html_news(news_summaries=articles, topic=topic)
    with open("current_output.html", "w") as file:
        file.write(str(formatted_email))
    send_email(subject="Custom Brew", body=f"<!DOCTYPE html><html><body>{formatted_email}</body></html>", email_recipient=email, topic=topic)


all_info = get_all_user_data()
topics = list(set([user['Topic'] for user in all_info]))
finalized_emails = {}

# sample data to save newsapi calls during testing
business = [{'source': {'id': 'cnn', 'name': 'CNN'}, 'author': None, 'title': 'US Postal Service head DeJoy to step down after 5 years marked by pandemic, losses and cost cuts - CNN', 'description': 'Louis DeJoy, the head of the US Postal Service, intends to step down, the federal agency said Tuesday, after a nearly five-year tenure marked by the coronavirus pandemic, surges in mail-in election ballots and efforts to stem losses through cost and service c…', 'url': 'https://www.cnn.com/2025/02/18/politics/louis-dejoy-usps-postmaster-general-steps-down/index.html', 'urlToImage': 'https://media.cnn.com/api/v1/images/stellar/prod/sipausa-58205197.jpg?c=16x9&q=w_800,c_fill', 'publishedAt': '2025-02-19T01:10:00Z', 'content': 'Louis DeJoy, the head of the US Postal Service, intends to step down, the federal agency said Tuesday, after a nearly five-year tenure marked by the coronavirus pandemic, surges in mail-in election b… [+2259 chars]'}, {'source': {'id': 'abc-news', 'name': 'ABC News'}, 'author': 'ABC News', 'title': 'Dramatic video shows moment Delta plane flipped after landing in Toronto - ABC News', 'description': None, 'url': 'https://abcnews.go.com/US/dramatic-video-shows-moment-delta-plane-flipped-after/story?id\\\\u003d118921357', 'urlToImage': None, 'publishedAt': '2025-02-19T01:09:46Z', 'content': None}, {'source': {'id': None, 'name': 'Financial Times'}, 'author': 'Myles McCormick', 'title': 'Donald Trump considers 25% tariff on imported cars - Financial Times', 'description': 'US president threatens to intensify trade war with levies on drugs and semiconductors, too', 'url': 'https://www.ft.com/content/3645b83e-75b8-4eb0-b027-d6ef0fda7b5f', 'urlToImage': 'https://www.ft.com/__origami/service/image/v2/images/raw/https%3A%2F%2Fd1e00ek4ebabms.cloudfront.net%2Fproduction%2F66ecb7a3-0736-4667-8660-7b660064dbe0.jpg?source=next-barrier-page', 'publishedAt': '2025-02-19T00:56:04Z', 'content': 'was $29now $25 per 3 months\r\n10% off your first year. The new FT Digital Edition: todays FT, cover to cover on any device. This subscription does not include access to ft.com or the FT App.\r\n<ul><li>… [+140 chars]'}]
entertainment = [{'source': {'id': 'cnn', 'name': 'CNN'}, 'author': 'Alli Rosenbloom', 'title': 'Blake Lively and Ryan Reynolds step out for ‘SNL’ 50th anniversary special amid Justin Baldoni legal battle - Yahoo Entertainment', 'description': 'Blake Lively and Ryan Reynolds appeared on Sunday night ahead of the “Saturday Night Live” 50th anniversary special in New York City, marking their first joint red carpet appearance since their legal dispute with Justin Baldoni began.', 'url': 'https://www.cnn.com/2025/02/16/entertainment/blake-lively-ryan-reynolds-snl/index.html', 'urlToImage': 'https://media.cnn.com/api/v1/images/stellar/prod/ap25048032096681.jpg?c=16x9&q=w_800,c_fill', 'publishedAt': '2025-02-17T01:30:00Z', 'content': 'Blake Lively and Ryan Reynolds on Sunday made their first joint red carpet appearance since the start of their legal dispute with Justin Baldoni.\r\nThe couple were seen posing for photos together on t… [+1726 chars]'}, {'source': {'id': None, 'name': 'Hindustan Times'}, 'author': 'AP', 'title': "Paul Simon and Sabrina Carpenter open the 'Saturday Night Live' 50th anniversary celebration - Hindustan Times", 'description': "Paul Simon and Sabrina Carpenter open the 'Saturday Night Live' 50th anniversary celebration", 'url': 'https://www.hindustantimes.com/world-news/us-news/paul-simon-and-sabrina-carpenter-open-the-saturday-night-live-50th-anniversary-celebration-101739754782603.html', 'urlToImage': 'https://www.hindustantimes.com/ht-img/img/2024/12/18/1600x900/World_2_1734523138451_1734523182285.jpg', 'publishedAt': '2025-02-17T01:13:02Z', 'content': "NEW YORK Paul Simon and Sabrina Carpenter opened the 50th anniversary special celebrating Saturday Night Live with a duet of his song Homeward Bound. \r\nPaul Simon and Sabrina Carpenter open the 'Satu… [+4746 chars]"}, {'source': {'id': None, 'name': 'Billboard'}, 'author': 'Keith Caulfield', 'title': 'Kendrick Lamar’s ‘GNX’ Returns to No. 1 on Billboard 200 Chart - Billboard', 'description': "Kendrick Lamar's 'GNX' jumps back to No. 1 on the Billboard 200 after his Super Bowl halftime show, while two more Lamar albums return to the top 10.", 'url': 'http://www.billboard.com/music/chart-beat/kendrick-lamar-gnx-returns-number-one-billboard-200-super-bowl-1235903744/', 'urlToImage': 'https://www.billboard.com/wp-content/uploads/2025/02/00-kendrick-lamar-super-bowl-lix-halftime-show-2025-billboard-1548.jpg?w=1024', 'publishedAt': '2025-02-17T00:00:25Z', 'content': 'Kendrick Lamar’s GNX jumps back to No. 1 on the Billboard 200 albums chart, for a second week atop the list (rising 4-1 on the survey dated Feb. 22), following his Super Bowl halftime show (Feb. 9) a… [+4753 chars]'}]
def orchestrate():
    for topic in topics:
        curated_articles = []
        a_bunch_of_news = get_news(topic=topic)
        headlines = [article['title'] for article in a_bunch_of_news]
        best_headlines = curate_news(headlines, topic)["handpicked_headlines"]
        for article in a_bunch_of_news:
            if article['title'] in best_headlines:
                curated_articles.append(article)
        print(f"Curated articles in orchestrator.py: {curated_articles}")
        # for article in curated_articles:
        # if topic == "Business":
        #     news_info = business
        # elif topic == "Entertainment":
        #     news_info = entertainment
        articles = []
        for article in curated_articles:
            article_info = {}
            article_summary = generate_summary(article['url'])
            if article_summary is None:
                print(f"Could not parse article {article['url']}, skipping")
            else:
                article_summary = article_summary.replace('**', '')
                article_info['summary'] = f"""{article_summary} <a href='{article["url"]}' target="_blank">{article["title"]}</a><br>"""
                article_info['title'] = article['title']
                if 'description' in article.keys() and 'urlToImage' in article.keys():
                    article_info['description'] = article['description']
                    article_info['urlToImage'] = article['urlToImage']
                articles.append(article_info)
        formatted_email = input_html_news(news_summaries=articles, topic=topic)
        finalized_emails[topic] = formatted_email
    for topic in finalized_emails.keys():
        with open(f"finalized_emails/{topic}.html", "w") as f:
            f.write(str(finalized_emails[topic]))

    for user in all_info:
        if user['Frequency'] == 'Daily':
            users_topic = user['Topic']
            users_email = user['Email']
            if TEST_WITH_MYSELF:
                if user['Email'] == "smaueltown@gmail.com":
                    send_email(f"{users_topic} Custom Brew ☕", body=finalized_emails[users_topic], email_recipient=users_email, topic=users_topic)
            else:
                send_email(f"{users_topic} Custom Brew ☕", body=finalized_emails[users_topic], email_recipient=users_email, topic=users_topic)

            

orchestrate()

# send_email_scheduler("smaueltown@gmail.com", "Business")