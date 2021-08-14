import io
import os
import time
import tweepy
import pandas as pd
import requests
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys

#----------------------------------------------------------------------------------------

def input_file():
  info_list = []
  f = open("information.txt", "r")
  info = f.readlines()
  for line in info:
    info_list.append(line) 
  return info_list

#----------------------------------------------------------------------------------------

def twitter_extraction(twitter_id):
  try:
    tweets_dict = []
    customer_API_key        = os.environ.get("CUSTOMER_API_KEY")
    customer_API_secret     = os.environ.get("CUSTOMER_API_SECRET")
    access_token            = os.environ.get("ACCESS_TOKEN")
    access_token_secret     = os.environ.get("ACCESS_TOKEN_SECRET")

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

  except tweepy.TweepError:

    return False

#----------------------------------------------------------------------------------------

def csv_file(df):
  with io.StringIO() as buffer:
    df.to_csv(buffer)
    return buffer.getvalue()

#----------------------------------------------------------------------------------------

def excel_file(df):
  with io.BytesIO() as buffer:
    writer = pd.ExcelWriter(buffer)
    df.to_excel(writer)
    writer.save()
    return buffer.getvalue()

#----------------------------------------------------------------------------------------

EMAIL_ID = os.environ.get("EMAIL_ID")
PASSWORD_SCRIPT = os.environ.get("PASSWORD_SCRIPT")

def email (df, twitter_id, receiver_email, body):
  if isinstance(df, pd.DataFrame):
    recipient = receiver_email
    msg = MIMEMultipart()
    msg['Subject'] = f"Twitter data for {twitter_id} is here !" 
    msg['From'] = "Tweet Scraper"
    msg['To'] = receiver_email
    
    filename_dict = { 'dataset.csv': csv_file, 'dataset.xlsx': excel_file}

    intro_line = """\
    <html>
      <head>
      <p style="font-size:20px">
      Hey there, 
      </p>
      <p style="font-size:20px">
      {0}
      </p>
      </head>
    </html>
    """.format(body)

    title = MIMEText(intro_line, 'html')
    msg.attach(title)

    for filename in filename_dict:    
      attachment = MIMEApplication(filename_dict[filename](df))
      attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
      msg.attach(attachment)

  elif df == False:

    recipient = receiver_email
    msg = MIMEMultipart()
    msg['Subject'] = "Incorrect Twitter ID !" 
    msg['From'] = "Tweet Scraper"
    msg['To'] = receiver_email

    intro_line = """\
    <html>
      <head>
      <p style="font-size:20px">
      The twiiter handle that you used is incorrect.
      </p>
      </head>
    </html>
    """

    title = MIMEText(intro_line, 'html')
    msg.attach(title)
  

  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(EMAIL_ID, PASSWORD_SCRIPT)
  server.sendmail(msg['From'], recipient, msg.as_string())
  server.close()

#----------------------------------------------------------------------------------------

def main():
  info_list = input_file()
  twitter_handle = info_list[0]
  recepient_email = info_list[1]
  trigger_time = info_list[2]
  tweets_df = twitter_extraction(twitter_handle)
  
  body = f"Your favourite Twitter bot has scraped all this data just for you.\
           These datasets comprise of {len(tweets_df)} record(s) each.\
           Use them wisely \N{slightly smiling face}"

  email(tweets_df, twitter_handle, recepient_email, body)

  return trigger_time

#----------------------------------------------------------------------------------------

'''
Let us now call the main() function in a loop
'''
flag = True

while flag:
  trigger_time = main()
  print(trigger_time)
  time.sleep(int(trigger_time)*60)

