Hackbright Final Project
============

Resorio is my Hackbright Academy Final Project.  I'll be demoing on Career Day on April 8th.  Resorio is deployed via Heroku and is available for viewing at http://resor.io or http://resorio.herokuapp.com.  

One of my favorite activities is travel, and one of the things I pride myself on is both earning and using points well.  Doing so at present requires a lot of manual research, so I sought to create a product that would make comparison shopping how to spend your hotel points a little bit easier.  My application lets you easily see how much the point cost of hotels across chains compares in a single city, as well as lets you explore redemption options for a given amount of points and look at hotels in a category.  One of the biggest value adds of my application is the relational data provided on how redemptions you're reviewing compare to the average options for that brand.  The brands supported by Resorio are Starwood, Hilton, Hyatt, and Marriott.  I will probably plan on adding in Club Carlson and Priority Club (Intercontinental Hotel Group) at some point in the future.

Resorio was primarily written in Python.  I've got Flask as my framework, MySQL as my database, and have a bit of Javascript thrown in for various front end pieces.  I used Bootstrap, Bootstrap Datepicker, and some custom CSS for the front end.  Resorio employs the Expedia API to combine live data about hotel cost with point information from a Curated Hotels database that I created by combining webscraping (mostly using Beautiful Soup), redemption rules (learned during my years of consulting and fun travel), and the Expedia active properties list.  The average redemption rates are from a database I've created that caches the cents per point of all searches done with Resorio.  

As encouraged by Hackbright, I used an Agile development methodology that included sprints, weekly goals and daily standups with my house.  Below, I'm going to wallk you through what I accomplished in each sprint and what I learned from it.  Due to my eagerness to work on the project, I spent parts of two weekends prior to the official project start making some building blocks.  I've included those as sprints below.

Sprint 1 - Database Fun!
============
Weekend Following Hackbright Week 4

At the end of Week 4 at Hackbright we learn about Databases (yay, databases!) and since I knew I'd need a database that made from the Expedia Active Properties text file, I devoted this weekend to creating that.  Since our initial database work at Hackbright was in SQLite3, I had to spend time researching and learning how to use a big kid database.  I spent substantial time debating and investigating the various database options, and after consulting with my mentors decided to go with MySQL.  After extensive docreading and experimentation, I was able to create a MySQL server and use LOAD IN FILE to convert the Expedia Active Properties text file into a 174k line DB that would be the basis of my project.  Key takeaways from this weekend were the comparative advantages of relational vs. NoSQL DBs and how to start, seed, and query a MySQL DB.

Sprint 2 - Request, API, and JSON
============
Weekend Following Hackbright Week 5

In Week 5 of Hackbright we make our very first web applications, so for me the obvious takeaway was that I was going to make a web application that weekend.  For my second sprint, I decided that I was going to create a working web application that could make a request to the Expedia API and present back results of hotel rooms available in a city.  

The first hurdle was learning how to create and format a request to the Expedia API, which I read about in the documentation and practiced in their API sandbox https://api.eancdn.com/api/tester/#query=basicAvailability.  One of the interesting things I learned was all the different ways you could query: a City/State/Country combination (which I started out with), a Destination string (which I moved to and which is still central to my application), or a list of HotelIds (which is the way I do most of my API requests now).  You cannot query based on brand, TripAdvisor rating, price, or other similar options.

After I mastered how to write an XML request, the next step I took was learning how to send one and get a response.  I ended up using the Requests library for python, relying heavily on the documentation available at http://docs.python-requests.org/en/latest/.

One of the bigest hurdle I faced was how to turn the response object I received back from my request into something I could use in Python.  I spent more google time and doc-searching that I'd like to admit before learning how to use SimpleJSON to unpack the response object and turn it into a useable format.  I ended up becoming quite comfortable with both writing, reading, and analyzing JSONs, and ended up using JSON extensively throughout my project.

Sprint 3 - Webscrape all the Things
============
Hackbright Week 6

Week 6 of Hackbright is a partial project week, and also the week I had to present my Tech Talk (a 5-10 minute presentation on a technical topic that all Hackbright Students must give).  Since I knew the next key step in the process was going to be webscraping category information (which you can use to determine how many points a hotel room will cost),  I decided giving a talk on webscraping was just the right combination of lazy and efficient.  While researching my presentation, I learned a ton about various webscraping options and eventually decided that Beautiful Soup would be right answer for this project.  A copy of my preserntation is available at https://docs.google.com/presentation/d/1i41Fo1ypOCXcRZsxI58ddXrN47eJeKP-70uNhXIMTog/edit?usp=sharing.  Despite knowing how to make a really mean Powerpoint (I'm a former consultant, after all),  I decided to break the cardinal rule of presenting and go for super simplistic slides that don't even need to be presented to make sense.  Gratifyingly, I became the in-house webscraping expert for our Hackbright class, and got to consult with several of my classmates on webscraping for their projects and heard from quite a few others that my presentation helped them along the way.

Once I learned how to scrape, I built rules surrounding the information I wanted to capture and attach to each hotel category, and then went ahead and created functions to scrape the relevant information from the four chains I was working on. Most of the chains had just a few tricky parts (needing a class within a class for Hyatt, capturing high seeason dates for Starwood, copying unlinkable HTML into textfiles and changing my code to analyze that for Marriott), but the Hilton category information was an absolute nightmare to scrape.  In addition to an incredibly complex system for getting from one page of hotels and category to the next, virtually none of their information had classes or IDs that I could use to direct my scraping. In the end, I had to employ Regular Expressions to pull the hotel names associated with a category, and was unable to obtain the links (as all of the ones presented were expiring sessions that redirected to the Hilton homepage).

Sprint 4 - Linking the Data
============
Hackbright Week 7

At the end of Week 6 I'd scraped and built rules around all the information I needed, and stored it in dictionaries saved as JSONs waiting for processing.  In Week 7, I had two goals: create a table of Curated Hotels that combined my scraped dictionaries with the data from the EAN active property list, and update my web application so it presented results from my Curated Hotels database.

The first task wasn't difficult, but was delicate and complex.  After writing a function that iterated through my dictionaries and found matches, I spent nearly half a day writing a SQL query with 27 variables that carefully linked up information pulled from my JSON and EAN Hotels Database and then created an entry in my Curated Hotels database that included all that I was going to need for my updated results page.  

More challenging was figuring out how I was going to pull results from my Curated Hotels database off the loose destination string that users enter, and what the exact data flow was going to be. If a user enters NYC, they should receive the same results as another user who enters New York City or New York or NY, NY, even though only one of those is actually the city name in my curated hotels database. This destination string parsing is actually a pretty complex part of travel searching, and one I knew I didn't have the time to solve.

Luckily, the hotels in the Expedia database also have Region IDs, and I was able to use those to solve the problem.  When someone searches for a destination, I first query my database to see if I've got it stored in a table I have matching destination strings to region codes: if I don't, I send an API request to expedia for hotels in that destination string and use those to find the region code (and then, obviously, store the destination string region code pair for future reference).  Once I have the region code, I use that to query my Curated Hotels database.  With the rows returned by my query, I create a list of hotel IDs (which I'll send to Expedia to get pricing information) and a dictionary of information about the hotels.  I then use the hotel ID list to get live pricing information, and merge that with the dictionary of information I've just stored on the hotels.  The combined data is the core content of the results page. 


Sprint 5 - Data Storage and Deployment
============
Hackbright Week 8

At the beginning of Hackbright Week 8, I realized I was creating interesting data about the average value of the hotel redemptions, and realized I wanted to store and analyze it.  After playing around with the idea of a task queue (I read about them, am comfortable with them, but didn't think it was worth the time investment this early to set one up), I ended up writing and directly calling functions that would store the hotel id and cents per point found in all searches on Resorio.

During Week 8, I also created an additional way of finding hotel redemptions: search by category.  For someone with points to burn but who's slightly destination agnostic (as I often am), this is a great exploration tool and something I'm glad I was able to create.  The tech behind it was pretty simple (just slightly different functions with slightly different MySQL queries), but it was fun to create and amazing to see how easy this was to do relative to just a week ago.

During the last two days of Week 8, I deployed to Heroku.  Due to a compiling issue that neither I, the instructors, nor the Heroku staff could solve, I ended up needing to create a new github repository and moved over key files.  You can check out my original repo at https://github.com/torypayne/hotelproject if you're curious.  Luckily the new repo switch worked, and I'm now deployed and live at resor.io.

Sprint 6 - Beautification and Quality of Life
============
Hackbright Week 9

During our last full project week, I decided to dedicate my time to making my project easy and beautiful to use.  I spent a lot of time during Week 9 learning bootstrap and coming up with a design that both explained my value proposition and brought that value to users. I'm really, really pleased with how it's turned out.  I got to play with some Javascript as I experimented with various pop up datepickers, and think I ended up with one that was beautiful, simple and intuitive.  

I also created an additional search option so users could understand their opportunities based on how many points they had.  This was actually an interesting challenge since I had to care about the order the results were in and cared about linkages between dictionaries that hadn't existed in previous results. 

I rounded out week 9 with quality of life improvements and bug fixes.  I created the ability to update your searches from the results page.  I added pagination to category searches so you could see more than just the first twenty results.  I wrote code that found the best and worst redemptions looked at with Resorio and brought them front and center to share with users.  Most of all, I tested and I debugged.  I found region code irregularities with the Expedia data (where St. Louis is different from Saint Louis which is different from St Louis) and wrote workarounds. I got to the bottom of a weird bug where hotels in Dubai wouldn't load (one of them was missing a Trip Advisor rating).  I wrapped things in Try-Excepts to make sure my site failed elegantly, and always tried to get to the bottom of why things were failing in the first place.

Week 9 was a chaotic, beautiful, bring the project to close mishmash, and I couldn't be any happier with the results.

Going Forward
============

Resorio is pretty amazingly awesome, but I think it could be even better.  Here's what I'm planning on adding in the future:

1. A more robust location search
2. Fun, interesting ways to filter and search (weekend trip from city x, all hotels in Vietnam, more exploration regarding the best redemptions)
3. Multi-city optimization (I'm going to Amsterdam, Berlin and Cologne: where do I spend my Hilton points, where do I spend my Hyatt points, and where do I spend cash?)
4. More curated Hotels in my database
5. A task queue
6. Pulling dynamic high season rates from Hilton
7. Letting users easily import point data from Award Wallet
8. Let users set their own point values and thresholds for what makes an award Good, Great, or Bad.