from flask import Flask, render_template, redirect, request, url_for, flash, session
import requests
import json
from pprint import pprint
import evaluator
import avgcpp


app = Flask(__name__)
app.secret_key = "tempsecret"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://b64cd4ed64d781:eb2052db@us-cdbr-east-05.cleardb.net/heroku_ff4277368662e82?reconnect=true"

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

@app.route("/catsearch", methods=["POST"])
def cat_search():
	brand = request.form.get("catbrand")
	category = request.form.get("catnumber")
	checkin = request.form.get("catcheckin")
	checkout = request.form.get("catcheckout")
	# print brand
	# print category
	# print evaluator.search_cat(brand,category)
	hotel_tuple = evaluator.search_cat(brand, category)
	# print hotel_tuple
	hotel_list = hotel_tuple[0]
	hotel_dict = hotel_tuple[1]
	expedia_list = evaluator.request_specific_hotels(hotel_list,checkin,checkout)
	pretty_string =brand+" Category "+str(category)
	try:
		print "made it into the try"
		r = expedia_list["HotelListResponse"]["HotelList"]["HotelSummary"]
		print r
		print "trying to marge data"
		r = evaluator.merge_data(r, hotel_dict)
		print "Just tried to merge data"
		# if evaluator.cpp_already_stored(region, checkin, checkout) == False:
		# 	evaluator.store_cpp(r, region, checkin, checkout)
		return render_template("search.html", city=pretty_string, 
											checkin=checkin, 
											checkout=checkout, 
											hotel_list=r)
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
	flash("hey, look at you searching those points")
	return redirect(url_for("index"))


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