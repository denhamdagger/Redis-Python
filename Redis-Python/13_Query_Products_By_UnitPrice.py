import settings
import redis

# ID,Product,Category,QuantityPerUnit,UnitPrice,UnitsInStock,UnitsOnOrder,ReorderLevel,Discontinued

def ProcessCustomer(key):
	# Get all keys and values from hash
	_cust = r.hmget("product:" + key.decode('utf-8'), "Product", "Category", "UnitPrice")
	print("{:40s} {:25s} {:}".format(
		_cust[0].decode('utf-8'), 
		_cust[1].decode('utf-8'),
		_cust[2].decode('utf-8')
		))

if __name__ == "__main__":
	print("Querying Products...")

	# Connect to Redis
	r = redis.Redis(host=settings.redisSettings["host"], port=settings.redisSettings["port"], password=settings.redisSettings["password"], db=settings.redisSettings["database"])

	_key = "product-all:unitprice"

	# Get all the Customer Keys. This does a SCAN under the covers
	print("{:40s} {:25s} {:25s}".format("Product","Category","UnitPrice"))
	for key in r.zrangebyscore(_key, 15.00, 20.00):
		ProcessCustomer(key)

	print("Querying Products Completed")
