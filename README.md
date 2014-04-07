Hackbright Final Project
============

Resorio is my Hackbright Academy Final Project.  I'll be Demoing on Career Day on April 8th.  Resorio is deployed via Heroku and is available for viewing at resor.io or resorio.herokuapp.com.

One of my favorite activities is travel, and one of the things I pride myself on is both earning and using points well.  Doing so at present requires a lot of manual research, so I sought to create a product that would make comparison shopping how to spend your hotel points a little bit easier.  My application lets you easily see how much the point cost of hotels across chains compares in a single city, as well as lets you explore redemption options for a given amount of points and look at hotels in a category.  One of the biggest value adds of my application is the relational data provided on how redemptions you're reviewing compare to the average options for that brand.

Resorio was primarily written in Python.  I've got Flask as my framework, MySQL as my database, and have a bit of Javascript thrown in for various front end pieces.  Resorio employs the Expedia API to combine live data about hotel cost with point information from a Curated Hotels database that I created by combining webscraping (mostly using Beautiful Soup), redemption rules (learned during my years of consulting and fun travel), and the Expedia active properties list.  The average redemption rates are from a database I've created that caches the cents per point of all searches done with Resorio.

As encouraged by Hackbright, I used an Agile development methodology that included sprints and weekly standups with my house.  Below, I'm going to wallk you through what I accomplished in each sprint and what I learned from it.  Due to my eagerness to work on the project, I spent parts of two weekends prior to the official project start making some building blocks.  I've included those as sprints below.

Sprint 1 - Database fun!
============
Weekend Following Hackbright Week 4

At the end of Week 4 at Hackbright we learn about Databases (yay, databases!) and since I knew I'd need a database that made from the Expedia Active Properties text file, I devoted this weekend to creating that.  Since our initial database work at Hackbright was in SQLite3, I had to spend time researching and learning how to use a big kid database.  I spent substantial time debating and investigating the various database options, and after consulting with my mentors decided to go with MySQL.  After extensive docreading and experimentation, I was able to create a MySQL server and use LOAD IN FILE to convert the Expedia Active Properties text file into a 174k line DB that would be the basis of my project.

Sprint 2 - Request, API, and JSON
============
Weekend Following Hackbright Week 5