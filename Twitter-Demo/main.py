import twitter
import redis
import settings
import json
import sys

# Redis Time to Live = 30 Seconds
REDISTTL    = 30
TWEET_COUNT = 20

t = twitter.Twitter(auth = twitter.OAuth(settings.twitterSettings["token"], settings.twitterSettings["token_secret"], settings.twitterSettings["consumer_key"], settings.twitterSettings["consumer_secret"]))
r = redis.Redis(host=settings.redisSettings["host"], port=settings.redisSettings["port"], password=settings.redisSettings["password"], db=settings.redisSettings["database"])

def CheckRedisCache(query):
	_res = r.get(query)

	if (_res is None):
		return None

	print("***** Getting Data From Redis Cache *****")
	# Deserialize the JSON back into a Python list
	return json.loads(_res.decode('utf-8'))


def FetchFromTwitter(query):
	print("***** Getting Data From Twitter *****")
	_results = t.search.tweets(q = query, count = TWEET_COUNT)

	_redisValue = {}
	_redisValue = _results["statuses"]

	# Store the Python list as JSON in Redis with expiry
	r.setex(query, json.dumps(_redisValue), REDISTTL)
	return _results["statuses"]


if __name__ == "__main__":
	if (len(sys.argv) < 2):
		print("Usage: main.py <search string>")
		sys.exit()

	_search = sys.argv[1]

	print("Searching Twitter for", _search, "...")

	_results = CheckRedisCache(_search)

	if (_results is None):
		_results = FetchFromTwitter(_search)

	for _res in _results:
		print("{:19s} - @{:20s} - {:140s}".format(_res["created_at"][0:19], _res["user"]["screen_name"][0:20], _res["text"].replace("\n"," ")))

