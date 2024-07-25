import feedparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def fetch_arxiv_articles():
    url = 'http://export.arxiv.org/rss/astro-ph.CO'
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        article = {
            'title': entry.title,
            'authors': entry.author,
            'summary': entry.summary,
            'link': entry.link
        }
        articles.append(article)
    return articles

def format_articles_for_github(articles):
    formatted = "# Daily arXiv astro-ph.CO Articles\n\n"
    for article in articles:
        formatted += f"## {article['title']}\n"
        formatted += f"**Authors:** {article['authors']}\n\n"
        formatted += f"**Summary:** {article['summary']}\n\n"
        formatted += f"[Read more]({article['link']})\n\n"
    return formatted

def send_email(articles, recipient_email):
    sender_email = "astrobaijc@gmail.com"
    password = "xgka vivd yfwb ilpx"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Daily arXiv astro-ph.CO Articles"

    body = ""
    for article in articles:
        body += f"Title: {article['title']}\n"
        body += f"Authors: {article['authors']}\n"
        body += f"Summary: {article['summary']}\n"
        body += f"Link: {article['link']}\n\n"
    
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    text = msg.as_string()
    server.sendmail(sender_email, recipient_email, text)
    server.quit()

def main():
    articles = fetch_arxiv_articles()
    formatted_articles = format_articles_for_github(articles)

    with open('index.md', 'w') as file:
        file.write(formatted_articles)

    send_email(articles, "astrobaijc@gmail.com")

if __name__ == "__main__":
    main()

