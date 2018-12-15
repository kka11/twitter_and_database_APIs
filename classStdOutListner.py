from tweepy import OAuthHandler,Stream
from tweepy.streaming import StreamListener
import json, datetime, pymongo
from mongodbFunctions import *
db = connectToDatabase(getMongoClient(), "admin")
class StdOutListner(StreamListener):
	def on_error(self,status):
		print ("error" + str(status))
	def on_data(self,data):
		current_tweet_data = json.loads(data)
		#Now Taken Only those data of tweet which are important
		tweet_id = current_tweet_data["id_str"]
		text = current_tweet_data["text"] #tweet text
		user_screen_name = current_tweet_data["user"]["screen_name"]
		name = current_tweet_data["user"]["name"]
		hashtags = current_tweet_data["entities"]["hashtags"]
		retweet_count = current_tweet_data["retweet_count"]
		favorite_count = current_tweet_data["favorite_count"]
		reply_count = current_tweet_data["reply_count"]
		quote_count = current_tweet_data["quote_count"]
		link_to_count = current_tweet_data["source"]
		dt = current_tweet_data['created_at']
		created = datetime.datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')
		tweet_data = {"tweet_id":tweet_id, "text":text, "name":name, "user_screen_name":user_screen_name, "hashtags":hashtags,
		 "retweet_count":retweet_count, "favorite_count":favorite_count, "reply_count":reply_count, "quote_count":quote_count,
		  "link_to_count":link_to_count, "created":created}#Creating a Dictionary of accessed data
		print("Start Saving tweet")
		#Saving the tweet info into tweets Collection
		db.tweets.insert(tweet_data)
		print ("saved tweet" + text)#Printing only text of tweet
		print("End Saving tweet")
		#Taking Information of the user, who has makes the current tweet
		user_id = current_tweet_data["user"]["id_str"]
		user_name = current_tweet_data["user"]["name"]
		user_screen_name = current_tweet_data["user"]["screen_name"]
		about_user = current_tweet_data["user"]["description"]
		followers = current_tweet_data["user"]["followers_count"]
		friends = current_tweet_data["user"]["friends_count"]
		listed_count = current_tweet_data["user"]["listed_count"]
		favourites_count = current_tweet_data["user"]["favourites_count"]
		user_creation_time = current_tweet_data["user"]["created_at"]
		following = current_tweet_data["user"]["following"]
		location = current_tweet_data["user"]["location"]
		user_data = {"user_id":user_id , "name":user_name, "user_screen_name":user_screen_name, "about_user":about_user,
		 "followers":followers,"friends":friends, "listed_count":listed_count, "favourites_count":favourites_count,
		  "user_creation_time":user_creation_time, "following":following, "location":location}#Creating a Dictionary for User Data
		

		print ("Start Storing User Info")
		#Saving the User info into Users Collection
		db.users.insert(user_data)
		print ("USER NAME IS "+ user_name)
		print("USER SAVED")