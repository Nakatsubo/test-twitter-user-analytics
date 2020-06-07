# coding:utf-8
import tweepy
import pandas as pd
import time
import os

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Pandas
columns = ["screen_name", "description", "follower", "following"]
df = pd.DataFrame(columns=columns)

# target_user
target_screen_name = "SolvIT_Africa"

# followers
followers_ids = tweepy.Cursor(api.followers_ids, id = target_screen_name, cursor = -1).items()
followers_ids_list = []
try:
  for followers_id in followers_ids:
      followers_ids_list.append(followers_id)
except tweepy.error.TweepError as e:
  print (e.reason)

# save dataframe
for follower_id in followers_ids_list:
 try:
    user = api.get_user(follower_id)
    screen_name = user.screen_name
    description = user.description
    follower = user.followers_count
    following = user.friends_count
    se = pd.Series([screen_name, description, follower, following], columns)
    df = df.append(se, ignore_index=True)
    print(df)
 except Exception as e:
    print(e)
    time.sleep(60*15)

# export CSV
filename = "result.csv"
df.to_csv(filename, encoding = 'utf-8-sig')
