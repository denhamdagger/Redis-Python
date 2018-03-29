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

	hkey = "customer:" + row[0]

	# Delete old Customer:id key
	r.delete(hkey)

	rowdata = {}
	rowdata["ID"] = row[0]
	rowdata["Company"] = row[1]
	rowdata["Contact"] = row[2]
	rowdata["ContactTitle"] = row[3]
	rowdata["Address"] = row[4]
	rowdata["City"] = row[5]
	if row[6] != "NULL":
		rowdata["Region"] = row[6]
	if row[7] != "NULL":
		rowdata["PostalCode"] = row[7]
	rowdata["Country"] = row[8]
	rowdata["Phone"] = row[9]
	if row[10] != "NULL":
		rowdata["Fax"] = row[10]

	r.hmset(hkey, rowdata)
	r.incr("customer-all:count")

if __name__ == "__main__":
	print("Importing Customers...")
	_csvPath = os.path.dirname(os.path.dirname(__file__))
	_customersCSV = os.path.join(_csvPath, "CSVs", "customers.csv")

	# Connect to Redis
	r = redis.Redis(host=settings.redisSettings["host"], port=settings.redisSettings["port"], password=settings.redisSettings["password"], db=settings.redisSettings["database"])

	# Initialise our customer count to zero
	r.set("customer-all:count",0)

	# Insert Customers
	ProcessCSVFile(r, _customersCSV)

	print("Importing Customers Completed")
