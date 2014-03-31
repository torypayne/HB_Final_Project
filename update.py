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

print B_W_Dict

f = open('bestandworst.json', 'w')

f.write(json.dumps(B_W_Dict))
