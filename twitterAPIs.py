import pymongo,json,datetime
import unicodecsv as csv
from tweepy import OAuthHandler,Stream
from tweepy.streaming import StreamListener
access_token = "971294476911235072-BMt5RNb3kQQh4GXQP8LiDmJYzK2DTw2"
access_token_secret = "ubP96v7FFCkYvUbUetck1C6JhfFVSKCGO9oGk0tfzA7gP"
consumer_key = "OHLLZdOQ78IhPluSJoyW5e5ex"
consumer_secret = "n6jaLVEjUOFruAWKINIlAe9CKadBvGtrHnH8EJ9zIpgAw0QrKp"
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
client = pymongo.MongoClient()
db = client.admin
class StdOutListner(StreamListener):
	def on_error(self,status):
		print ("error" + str(status))
	def on_data(self,data):
		current_tweet_data = json.loads(data)

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
		  "link_to_count":link_to_count, "created":created}
		print("Start Saving tweet")
		db.tweets.insert(tweet_data)
		print ("saved tweet" + text)
		print("End Saving tweet")

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
		  "user_creation_time":user_creation_time, "following":following, "location":location}
		print ("Start Storing User Info")
		db.users.insert(user_data)
		print ("USER NAME IS "+ user_name)
		print("USER SAVED")
def tweetPrint(tweet_Data):
	print ("-----------------------------------------------------------")
	print 
	print ("tweet_id 				 :	" + tweet_Data["tweet_id"])
	print 
	print ("tweet text 				 :	" + tweet_Data["text"])
	print 
	print("tweet made by(screen name):	" + tweet_Data["user_screen_name"])
	print 
	print ("tweet made by(name)		 :	" + tweet_Data["name"])
	print 
	print ("hashtags 				 :	")
	print (tweet_Data["hashtags"])
	print 
	print ("retweet count   		 :	" + str(tweet_Data["retweet_count"]))
	print 
	print ("favorite count 			 :	" + str(tweet_Data["favorite_count"]))
	print 
	print ("reply count 			 :	" + str(tweet_Data["reply_count"]))
	print 
	print ("quote_count 			 :	" + str(tweet_Data["quote_count"]))
	print 
	print ("link_to_count 			 :	" + str(tweet_Data["link_to_count"]))
	print 
	print ("Tweet time 				 :	" )
	print (tweet_Data["created"])
	print 
	print ("-----------------------------------------------------------")
def FIRSTAPI():
	keywords = []
	number_of_words = input("Enter number of Target Words 	")
	for  i in range(number_of_words):
		keywords.append(raw_input("Enter a Target word 	"))
	StreamListenObject = StdOutListner()
	stream = Stream(auth , StreamListenObject)
	stream.filter(track=keywords)
def SECONDAPI():
	print ("	1.FILTER FOR TWEETS")
	print ("	2.FILTER FOR USERS")
	choice = raw_input("")
	if choice == "1":
		all_tweets_data = db.tweets.find()
		print ("	1.SEARCH BY USERNAME WHO TWEETED")
		print ("	2.SEARCH BY USER SCREENNAME WHO TWEETED")
		print ("	3.SEARCH USING TWEET TEXT")
		print ("	4.FILTER USING RETWEET COUNT RANGE")
		print ("	5.FILTER USING FAVORITE COUNT RANGE")	
		print ("	6.FILTER USING REPLY COUNT RANGE")
		print ("	7.FILTER USING QUOTE COUNT RANGE")
		print ("	8.FILTER USING TWEET ID")
		#print ("	9.FILTER USING DATE AND TIME RANGE")
		print ("	9.BACK")
		choice = raw_input("")
		if choice == "1":
			username_bool = 0
			mylist = []
			NameOfUser = raw_input("		ENTER NAME OF THE USER    ")
			for tweets_row in all_tweets_data:
				if(tweets_row["name"] == NameOfUser):
					print ("			PRINTING TWEET")
					tweetPrint(tweets_row)
					mylist.append(tweets_row)
					username_bool = 1
			if username_bool == 0:
				print ("-----------------------")
				print ("NO TWEET FOR GIVEN NAME")
				print ("-----------------------")
			elif username_bool == 1:
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('tweetFilterUsingUserName.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("ALL TWEETS HAVE SAVED IN tweetFilterUsingUserName.csv.csv")

		elif choice == "2":
			screenname_bool = 0
			mylist = []
			ScreenName = raw_input("		ENTER SCREEN NAME OF THE USER    ")
			for tweets_row in all_tweets_data:
				if(tweets_row["user_screen_name"] == ScreenName):
					print ("PRINTING TWEET")
					tweetPrint(tweets_row)
					mylist.append(tweets_row)
					screenname_bool = 1
			if screenname_bool == 0:
				print ("------------------------------")
				print ("NO TWEET FOR GIVEN SCREEN NAME")
				print ("------------------------------")
			elif screenname_bool == 1:
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('tweetFilterUsingUserScreenName.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("ALL TWEETS HAVE SAVED IN tweetFilterUsingUserScreenName.csv")

		elif choice == "3":
			tweet_text_bool = 0
			mylist = []
			TweetText = raw_input("		ENTER TWEET TEXT    ")
			for tweets_row in all_tweets_data:
				if(tweets_row["text"] == TweetText):
					print ("PRINTING TWEET")
					tweetPrint(tweets_row)
					mylist.append(tweets_row)
					tweet_text_bool = 1
			if tweet_text_bool == 0:
				print ("------------------------------")
				print ("NO TWEET FOR GIVEN SCREEN NAME")
				print ("------------------------------")
			elif tweet_text_bool == 1:
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('tweetFilterUsingTweetText.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("ALL TWEETS HAVE SAVED IN tweetFilterUsingTweetText.csv")

		elif choice == "4":
			retweet_count_bool = 0
			mylist = []
			smallest_retweet_count = input("		Enter the Lower limit on retweet count    ")
			largest_retweet_count  = input("		Enter the upper limit on retweet count    ")
			for tweets_row in all_tweets_data:
				if(tweets_row["retweet_count"] >= smallest_retweet_count and tweets_row["retweet_count"] <= largest_retweet_count):
					print ("PRINTING TWEET")
					tweetPrint(tweets_row)
					mylist.append(tweets_row)
					retweet_count_bool = 1
			if retweet_count_bool == 0:
				print ("--------------------------------")
				print ("NO TWEET FOR GIVEN RETWEET RANGE")
				print ("--------------------------------")
			elif retweet_count_bool == 1:
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('tweetFilterUsingRetweetCount.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("ALL TWEETS HAVE SAVED IN tweetFilterUsingRetweetCount.csv")

		elif choice == "5":
			favorite_count_bool = 0
			mylist = []
			smallest_favorite_count = input("		Enter the Lower limit on favorite count    ")
			largest_favorite_count  = input("		Enter the upper limit on favorite count    ")			
			for tweets_row in all_tweets_data:
				if(tweets_row["favorite_count"] >= smallest_favorite_count and tweets_row["favorite_count"] <= largest_favorite_count):
					print ("PRINTING TWEET")
					tweetPrint(tweets_row)
					mylist.append(tweets_row)
					favorite_count_bool = 1
			if favorite_count_bool == 0:
				print ("--------------------------------")
				print ("NO TWEET FOR GIVEN FAVORITE COUNT RANGE")
				print ("--------------------------------")	
			elif favorite_count_bool == 1:
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('tweetFilterUsingFavoriteCount.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("ALL TWEETS HAVE SAVED IN tweetFilterUsingFavoriteCount.csv")

		elif choice == "6":
			reply_count_bool = 0
			mylist = []
			smallest_reply_count = input("		Enter the Lower limit on reply count    ")
			largest_reply_count  = input("		Enter the upper limit on reply count    ")
			for tweets_row in all_tweets_data:
				if(tweets_row["reply_count"] >= smallest_reply_count and tweets_row["reply_count"] <= largest_reply_count):
					print ("PRINTING TWEET")
					tweetPrint(tweets_row)
					mylist.append(tweets_row)
					reply_count_bool = 1
			if reply_count_bool == 0:
				print ("------------------------------------------")
				print ("NO TWEET FOR GIVEN REPLY TWEET COUNT RANGE")
				print ("------------------------------------------")
			elif reply_count_bool == 1:
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('tweetFilterUsingReplyCount.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("ALL TWEETS HAVE SAVED IN tweetFilterUsingReplyCount.csv")

		elif choice == "7":
			quote_count_bool = 0
			mylist = []
			smallest_quote_count = input("		Enter the Lower limit on quote count    ")
			largest_quote_count  = input("		Enter the upper limit on quote count    ")
			for tweets_row in all_tweets_data:
				if(tweets_row["quote_count"] >= smallest_quote_count and tweets_row["quote_count"] <= largest_quote_count):
					print ("PRINTING TWEET")
					tweetPrint(tweets_row)
					mylist.append(tweets_row)
					quote_count_bool = 1
			if quote_count_bool == 0:
				print ("------------------------------------")
				print ("NO TWEET FOR GIVEN QUOTE COUNT RANGE")
				print ("------------------------------------")	
			elif quote_count_bool == 1:
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('tweetFilterUsingQuoteCount.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("ALL TWEETS HAVE SAVED IN tweetFilterUsingQuoteCount.csv")
		elif choice == "8":
			tweet_id_bool = 0
			mylist = []
			TweetID = raw_input("		ENTER TWEET ID    ")
			for tweets_row in all_tweets_data:
				if(tweets_row["tweet_id"] == TweetID):
					print ("PRINTING TWEET")
					tweetPrint(tweets_row)
					mylist.append(tweets_row)
					tweet_id_bool = 1
			if tweet_id_bool == 0:
				print ("---------------------------")
				print ("NO TWEET FOR GIVEN TWEET ID")
				print ("---------------------------")
			elif tweet_id_bool == 1:
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('tweetFilterUsingTweetID.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("ALL TWEETS HAVE SAVED IN tweetFilterUsingTweetID.csv")
		elif choice == "9":
			return
		else:
			print ("---------------------------")
			print ("PLEASE ENTER CORRECT CHOICE")
			print ("---------------------------")
	elif choice == "2":
		print ("	1.SEARCH USER BY SCREEN NAME")
		print ("	2.SEARCH USER BY NAME")
		print ("	3.SEARCH USER BY ID")
		choice = raw_input("")
		all_user_data = db.users.find()
		if choice == "1":
			screen_name_bool = 0
			screenName = raw_input("ENTER SCREEN NAME OF USER 	")
			for users_row in all_user_data:
				if(users_row["user_screen_name"] == screenName):
					print ("DETAIL OF USER -")
					print (users_row)
					screen_name_bool = 1
			if screen_name_bool == 0:
				print ("NO USER WITH GIVEN SCREEN NAME IS FOUND")
		elif choice == "2":
			name_bool = 0
			Name = raw_input("ENTER NAME OF USER 	")
			for users_row in all_user_data:
				if(users_row["name"] == Name):
					print ("DETAIL OF USER -")
					print users_row
					name_bool = 1
			if name_bool == 0:
				print ("NO USER WITH GIVEN NAME IS FOUND")
		elif choice == "3":
			id_bool = 0
			ID = raw_input("ENTER ID OF USER 	")
			for users_row in all_user_data:
				if (users_row["user_id"] == ID):
					print ("DETAIL OF USER -")
					print (users_row)
					id_bool = 1
			if(id_bool == 0):
				print ("NO USER WITH GIVEN ID IS FOUND")
	else:
		print("You have entered the wrong key.")
def main():
	while(1):
		print ("1.EXTRACT AND SAVE DATA FROM TWITTER STREAMING")
		print ("2.ETRACT SAVED INFO FROM DATABASE USING FILTERS")
		print ("3.GENERATE CSV FILES OF TWEETS OR USERS")
		print ("4.EXIT")
		choice = raw_input("")
		if choice == "1":
			FIRSTAPI()
		elif choice == "2":
			SECONDAPI()
		elif choice == "3":
			print ("		1.GENERATE CSV FILES OF ALL TWEETS")
			print ("		2.GENERATE CSV FILES OF ALL USERS")
			choice = raw_input("")
			if choice == "1":
				all_tweets_data = db.tweets.find()
				keys = all_tweets_data[0].keys()
				with open('tweets.csv', 'wb') as output_file:
					dict_writer = csv.DictWriter(output_file, keys)
					dict_writer.writeheader()
					dict_writer.writerows(all_tweets_data)
					print ("ALL TWEETS HAVE SAVED IN tweets.csv")
			elif choice == 2:
				all_user_data = db.users.find()
				keys = all_users_data[0].keys()
				with open('users.csv', 'wb') as output_file:
					dict_writer = csv.DictWriter(output_file, keys)
					dict_writer.writeheader()
					dict_writer.writerows(all_users_data)
					print ("ALL USERS HAVE SAVED IN users.csv")
			else :
				print("PLEASE ENTER CORRECT CHOICE")
		elif choice == "4":
			print ("EXIT")
			break
		else :
			print ("ENTER CORRECT KEY")
main()