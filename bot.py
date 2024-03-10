import os
import pickle
import random
import re
import sys

import tweepy
from dotenv import load_dotenv


def initClient() -> tweepy.Client:
    return tweepy.Client(
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("CONSUMER_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
    )


def getRandomTweet(log: list[str]) -> str:
    try:
        with open("music.txt", "r", encoding="utf-8") as f:
            all_tweets = re.findall(
                r"^(?!#.*$)\S.*", f.read().strip("\n"), re.MULTILINE)
    except FileNotFoundError:
        sys.exit("Source file not found.")
    valid_tweets = [tweet for tweet in all_tweets if tweet not in log]
    random_tweet = random.choice(valid_tweets).replace("\\n", "\n")
    return random_tweet


def postTweet():
    try:
        with open("recent.pkl", "rb") as f:
            log = pickle.load(f)
    except FileNotFoundError:
        limit = int(os.getenv("STORAGE_THRESHOLD"))
        log = [None]*limit

    tweet = getRandomTweet(log)
    try:
        client.create_tweet(text=tweet)
    except Exception as e:
        print(e)
        return

    log.pop(0)
    log.append(tweet)
    with open("recent.pkl", "wb") as f:
        pickle.dump(log, f)


if __name__ == "__main__":
    os.chdir(sys.path[0])
    if load_dotenv():
        client = initClient()
        postTweet()
