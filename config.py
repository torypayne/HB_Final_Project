import os
import datetime

env = os.getenv('ENV', "local")
if env == 'prod':
	HOST = "us-cdbr-east-05.cleardb.net"
	USER = "b64cd4ed64d781"
	PASS = "eb2052db"
	DB = "heroku_ff4277368662e82"
	# mysql://b64cd4ed64d781:eb2052db@us-cdbr-east-05.cleardb.net/heroku_ff4277368662e82?reconnect=true
else:
	HOST = "localhost"
	USER = "root"
	PASS = ""
	DB = "hotelchains"

BMARRIOTT = 219357
WMARRIOTT = 226714
BSTARWOOD = 105669
WSTARWOOD = 136353
BHITLON = 173873
WHILTON = 113056
BHYATT = 139597
WHYATT = 163446

DEFCHECKIN = "5/10/2014"
DEFCHECKOUT = "5/12/2014"