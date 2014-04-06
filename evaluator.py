from flask import Flask, render_template, redirect, request, url_for, flash
import MySQLdb
import requests
import json
# from pprint import pprint
import time
import config


DB = None
CONN = None


hotel_points_dictionary = {"Hyatt" : [5000,8000,12000,15000,20000,25000,30000], 
							"Starwood" : [3000,4000,7000,10000,12000,20000,30000], 
							"Hilton" : [5000, 10000, 20000, 20000, 30000, 30000, 30000, 40000, 50000, 70000], 
							"Marriott" : [7500,10000,15000,20000,25000,30000,35000,40000,45000]}


def connect_to_db():
	global DB
	global CONN
	CONN = MySQLdb.connect(host=config.HOST, user=config.USER, passwd=config.PASS, db=config.DB)
	DB = CONN.cursor()


def make_xml_request(destination, checkin, checkout):
	xml_request = "<HotelListRequest><destinationstring>"+destination+"</destinationstring><arrivalDate>"+checkin+"</arrivalDate><departureDate>"+checkout+"</departureDate></HotelListRequest>"
	payload = {"cid": "55505", "minorRev": "99", 
			"apiKey": "rddk3k82jjqbk4wgfbkb6qg8",
			"locale": "en_US", "currencyCode": "USD",
			"xml": xml_request}
 
			# "cid": "55505", "minorRev": "99", 
			# "apiKey": "pnqbxpnwvest5ap5qrry4pk8", 
	r = requests.get("http://api.eancdn.com/ean-services/rs/hotel/v3/list?", params=payload)
	r = json.loads(r.text)
	# pprint(r)
	return r

def request_specific_hotels(hotel_id_list,checkin, checkout):
	hotel_id_list = ",".join([str(i) for i in hotel_id_list])
	xml_request = "<HotelListRequest><hotelIdList>"+hotel_id_list+"</hotelIdList><arrivalDate>"+checkin+"</arrivalDate><departureDate>"+checkout+"</departureDate></HotelListRequest>"
	print xml_request
	payload = {"cid": "55505", "minorRev": "99", 
			"apiKey": "rddk3k82jjqbk4wgfbkb6qg8",
			"locale": "en_US", "currencyCode": "USD",
			"xml": xml_request}
	r = requests.get("http://api.eancdn.com/ean-services/rs/hotel/v3/list?", params=payload)
	r = json.loads(r.text)
	# pprint(r)
	return r	

def request_single_hotel(hotel_id_list,checkin, checkout):
	xml_request = "<HotelListRequest><hotelIdList>"+str(hotel_id_list)+"</hotelIdList><arrivalDate>"+checkin+"</arrivalDate><departureDate>"+checkout+"</departureDate></HotelListRequest>"
	print xml_request
	payload = {"cid": "55505", "minorRev": "99", 
			"apiKey": "rddk3k82jjqbk4wgfbkb6qg8",
			"locale": "en_US", "currencyCode": "USD",
			"xml": xml_request}
	r = requests.get("http://api.eancdn.com/ean-services/rs/hotel/v3/list?", params=payload)
	r = json.loads(r.text)
	# pprint(r)
	return r	

#May want to look up some safety stuff since mySQL isn't accepting ? instead of %s
def find_region_code(destination, checkin, checkout):
	connect_to_db()
	query = """SELECT RegionCode FROM RegionCodes WHERE DestinationString = %s"""
	DB.execute(query, (destination,))
	row = DB.fetchone()
	if row:
		code = row[0]
		print "We've already got "+str(code)+" for "+destination
		return code
	else:
		r = make_xml_request(destination,checkin,checkout)
		hotelid = r["HotelListResponse"]["HotelList"]["HotelSummary"][0]["hotelId"]
		query = """SELECT RegionID FROM eanhotellist WHERE eanhotelid = %s"""
		DB.execute(query, (hotelid,))
		row = DB.fetchone()
		code = row[0]
		query = """INSERT INTO RegionCodes (DestinationString, RegionCode) VALUES (%s, %s);"""
		DB.execute(query, (destination,code))
		CONN.commit()
		print "Just added "+str(code)+" for "+destination
		return code
	#connect to DB
	#search for existing string-code match
	#if none, send destination string to expedia api for a hotel id
	#use hotel ID to look up region code
	#write destinationstring and regioncode to DB for future reference

# def region_code_from_hotel_id(hotelid):


def hotel_list_from_rows(rows):
	hotel_lookup_list = []
	hotel_lookup_detail = {}
	for row in rows:
		eanhotelid = row[1]
		hotel_lookup_detail[eanhotelid] = {}
		hotel_lookup_detail[eanhotelid]["name"] = row[2]
		hotel_lookup_detail[eanhotelid]["website"] = row[13]
		hotel_lookup_detail[eanhotelid]["program"] = row[14]
		hotel_lookup_detail[eanhotelid]["category"] = row[15]
		hotel_lookup_detail[eanhotelid]["points"] = row[16]
		hotel_lookup_detail[eanhotelid]["fifthfree"] = row[17]
		hotel_lookup_detail[eanhotelid]["candp"] = row[18]
		hotel_lookup_detail[eanhotelid]["cashofcandp"] = row[19]
		hotel_lookup_detail[eanhotelid]["pointsofcandp"] = row[20]
		hotel_lookup_detail[eanhotelid]["highseason"] = row[21]
		hotel_lookup_detail[eanhotelid]["highseasondates"] = row[22]
		hotel_lookup_detail[eanhotelid]["highseasonpoints"] = row[23]
		hotel_lookup_detail[eanhotelid]["pointsaver"] = row[24]
		hotel_lookup_detail[eanhotelid]["pointsaverdates"] = row[25]
		hotel_lookup_detail[eanhotelid]["pointsaverpoints"] = row[26]
		hotel_lookup_list.append(eanhotelid)
	return (hotel_lookup_list, hotel_lookup_detail)


def curated_hotels_by_region(region):
	connect_to_db()
	query = """SELECT * FROM CuratedHotels WHERE RegionID = %s"""
	DB.execute(query, (region,))
	rows = DB.fetchall()
	return hotel_list_from_rows(rows)



def calculate_totalpoints(hotel_dict):
	total_points = int(hotel_dict["nights"]) * int(hotel_dict["points"])
	if hotel_dict["fifthfree"] == True:
		free_nights = int(hotel_dict["nights"])/5
		total_points = total_points - (free_nights * int(hotel_dict["points"]))
	return total_points

def calculate_cpp(hotel_dict):
	cpp = (float(hotel_dict["totalcost"])/int(hotel_dict["totalpoints"]))*100
	return cpp

def fullsize_image(image_url):
	image_url = image_url.replace("t.jpg","b.jpg")
	return image_url


def merge_data(expedia_list, curated_hotels):
	final_list =[]
	if type(expedia_list) == dict:
		expedia_list = [expedia_list]
	for i in range(len(expedia_list)):
		hotelid = expedia_list[i]["hotelId"]
		hotel_dict = {}
		hotel_dict["hotelId"] = hotelid
		hotel_dict["name"] = expedia_list[i]["name"]
		hotel_dict["address"] = expedia_list[i]["address1"]
		hotel_dict["city"] = expedia_list[i]["city"]
		hotel_dict["countryCode"] = expedia_list[i]["countryCode"]
		try:
			hotel_dict["tripAdvisorRating"] = expedia_list[i]["tripAdvisorRating"]
			hotel_dict["tripAdvisorRatingUrl"] = expedia_list[i]["tripAdvisorRatingUrl"]
			hotel_dict["tripAdvisorReviewCount"] = expedia_list[i]["tripAdvisorReviewCount"]
		except:
			hotel_dict["tripAdvisorRating"] = ""
			hotel_dict["tripAdvisorRatingUrl"] = ""
			hotel_dict["tripAdvisorReviewCount"] = ""
		hotel_dict["locationDescription"] = expedia_list[i]["locationDescription"]
		hotel_dict["latitude"] = expedia_list[i]["latitude"]
		hotel_dict["longitude"] = expedia_list[i]["longitude"]
		hotel_dict["thumbNailUrl"] = fullsize_image(expedia_list[i]["thumbNailUrl"])
		hotel_dict["avgbaserate"] = expedia_list[i]["RoomRateDetailsList"]["RoomRateDetails"]["RateInfos"]["RateInfo"]["ChargeableRateInfo"]["@averageRate"]
		hotel_dict["totalcost"] = expedia_list[i]["RoomRateDetailsList"]["RoomRateDetails"]["RateInfos"]["RateInfo"]["ChargeableRateInfo"]["@total"]
		hotel_dict["roomDescription"] = expedia_list[i]["RoomRateDetailsList"]["RoomRateDetails"]["roomDescription"]
		hotel_dict["nights"] = expedia_list[i]["RoomRateDetailsList"]["RoomRateDetails"]["RateInfos"]["RateInfo"]["ChargeableRateInfo"]["NightlyRatesPerRoom"]["@size"]
		hotel_dict["website"] = curated_hotels[hotelid]["website"]
		hotel_dict["program"] = curated_hotels[hotelid]["program"]
		hotel_dict["category"] = curated_hotels[hotelid]["category"]
		hotel_dict["points"] = curated_hotels[hotelid]["points"]
		hotel_dict["fifthfree"] = curated_hotels[hotelid]["fifthfree"]
		if int(hotel_dict["nights"]) < 5:
			hotel_dict["fifthfree"] = False
		hotel_dict["candp"] = curated_hotels[hotelid]["candp"]
		hotel_dict["cashofcandp"] = curated_hotels[hotelid]["cashofcandp"]
		hotel_dict["pointsofcandp"] = curated_hotels[hotelid]["pointsofcandp"]
		hotel_dict["highseason"] = curated_hotels[hotelid]["highseason"]
		hotel_dict["highseasondates"] = curated_hotels[hotelid]["highseasondates"]
		hotel_dict["highseasonpoints"] = curated_hotels[hotelid]["highseasonpoints"]
		hotel_dict["pointsaver"] = curated_hotels[hotelid]["pointsaver"]
		hotel_dict["pointsaverdates"] = curated_hotels[hotelid]["pointsaverdates"]
		hotel_dict["pointsaverpoints"] = curated_hotels[hotelid]["pointsaverpoints"]
		hotel_dict["totalpoints"] = calculate_totalpoints(hotel_dict)
		hotel_dict["cpp"] = calculate_cpp(hotel_dict)
		# print curated_hotels[hotelid]["name"]
		# hotel_dict["name"] = curated_hotels[hotelid]["name"]
		# print final_list
		final_list.append(hotel_dict)
	return final_list


def cpp_already_stored(RegionID, checkin, checkout):
	query = """SELECT * FROM CPP_values WHERE (RegionID = %s AND CheckIn = %s AND CheckOut = %s)"""
	DB.execute(query, (RegionID, checkin, checkout))
	row = DB.fetchone()
	if row:
		return True
	else:
		return False


def store_cpp(final_list, RegionID, checkin, checkout):
	for hotel in final_list:
		query =  """INSERT INTO CPP_values (EANHotelID, Chain, RegionID, 
			CheckIn, CheckOut, CentsPerPoint) VALUES (%s, %s, %s, %s, %s, %s)"""
		DB.execute(query, (hotel["hotelId"], hotel["program"], RegionID, checkin, checkout, hotel["cpp"]))
	CONN.commit()
	pass

def find_average_cpp():
	chain_cpp = {}
	connect_to_db()
	query = """SELECT Chain, AVG(CentsPerPoint) FROM CPP_values GROUP BY CHAIN"""
	DB.execute(query)
	rows = DB.fetchall()
	for row in rows:
		chain_cpp[row[0]] = row[1]
	return chain_cpp

def create_account(email, password, password_verify):
	connect_to_db()
	email = email
	query = """SELECT email FROM users where email = %s"""
	DB.execute(query, (email,))
	check_username = DB.fetchone()
	if check_username != None:
		return 1
	elif hash(password) != hash(password_verify):
		return 2
	else:
		query = """INSERT INTO users (Email, PasswordHash, System) VALUES (%s, %s, %s)"""
		DB.execute(query, (email, hash(password), "Resor"))
		# print DB._last_executed
		CONN.commit()
		return "New user"

def authenticate(email, password):
	connect_to_db()
	password_input = hash(password)
	query = """SELECT Email, PasswordHash FROM users WHERE email = %s"""
	DB.execute(query, (email,))
	row = DB.fetchone()
	# print row
	DB_password = row[1]
	# print DB_password
	# print password_input
	if int(password_input) == int(DB_password):
		return True
	else:
		return None

def curated_hotels_by_id(hotel_id_list):
	connect_to_db()
	rows = []
	for i in range(len(hotel_id_list)):
		query = """SELECT * FROM CuratedHotels WHERE EANHotelID = %s"""
		DB.execute(query, (int(hotel_id_list[i]),))
		row = DB.fetchone()
		rows.append(row)
	return hotel_list_from_rows(rows)


def find_points(email):
	pass

def search_cat(brand,category):
	connect_to_db()
	query = """SELECT * FROM CuratedHotels WHERE (LoyaltyProgram = %s AND LoyaltyCategory = %s) LIMIT 20"""
	DB.execute(query, (brand, category))
	# print DB._last_executed
	rows =  DB.fetchall()
	# print rows
	return hotel_list_from_rows(rows)

def number_of_pages(brand,category):
	connect_to_db()
	query = """SELECT COUNT(*) FROM CuratedHotels WHERE (LoyaltyProgram = %s AND LoyaltyCategory = %s)"""
	DB.execute(query, (brand, category))
	row = DB.fetchone()
	hotelcount = row[0]
	print hotelcount
	pages = int(hotelcount)/20
	pages += 1
	print pages
	return pages

def number_of_nights(points, brand):
	print brand
	points_list = hotel_points_dictionary[brand]
	options = {}
	for i in range(len(points_list)):
		nights = int(points)/int(points_list[i])
		if nights > 0:
			if nights >= 5:
				if brand != "Hyatt":
					free_nights = nights/5
					nights = nights + free_nights
			options[i+1] = nights
	return options

def find_redemptions(options, brand):
	connect_to_db()
	hotel_rows = ()
	query = """SELECT * FROM CuratedHotels WHERE (LoyaltyProgram = %s AND LoyaltyCategory = %s AND TripAdvisorRating > 4) LIMIT 3"""
	for key in options.iterkeys():
		DB.execute(query, (brand, key))
		rows = DB.fetchall()
		hotel_rows = hotel_rows + rows
	return hotel_list_from_rows(hotel_rows)

def xml_hotels_no_dates(hotel_id_list):
	hotel_id_list = ",".join([str(i) for i in hotel_id_list])
	xml_request = "<HotelListRequest><hotelIdList>"+hotel_id_list+"</hotelIdList></HotelListRequest>"
	print xml_request
	payload = {"cid": "55505", "minorRev": "99", 
			"apiKey": "rddk3k82jjqbk4wgfbkb6qg8",
			"locale": "en_US", "currencyCode": "USD",
			"xml": xml_request}
	r = requests.get("http://api.eancdn.com/ean-services/rs/hotel/v3/list?", params=payload)
	r = json.loads(r.text)
	# pprint(r)
	return r

def merge_data_no_prices(expedia_list, curated_hotels):
	final_list =[]
	if type(expedia_list) == dict:
		expedia_list = [expedia_list]
	for i in range(len(expedia_list)):
		hotelid = expedia_list[i]["hotelId"]
		hotel_dict = {}
		hotel_dict["hotelId"] = hotelid
		hotel_dict["name"] = expedia_list[i]["name"]
		hotel_dict["address"] = expedia_list[i]["address1"]
		hotel_dict["city"] = expedia_list[i]["city"]
		hotel_dict["countryCode"] = expedia_list[i]["countryCode"]
		try:
			hotel_dict["tripAdvisorRating"] = expedia_list[i]["tripAdvisorRating"]
			hotel_dict["tripAdvisorRatingUrl"] = expedia_list[i]["tripAdvisorRatingUrl"]
			hotel_dict["tripAdvisorReviewCount"] = expedia_list[i]["tripAdvisorReviewCount"]
		except:
			hotel_dict["tripAdvisorRating"] = ""
			hotel_dict["tripAdvisorRatingUrl"] = ""
			hotel_dict["tripAdvisorReviewCount"] = ""
		hotel_dict["locationDescription"] = expedia_list[i]["locationDescription"]
		hotel_dict["latitude"] = expedia_list[i]["latitude"]
		hotel_dict["longitude"] = expedia_list[i]["longitude"]
		hotel_dict["thumbNailUrl"] = fullsize_image(expedia_list[i]["thumbNailUrl"])
		hotel_dict["website"] = curated_hotels[hotelid]["website"]
		hotel_dict["program"] = curated_hotels[hotelid]["program"]
		hotel_dict["category"] = curated_hotels[hotelid]["category"]
		hotel_dict["points"] = curated_hotels[hotelid]["points"]
		hotel_dict["fifthfree"] = curated_hotels[hotelid]["fifthfree"]
		hotel_dict["candp"] = curated_hotels[hotelid]["candp"]
		hotel_dict["cashofcandp"] = curated_hotels[hotelid]["cashofcandp"]
		hotel_dict["pointsofcandp"] = curated_hotels[hotelid]["pointsofcandp"]
		hotel_dict["highseason"] = curated_hotels[hotelid]["highseason"]
		hotel_dict["highseasondates"] = curated_hotels[hotelid]["highseasondates"]
		hotel_dict["highseasonpoints"] = curated_hotels[hotelid]["highseasonpoints"]
		hotel_dict["pointsaver"] = curated_hotels[hotelid]["pointsaver"]
		hotel_dict["pointsaverdates"] = curated_hotels[hotelid]["pointsaverdates"]
		hotel_dict["pointsaverpoints"] = curated_hotels[hotelid]["pointsaverpoints"]
		# print curated_hotels[hotelid]["name"]
		# hotel_dict["name"] = curated_hotels[hotelid]["name"]
		# print final_list
		final_list.append(hotel_dict)
	return final_list

def point_options_list(points, brand):
	print brand
	options = number_of_nights(points, brand)
	hotel_tuple = find_redemptions(options, brand)
	hotel_list = hotel_tuple[0]
	hotel_dict = hotel_tuple[1]
	expedia_list = xml_hotels_no_dates(hotel_list)
	expedia_list = expedia_list["HotelListResponse"]["HotelList"]["HotelSummary"]
	r = merge_data_no_prices(expedia_list, hotel_dict)
	cat_list = []
	for i in range(len(options)):
		mini_cat_list = []
		cat_list.append(mini_cat_list)
	for j in range(len(r)):
		cat_index = int(r[j]["category"]) - 1
		cat_list[cat_index].append(r[j])
	return (options, cat_list)




