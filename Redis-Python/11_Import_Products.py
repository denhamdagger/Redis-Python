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

	hkey = "product:" + row[0]

	# Delete old Customer:id key
	r.delete(hkey)

	rowdata = {}
	rowdata["ID"] = row[0]
	rowdata["Product"] = row[1]
	rowdata["Category"] = row[2]
	rowdata["QuantityPerUnit"] = row[3]
	rowdata["UnitPrice"] = row[4]
	rowdata["UnitsInStock"] = row[5]
	rowdata["UnitsOnOrder"] = row[6]
	rowdata["ReorderLevel"] = row[7]
	rowdata["Discontinued"] = row[8]

	r.hmset(hkey, rowdata)
	r.incr("product-all:count")

if __name__ == "__main__":
	print("Importing Products...")
	_csvPath = os.path.dirname(os.path.dirname(__file__))
	_customersCSV = os.path.join(_csvPath, "CSVs", "products.csv")

	# Connect to Redis
	r = redis.Redis(host=settings.redisSettings["host"], port=settings.redisSettings["port"], password=settings.redisSettings["password"], db=settings.redisSettings["database"])

	# Initialise our customer count to zero
	r.set("product-all:count",0)

	# Insert Customers
	ProcessCSVFile(r, _customersCSV)

	print("Importing Products Completed")
