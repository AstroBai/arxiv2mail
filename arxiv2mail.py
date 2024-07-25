import feedparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse

def fetch_arxiv_articles():
    url = 'http://export.arxiv.org/rss/astro-ph.CO'
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        article = {
            'title': entry.title,
            'link': entry.link
        }
        articles.append(article)
    return articles

def send_email(articles, recipient_email):
    sender_email = "astrobaijc@gmail.com"
    password = "xgka vivd yfwb ilpx"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Daily arXiv astro-ph.CO Articles"

    body = "Daily arXiv astro-ph.CO Articles\n"
    body += "==============================\n"
    for article in articles:
        body += f"{article['title']}\n"
        body += f"{article['link']}\n"
        body += "------------------------------\n"
    
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    text = msg.as_string()
    server.sendmail(sender_email, recipient_email, text)
    server.quit()

def main(target_email):
    articles = fetch_arxiv_articles()
    send_email(articles, target_email)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send daily arXiv astro-ph.CO articles to a specified email address.")
    parser.add_argument('--target', dest='target_email', required=True, help='The email address of the target recipient.')
    args = parser.parse_args()
    main(args.target_email)
