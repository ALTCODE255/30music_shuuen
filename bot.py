import os
import random
import sys
import pickle
import re

from dotenv import load_dotenv
import tweepy

os.chdir(sys.path[0])
load_dotenv()

client = tweepy.Client(
    consumer_key=os.getenv("CONSUMER_KEY"),
    consumer_secret=os.getenv("CONSUMER_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
)


def getTweets(log: list[str]) -> list[str]:
    with open("music.txt", "r", encoding="utf-8") as f:
        all_tweets = re.sub(r"^\s|^[#;].*\n", "", f.read()).strip("\n")
    return [tweet for tweet in all_tweets.splitlines() if tweet not in log]


def getTweet() -> str:
    limit = int(os.getenv("STORAGE_THRESHOLD"))
    try:
        with open("recent.pkl", "rb") as f:
            log = pickle.load(f)
    except FileNotFoundError:
        log = [None]*limit
    random_tweet = random.choice(getTweets())
    log.pop(0)
    log.append(random_tweet)
    with open("recent.pkl", "wb") as f:
        pickle.dump(log, f)
    return random_tweet.replace("\\n", "\n")


if __name__ == "__main__":
    tweet = client.create_tweet(text=getTweet())
