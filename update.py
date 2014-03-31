import json
import evaluator
import MySQLdb
import config

DB = None
CONN = None

def connect_to_db():
	global DB
	global CONN
	CONN = MySQLdb.connect(host=config.HOST, user=config.USER, passwd=config.PASS, db=config.DB)
	DB = CONN.cursor()

B_W_Dict = {}
B_W_Dict["Best"] = {}
connect_to_db()
query = """SELECT * FROM CPP_VALUES WHERE CentsPerPoint IN (select MAX(CentsPerPoint) FROM CPP_Values GROUP BY CHAIN)"""
DB.execute(query)
rows = DB.fetchall()
for row in rows:
	B_W_Dict["Best"][row[2]] = {}
	B_W_Dict["Best"][row[2]]["eanid"] = row[1]
	B_W_Dict["Best"][row[2]]["cpp"] = row[6]
	B_W_Dict["Best"][row[2]]["regionid"] = row[3]
	B_W_Dict["Best"][row[2]]["checkin"] = row[4]
	B_W_Dict["Best"][row[2]]["checkout"] = row[5]
	r = evaluator.request_single_hotel(row[1], row[4], row[5])
	r = r["HotelListResponse"]["HotelList"]["HotelSummary"]
	B_W_Dict["Best"][row[2]]["city"] = r["city"]
	B_W_Dict["Best"][row[2]]["tripAdvisorRatingUrl"] = r["tripAdvisorRatingUrl"]
	B_W_Dict["Best"][row[2]]["name"] = r["name"]
	photo = r["thumbNailUrl"]
	photo = evaluator.fullsize_image(photo)
	B_W_Dict["Best"][row[2]]["photo"] = photo	


B_W_Dict["Worst"] = {}
query = """SELECT * FROM CPP_VALUES WHERE CentsPerPoint IN (select MIN(CentsPerPoint) FROM CPP_Values GROUP BY CHAIN)"""
DB.execute(query)
rows = DB.fetchall()
for row in rows:
	B_W_Dict["Worst"][row[2]] = {}
	B_W_Dict["Worst"][row[2]]["eanid"] = row[1]
	B_W_Dict["Worst"][row[2]]["cpp"] = row[6]
	B_W_Dict["Worst"][row[2]]["regionid"] = row[3]
	B_W_Dict["Worst"][row[2]]["checkin"] = row[4]
	B_W_Dict["Worst"][row[2]]["checkout"] = row[5]
	r = evaluator.request_single_hotel(row[1], row[4], row[5])
	r = r["HotelListResponse"]["HotelList"]["HotelSummary"]
	B_W_Dict["Best"][row[2]]["city"] = r["city"]
	B_W_Dict["Best"][row[2]]["tripAdvisorRatingUrl"] = r["tripAdvisorRatingUrl"]
	photo = r["thumbNailUrl"]
	photo = evaluator.fullsize_image(photo)
	B_W_Dict["Best"][row[2]]["photo"] = photo	

print B_W_Dict

j = open('bestandworst.json', 'w')

j.write(json.dumps(B_W_Dict))

Avg_CPP_Dict = {}
Avg_CPP_Dict = evaluator.find_average_cpp()

f = open("avgcpp.py", "w")

for key,value in Avg_CPP_Dict.iteritems():
	line = key+"="+str(value)+"\n"
	print line
	f.write(line)

f.close()

