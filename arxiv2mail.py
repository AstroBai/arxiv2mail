import feedparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse
import datetime

def fetch_arxiv_articles():
    url = 'http://export.arxiv.org/rss/astro-ph.CO'
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        article = {
            'title': entry.title,
            #'summary': entry.summary, # uncomment this line when you need to see the abstract.
            'link': entry.link,
            'id': entry.id
        }
        articles.append(article)
    return articles

def send_email(articles, recipient_email):
    sender_email = "astrobaijc@gmail.com" # use your own email here
    password = "xgka vivd yfwb ilpx" # app password, not your account's password
    
    today = datetime.date.today()
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "astro-ph.CO " + str(today)
    
    body = "Dear subscriber: \n\n"
    body += "Today's arXiv has been updated.\n\n\n"
    body += "==============================\n"
    body += "Daily arXiv astro-ph.CO Articles\n"
    body += "==============================\n"
    replace = True
    for i, article in enumerate(articles):
        if int(article['id'][-1])>1 and replace:
            body += "\n\n\n"
            body += "==============================\n"
            body += "The following are the articles replaced today\n"
            body += "==============================\n"
            replace = False
        body += f"{str(i+1)}. Title: {article['title']}\n"
        body += f"Link: {article['link']}\n"
        body += "------------------------------\n"
    body += "\n\n\n"
    body += "Thanks for subscribing,\n\n"
    body += "Jiachen"
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
