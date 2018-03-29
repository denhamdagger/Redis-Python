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
	# ID,Company,Contact,ContactTitle,Address,City,Region,PostalCode,Country,Phone,Fax

	_key = "customer-contacttitle:" + row[3].replace(" ",".")
	_id = row[0]
	r.sadd(_key, _id)

if __name__ == "__main__":
	print("Reading Customers...")
	_csvPath = os.path.dirname(os.path.dirname(__file__))
	_customersCSV = os.path.join(_csvPath, "CSVs", "customers.csv")

	# Connect to Redis
	r = redis.Redis(host=settings.redisSettings["host"], port=settings.redisSettings["port"], password=settings.redisSettings["password"], db=settings.redisSettings["database"])

	ProcessCSVFile(r, _customersCSV)

	print("Reading Customers Completed")
