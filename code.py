import tweepy
import urllib3
import time
import pandas as pd
import requests
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys

tweets_dict = []

#----------------------------------------------------------------------------------------
def input_file():
  info_list = []
  f = open("zain.txt", "r")
  info = f.readlines()
  for line in info:
    info_list.append(line) 
  return info_list

#----------------------------------------------------------------------------------------

def twitter_extraction(twitter_id):
  customer_API_key        = "M1CegAV9S0KtW43Bnfvaayoty"
  customer_API_secret     = "9gvPvmwJNACX8bSQKegA7syTT8qoKWLY0G2e7y8Q3Z3htbHngQ"
  access_token            = "2472447743-5kEl0N82R8DK4y5POVEX7tsovKdOEXLxtVON7T0"
  access_token_secret     = "rapbANkPiQqcJ3SItIX02cRfeTEO2K4SC8rr27KTaRePC"

  authentication  = tweepy.OAuthHandler(customer_API_key,customer_API_secret)
  authentication.set_access_token(access_token,access_token_secret)
  api = tweepy.API(authentication)

  user_ID = twitter_id
  tweets = api.user_timeline(screen_name = user_ID, tweet_mode = 'extended', count = 100)

  for t in tweets:
    dummy_dict = {}
    dummy_dict['Date'] = t.created_at
    dummy_dict['Favourites'] = t.favorite_count
    dummy_dict['Retweets'] = t.retweet_count
    dummy_dict['Tweet Text'] = t.full_text
    dummy_dict['Screen Name'] = t.user.screen_name
    tweets_dict.append(dummy_dict)

  tweets_df = pd.DataFrame.from_dict(tweets_dict)
  return tweets_df

#----------------------------------------------------------------------------------------

def email (df, twitter_id, tweets_dict, receiver_email):
  recipient = receiver_email
  msg = MIMEMultipart()
  msg['Subject'] = f"Twitter Dataset for {twitter_id} is here !" 
  msg['From'] = "Tweet Scraper"
  
  heading = f"This dataset comprises of {len(tweets_dict)} records !"
  html = """\
  <html>
    <head>
    <h2 style="font-size:20px">
    {0}
    </h2>
    <br />
    </head>
    <body>
      {1}
    </body>
  </html>
  """.format(heading ,df.to_html())

  part1 = MIMEText(html, 'html')
  msg.attach(part1)
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login('zain.raza.shah.tech@gmail.com', 'Pakarmy123')
  server.sendmail(msg['From'], recipient, msg.as_string())
  server.close()

#----------------------------------------------------------------------------------------

def main():
  info_list = input_file()
  twitter_handle = info_list[0]
  recepient_email = info_list[1]
  trigger_time = info_list[2]

  tweets_df = twitter_extraction(twitter_handle)

  email(tweets_df, twitter_handle, tweets_dict, recepient_email)

#----------------------------------------------------------------------------------------

'''
Let us now call the main() function
'''
main()
