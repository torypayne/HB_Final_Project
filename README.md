Hackbright Final Project
============

Resorio is my Hackbright Academy Final Project.  I'll be Demoing on Career Day on April 8th.  Resorio is deployed via Heroku and is available for viewing at resor.io or resorio.herokuapp.com.

One of my favorite activities is travel, and one of the things I pride myself on is both earning and using points well.  Doing so at present requires a lot of manual research, so I sought to create a product that would make comparison shopping how to spend your hotel points a little bit easier.  My application lets you easily see how much the point cost of hotels across chains compares in a single city, as well as lets you explore redemption options for a given amount of points and look at hotels in a category.  One of the biggest value adds of my application is the relational data provided on how redemptions you're reviewing compare to the average options for that brand.

Resorio was primarily written in Python.  I've got Flask as my framework, MySQL as my database, and have a bit of Javascript thrown in for various front end pieces.  Resorio employs the Expedia API to combine live data about hotel cost with point information from a Curated Hotels database that I created by combining webscraping (mostly using Beautiful Soup), redemption rules (learned during my years of consulting and fun travel), and the Expedia active properties list.  The average redemption rates are from a database I've created that caches the cents per point of all searches done with Resorio.

