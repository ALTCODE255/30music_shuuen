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


def passQuote(quote: str, log: list[str]) -> bool:
    return (
        True
        if quote and quote.strip() and not quote.startswith("#") and quote not in log
        else False
    )


def getQuote() -> str:
    with open("recent.txt", "r", encoding="utf-8") as f:
        log = f.read().splitlines()
        if len(log) < 11:
            log = [""] * (11 - len(log)) + log
    with open("shuuen_music.txt", "r", encoding="utf-8") as f:
        quotes = [quote for quote in f.read().splitlines() if passQuote(quote, log)]
    random_quote = random.choice(quotes)
    log.pop(0)
    log.append(random_quote)
    with open("recent.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(log))
    return random_quote.replace("\\n", "\n")


client.create_tweet(text=getQuote())
