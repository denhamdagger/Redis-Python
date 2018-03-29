import settings
import redis
import csv
import sys
import os

def ProcessCSVFile(r, csvin):
	with open(csvin, 'rt', encoding='utf-8') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE, )

		# Ignore Row Header
		next(spamreader)

		for row in spamreader:
			ProcessCustomerRow(r, row)

def ProcessCustomerRow(r, row):
	# CSV Header
	# ID,Product,Category,QuantityPerUnit,UnitPrice,UnitsInStock,UnitsOnOrder,ReorderLevel,Discontinued

	_key = "product-all:unitprice"
	_id = row[0]
	_unitPrice = row[4]
	r.zadd(_key, _id, _unitPrice)

if __name__ == "__main__":
	print("Reading Products...")
	_csvPath = os.path.dirname(os.path.dirname(__file__))
	_customersCSV = os.path.join(_csvPath, "CSVs", "products.csv")

	# Connect to Redis
	r = redis.Redis(host=settings.redisSettings["host"], port=settings.redisSettings["port"], password=settings.redisSettings["password"], db=settings.redisSettings["database"])

	ProcessCSVFile(r, _customersCSV)

	print("Reading Products Completed")
