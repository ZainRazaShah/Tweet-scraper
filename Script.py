import tweepy
from tqdm import tqdm
import socket
import pandas as pd
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys

customer_API_key        = "M1CegAV9S0KtW43Bnfvaayoty"
customer_API_secret     = "9gvPvmwJNACX8bSQKegA7syTT8qoKWLY0G2e7y8Q3Z3htbHngQ"
access_token            = "2472447743-5kEl0N82R8DK4y5POVEX7tsovKdOEXLxtVON7T0"
access_token_secret     = "rapbANkPiQqcJ3SItIX02cRfeTEO2K4SC8rr27KTaRePC"

authentication  = tweepy.OAuthHandler(customer_API_key,customer_API_secret)
authentication.set_access_token(access_token,access_token_secret)
api = tweepy.API(authentication)

user_ID = "elonmusk"
tweets = tweepy.Cursor(api.user_timeline, screen_name = user_ID, tweet_mode = 'extended').items()
elon_tweets_dict = []

for t in tqdm(tweets):
    dummy_dict = {}
    dummy_dict['Date'] = t.created_at
    dummy_dict['Favourites'] = t.favorite_count
    dummy_dict['Retweets'] = t.retweet_count
    dummy_dict['Tweet Text'] = t.full_text
    dummy_dict['Screen Name'] = t.user.screen_name
    elon_tweets_dict.append(dummy_dict)


elons_tweets_df = pd.DataFrame.from_dict(elon_tweets_dict)

recipients = ['zain.raza28@yahoo.com'] 
emaillist = [elem.strip().split(',') for elem in recipients]
msg = MIMEMultipart()
msg['Subject'] = f"Twitter Dataset for {user_ID} is here !" 
msg['From'] = 'Zain Raza Shah'

html = """\
<html>
  <head></head>
  <body>
    {0}
  </body>
</html>
""".format(elons_tweets_df.to_html())

part1 = MIMEText(html, 'html')
msg.attach(part1)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('zain.raza.shah.tech@gmail.com', 'Pakarmy123')
server.sendmail(msg['From'], emaillist, msg.as_string())
server.close()