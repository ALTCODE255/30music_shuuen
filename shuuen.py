import tweepy
import json
import os
import random

directory = os.path.realpath(os.path.dirname(__file__))

with open(directory + "/creds.json", "r") as credentials:
	keys = json.load(credentials)

client = tweepy.Client(consumer_key=keys["consumer_key"], consumer_secret=keys["consumer_secret"], access_token=keys["access_token"], access_token_secret=keys["access_token_secret"])

def getQuote():
	with open(directory + "/shuuen.txt", "r", encoding="utf-8") as f:
		quotes = f.read().splitlines()
	with open(directory + "/shuuen_recent.txt", "r", encoding="utf-8") as f:
		log = f.read().splitlines()
	filtered_quotes = [quote for quote in quotes if quote not in log]
	random_quote = random.choice(filtered_quotes)
	log.pop(0)
	log.append(random_quote)
	with open(directory + "/shuuen_recent.txt", "w", encoding="utf-8") as f:
		f.write('\n'.join(log))
	return random_quote

client.create_tweet(text=getQuote())
