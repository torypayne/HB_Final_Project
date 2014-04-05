from flask import Flask, render_template, redirect, request, url_for, flash, session
import requests
import json
from pprint import pprint
import evaluator
import avgcpp
import config


app = Flask(__name__)
app.secret_key = "tempsecret"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://b64cd4ed64d781:eb2052db@us-cdbr-east-05.cleardb.net/heroku_ff4277368662e82?reconnect=true"
hotel_points_dictionary = {"Hyatt" : [5000,8000,12000,15000,20000,25000,30000], 
							"Starwood" : [3000,4000,7000,10000,12000,20000,30000], 
							"Hilton" : [5000, 10000, 20000, 20000, 30000, 30000, 30000, 40000, 50000, 70000], 
							"Marriott" : [7500,10000,15000,20000,25000,30000,35000,40000,45000]}

@app.route("/")
def index():
	json_data=open('bestandworst.json')
	data = json.load(json_data)
	return render_template("altindex.html", BW = data, HiltonCPP = avgcpp.Hilton, 
							HyattCPP = avgcpp.Hyatt, MarriottCPP = avgcpp.Marriott,
							StarwoodCPP = avgcpp.Starwood)

@app.route("/test")
def test():
	json_data=open('bestandworst.json')
	data = json.load(json_data)
	return render_template("altindex.html", BW = data, HiltonCPP = avgcpp.Hilton, 
							HyattCPP = avgcpp.Hyatt, MarriottCPP = avgcpp.Marriott,
							StarwoodCPP = avgcpp.Starwood)

@app.route("/", methods=["POST"])
def search_data():
	city = request.form.get("search")
	checkin = request.form.get("checkin")
	checkout = request.form.get("checkout")
	return redirect(url_for("search_results", city=city, 
											checkin=checkin, 
											checkout=checkout))

@app.route("/catsearch")
def cat_search():
	try:
		brand = request.args.get("catbrand")
		category = request.args.get("catnumber")
		checkin = request.args.get("catcheckin")
		checkout = request.args.get("catcheckout")
		# print brand
		# print category
		# print evaluator.search_cat(brand,category)
		hotel_tuple = evaluator.search_cat(brand, category)
		# print hotel_tuple
		hotel_list = hotel_tuple[0]
		hotel_dict = hotel_tuple[1]
		expedia_list = evaluator.request_specific_hotels(hotel_list,checkin,checkout)
		pretty_string =brand+" Category "+str(category)
		CPP_dictionary = {"Hilton" : avgcpp.Hilton, 
							"Hyatt" : avgcpp.Hyatt, 
							"Marriott" : avgcpp.Marriott,
							"Starwood" : avgcpp.Starwood}
		r = expedia_list["HotelListResponse"]["HotelList"]["HotelSummary"]
		r = evaluator.merge_data(r, hotel_dict)
		print "Just tried to merge data"
		# if evaluator.cpp_already_stored(region, checkin, checkout) == False:
		# 	evaluator.store_cpp(r, region, checkin, checkout)
		return render_template("altsearch.html", city=pretty_string, 
											checkin=checkin, 
											checkout=checkout, 
											hotel_list=r,
											CPP_dictionary=CPP_dictionary)
	except:
		flash("Oh no! We couldn't find any hotels that matched your request! Double check your destination spelling and specificity, then try different dates.")
		return redirect(url_for("index"))

@app.route("/search")
def search_results():
	try:
		city = request.args.get("city")
		checkin = request.args.get("checkin")
		checkout = request.args.get("checkout")
		region = evaluator.find_region_code(city, checkin, checkout)
		CPP_dictionary = {"Hilton" : avgcpp.Hilton, 
						"Hyatt" : avgcpp.Hyatt, 
						"Marriott" : avgcpp.Marriott,
						"Starwood" : avgcpp.Starwood}
		hotel_tuple = evaluator.curated_hotels_by_region(region)
		hotel_list = hotel_tuple[0]
		hotel_dict = hotel_tuple[1]
		expedia_list = evaluator.request_specific_hotels(hotel_list,checkin,checkout)
		r = expedia_list["HotelListResponse"]["HotelList"]["HotelSummary"]
		r = evaluator.merge_data(r, hotel_dict)
		if evaluator.cpp_already_stored(region, checkin, checkout) == False:
			evaluator.store_cpp(r, region, checkin, checkout)
		return render_template("altsearch.html", city=city, 
											checkin=checkin, 
											checkout=checkout, 
											hotel_list=r,
											CPP_dictionary=CPP_dictionary)
	except:
		flash("Oh no! We couldn't find any hotels that matched your request! Double check your destination spelling and specificity, then try different dates.")
		return redirect(url_for("index"))
	# flash("You made it past to the end of your code!")
	# return redirect(url_for("index"))


@app.route("/pointsearch")
def point_search():
	# try:
	brand = request.args.get("pointsbrand")
	points = request.args.get("points")
	category_tuple = evaluator.point_options_list(points, brand)
	options = category_tuple[0]
	category_list = category_tuple[1]
	return render_template("pointsearch.html", points=points, 
										brand=brand, 
										category_list=category_list,
										options=options,
										checkin=config.DEFCHECKIN,
										checkout=config.DEFCHECKOUT)
	# except:
	# 	flash("hey, look at you searching those points")
	# 	# flash("Oh no! We couldn't find any hotels that matched your request! Double check your destination spelling and specificity, then try different dates.")
	# 	return redirect(url_for("index"))


@app.route("/cpp")
def cpp():
	json_data=open('bestandworst.json')
	data = json.load(json_data)
	chain_cpp = evaluator.find_average_cpp()
	return render_template("cpp.html", chain_cpp=chain_cpp, BW = data, HiltonCPP = avgcpp.Hilton, 
							HyattCPP = avgcpp.Hyatt, MarriottCPP = avgcpp.Marriott,
							StarwoodCPP = avgcpp.Starwood)


@app.route("/register")
def register():
	return render_template("register.html")
	# if session.get("username"):
	#     return redirect(url_for("user_wall",username=session['username']))
	# else:
	#     return render_template("register.html")

@app.route("/register", methods=["POST"])     
def register_user():
	email = request.form.get("email")
	password = request.form.get("password")
	password_verify = request.form.get("password_verify")
	response = evaluator.create_account(email, password, password_verify)
	if response == 1:
		flash("That email address is already in use. Please try again.")
		return redirect(url_for("register"))
	elif response == 2:
		flash("Passwords do not match. Please try again.")
		return redirect(url_for("register"))
	else:
		flash("Success! Please log in to customize your account information.")
		return redirect(url_for("login"))


@app.route("/login")
def login():
	return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
	email = request.form.get("email")
	password = request.form.get("password")
	print evaluator.authenticate(email, password)
	if evaluator.authenticate(email, password) == True:
		flash("You're logged in!")
		session['email'] = email
		return redirect(url_for("index"))
	else:
		flash("Username or password incorrect")
		return redirect(url_for("login"))


# @app.route("/mypoints")
# def show_points():
# 	evaluator.find_points(session['email'])
# 	return render_template("mypoints.html")


if __name__ == "__main__":
	app.run(debug = True)