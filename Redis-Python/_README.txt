
Change Settings
-----------------------------------------------------------------
Edit Settings.py to point to your server settings


One thing we need to do is keep track of our key naming standards
-----------------------------------------------------------------
customer:<ID>								Customer record
customer-all:count							Keeps a count of the number of customers
customer-id:sort							Keeps a list of the customer keys
customer-country:<COUNTRY>					Keeps a list of the customer ids for each country
customer-contacttitle:<TITLE>				Keeps a list of the customer ids for each contact title

product:<ID>								Product record
product-all:count							Keeps a count of the number of products
product-all:unitprice						Keeps a sorted set of IDs by Unit price score
