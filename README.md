# twitter_and_database_APIs
This Software is developed by Ankit Kumar(B15CS008) student of IIT JODHPUR. It is developed in python.

What Program Does - 

You can fetch data from twitter streaming for given words.

you can store the fetched data from twitter to a MongoDB Database.

you can access and generate csv files of the data(Stored in MongoDB Database) using filters.




Tested on python 2.7


HOW TO RUN - 

      1. Install following libraries of python.
          pymongo
          tweepy
          datetime
      2. Install MongoDB and run it on your local host, if you are not running it on your local host than pass the 
         URL to MongoClient
      3. Enter the following values in the code (You can get these values by making a account on twitter apps)
          access_token = "YOUR ACCES TOKEN" #(on line number 8)
          access_token_secret = "YOUR ACCESS TOKEN SECRET" # (on line number 9)
          consumer_key = "YOUR CONSUMER KEY" # (on line number 10)
          consumer_secret = "YOUR CONSUMER SECRET" # (on line number 11)
      4. Make Sure you have an active Internet Connection for streaming of data from Twitter.
      5. Run the following command - 
          sudo service mongod start
          sudo service mongod status #Make sure you found this active(running)
          python twitterAPIs.py
      6. If tweets are coming from twitter streaming and you want to stop the streaming(not program), 
          Press ctrl + c
          press 'q'(No need to enter the ' ' characters)
      7. Just follow what prints on your terminal
      
      
      
In case of any query drop me a mail at kumar.11@iitj.ac.in 
       
