import tweepy
import json
import random

with open("creds.json", "r") as credentials:
    keys = json.load(credentials)

client = tweepy.Client(
    consumer_key=keys["consumer_key"],
    consumer_secret=keys["consumer_secret"],
    access_token=keys["access_token"],
    access_token_secret=keys["access_token_secret"],
)


def getQuote() -> str:
    with open("shuuen_recent.txt", "r", encoding="utf-8") as f:
        log = f.read().splitlines()
        if len(log) < 11:
            log = [""] * (11 - len(log)) + log
    with open("shuuen.txt", "r", encoding="utf-8") as f:
        quotes = [quote for quote in f.read().splitlines() if quote not in log and quote and quote.strip()]
    random_quote = random.choice(quotes)
    log.pop(0)
    log.append(random_quote)
    with open("shuuen_recent.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(log))
    return random_quote


client.create_tweet(text=getQuote())
