import os

env = os.getenv('ENV', "local")
if env == 'prod':
	HOST = "localhost"
	USER = "root"
	PASS = ""
	DB = "hotelchains"
	# mysql://b64cd4ed64d781:eb2052db@us-cdbr-east-05.cleardb.net/heroku_ff4277368662e82?reconnect=true
else:
	HOST = "localhost"
	USER = "root"
	PASS = ""
	DB = "hotelchains"