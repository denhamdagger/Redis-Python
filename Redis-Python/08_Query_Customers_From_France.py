import settings
import redis

def ProcessCustomer(key):
	# Get all keys and values from hash
	_cust = r.hmget("customer:" + key.decode('utf-8'), "ID", "Company", "Contact", "City", "Country")

	print("{:5s} {:40s} {:25s} {:20s} {:20s}".format(
		_cust[0].decode('utf-8'), 
		_cust[1].decode('utf-8'),
		_cust[2].decode('utf-8'),
		_cust[3].decode('utf-8'),
		_cust[4].decode('utf-8')
		))

if __name__ == "__main__":
	print("Querying Customers...")

	# Connect to Redis
	r = redis.Redis(host=settings.redisSettings["host"], port=settings.redisSettings["port"], password=settings.redisSettings["password"], db=settings.redisSettings["database"])

	# Get all the Customer Keys. This does a SCAN under the covers
	print("{:5s} {:40s} {:25s} {:20s} {:20s}".format("ID","Company","Contact","City","Country"))
	for key in r.smembers("customer-country:France"):
		ProcessCustomer(key)

	print("Querying Customers Completed")
