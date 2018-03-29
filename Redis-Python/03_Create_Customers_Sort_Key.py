import settings
import redis
import csv
import sys
import os

def ProcessCSVFile(r, _sortkey, csvin):
	with open(csvin, 'rt', encoding='utf-8') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE, )

		# Ignore Row Header
		next(spamreader)

		for row in spamreader:
			ProcessCustomerRow(r, _sortkey, row)

def ProcessCustomerRow(r, sortkey, row):
	# CSV Header
	# ID,Company,Contact,ContactTitle,Address,City,Region,PostalCode,Country,Phone,Fax

	rowdata = {}
	_id = row[0]
	r.lpush(_sortkey, _id)

if __name__ == "__main__":
	print("Reading Customers...")
	_csvPath = os.path.dirname(os.path.dirname(__file__))
	_customersCSV = os.path.join(_csvPath, "CSVs", "customers.csv")
	_sortkey = "customer-id:sort"

	# Connect to Redis
	r = redis.Redis(host=settings.redisSettings["host"], port=settings.redisSettings["port"], password=settings.redisSettings["password"], db=settings.redisSettings["database"])

	# Delete the key in case we need to rerun
	r.delete(_sortkey)

	ProcessCSVFile(r, _sortkey, _customersCSV)

	print("Reading Customers Completed")
