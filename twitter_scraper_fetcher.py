import requests
from bs4 import BeautifulSoup
from config import TWITTER_URL
import re
 
CONTENT_CLASS_NAME = "dir-ltr"
CONTENT_CONTAINER_TAGS = ["div"]
EMPTY_ITEMS = [None, "", "None", "\n"]
AGENTS= 'Nokia5310XpressMusic_CMCC/2.0 (10.10) Profile/MIDP-2.1 '\
'Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; '\
'Nokia5310XpressMusic) U2/1.0.0 UCBrowser/9.5.0.449 U2/1.0.0 Mobile'
 
 
def get_elements(twitter_handle): # twitter_handle = JackBiggin
  url = TWITTER_URL + twitter_handle   # https://twitter.com/JackBiggin
  response = requests.get(url, headers={'User-Agent': AGENTS})
  html = response.content
 
  soup = BeautifulSoup(html, "html.parser")
 
  return soup.find_all(CONTENT_CONTAINER_TAGS, {"class": CONTENT_CLASS_NAME})
 
def get_user_tweets(twitter_handle):
  elements = get_elements(twitter_handle)
 
  tweets = []
 
  for post in elements:
    for text in post.contents:
      #check if line contains real text
      if text.string not in EMPTY_ITEMS:
        tweets.append(text.string)
 
  return tweets
 
def clean_tweets_data(tweets):
  emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        flags=re.UNICODE,
    )
 
  url_pattern = re.compile(r"http\S+", re.DOTALL)
  mentions_pattern = re.compile(r"@\S+", re.DOTALL)
 
  cleaned_tweets = []
  for tweet in tweets:
    text_without_emoji = emoji_pattern.sub(r"", tweet)
    text_without_url = url_pattern.sub(r"", text_without_emoji)
    cleaned_tweets.append(mentions_pattern.sub(r"", text_without_url))
 
  return cleaned_tweets