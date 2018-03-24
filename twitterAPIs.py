#importing libraries
import pymongo,json,datetime
import unicodecsv as csv
from tweepy import OAuthHandler,Stream
from tweepy.streaming import StreamListener
#These Four values can be taken by making an account on twitter apps
#Enter the access_token , acces_token_secret,consumer_key and consumer_secret
access_token = "YOUR ACCESS TOKEN"
access_token_secret = "YOUR ACCESS TOKEN SECRET"
consumer_key = "YOUR CONSUMER KEY"
consumer_secret = "YOUR CONSUMER SECRET"
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
#Creating a MongClient for Connecting to MongoDB
#If Your Database is not on localhost than, pass a url in MongoClient as parameter
client = pymongo.MongoClient() 
db = client.admin # Connecting to admin Database
#Creating a Class For capturing the Streaming of Twitter
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
#Function for Printing the whole tweet
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
#Function for printing the user details
def userPrint(user_Data):
	print ("-----------------------------------------------------------")
	print 
	print ("user_id 				 :	" + user_Data["user_id"])
	print 
	print ("name 					 :	" + user_Data["name"])
	print 
	print("screen name 				 :	" + user_Data["user_screen_name"])
	print 
	print ("About User 				 :	" + user_Data["about_user"])
	print 
	print ("followers count   		 :	" + str(user_Data["followers"]))
	print 
	print ("following count   		 :	" + str(user_Data["following"]))
	print 
	print ("friends					 :	" + str(user_Data["friends"]))
	print 
	print ("favourites count		 :	" + str(user_Data["favourites_count"]))
	print 
	print ("listed_count			 :	" + str(user_Data["listed_count"]))
	print 
	print ("location				 :	" + user_Data["location"])
	print 
	print ("user creation time			 :	" )
	print (user_Data["user_creation_time"])
	print 
	print ("-----------------------------------------------------------")
#Function for Handling Twitter Streaming 
def STREAMHANDLING():
	keywords = [] # List for Filtered Keywords
	number_of_words = input("Enter number of Target Words 	")
	for  i in range(number_of_words):
		keywords.append(raw_input("Enter a Target word 	"))
	StreamListenObject = StdOutListner()
	try:
		stream = Stream(auth , StreamListenObject)
		stream.filter(track=keywords)
	except KeyboardInterrupt:
		#a = raw_input("")
		#if(a == 'q'):
		#print ("Keyboard Interrupt")
		print ("CLosing the Twitter Stream")
		stream.disconnect()
		return
#Function For tweet and user data from Database
def FILTERSANDCSVHANDLING():
	print ("	1.FILTER FOR TWEETS")
	print ("	2.FILTER FOR USERS")
	print (" 	-----ENTER YOUR CHOICE-----")
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
		print (" 		-----ENTER YOUR CHOICE-----")
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
				print ("-----------------------------------------------")
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('tweetFilterUsingUserName.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("---------------------------------------------------------")
						print ("FILTERED TWEETS HAVE SAVED IN tweetFilterUsingUserName.csv.csv")
						print ("---------------------------------------------------------")
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
				print ("---------------------------------------------")
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('tweetFilterUsingUserScreenName.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("-----------------------------------------------------------")
						print ("FILTERED TWEETS HAVE SAVED IN tweetFilterUsingUserScreenName.csv")
						print ("-----------------------------------------------------------")
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
				print ("----------------------------------------------")
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('tweetFilterUsingTweetText.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("------------------------------------------------------")
						print ("FILTERED TWEETS HAVE SAVED IN tweetFilterUsingTweetText.csv")
						print ("------------------------------------------------------")
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
				print ("------------------------------------------------")
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('tweetFilterUsingRetweetCount.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("---------------------------------------------------------")
						print ("FILTERED TWEETS HAVE SAVED IN tweetFilterUsingRetweetCount.csv")
						print ("---------------------------------------------------------")
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
				print ("----------------------------------------------")
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('tweetFilterUsingFavoriteCount.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("----------------------------------------------------------")
						print ("FILTERED TWEETS HAVE SAVED IN tweetFilterUsingFavoriteCount.csv")
						print ("----------------------------------------------------------")
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
				print ("------------------------------------------------")
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('tweetFilterUsingReplyCount.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("-------------------------------------------------------")
						print ("FILTERED TWEETS HAVE SAVED IN tweetFilterUsingReplyCount.csv")
						print ("-------------------------------------------------------")
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
				print ("-----------------------------------------------")
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('tweetFilterUsingQuoteCount.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("-------------------------------------------------------")
						print ("FILTERED TWEETS HAVE SAVED IN tweetFilterUsingQuoteCount.csv")
						print ("-------------------------------------------------------")
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
				print ("--------------------------------------------------")
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('tweetFilterUsingTweetID.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("----------------------------------------------------")
						print ("FILTERED TWEETS HAVE SAVED IN tweetFilterUsingTweetID.csv")
						print ("----------------------------------------------------")
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
		print (" 		-----ENTER YOUR CHOICE-----")
		choice = raw_input("")
		all_user_data = db.users.find()
		if choice == "1":
			screen_name_bool = 0
			mylist = []
			screenName = raw_input("ENTER SCREEN NAME OF USER 	")
			for users_row in all_user_data:
				if(users_row["user_screen_name"] == screenName):
					print ("		DETAIL OF USER -")
					#print (users_row)
					userPrint(users_row)
					mylist.append(users_row)
					screen_name_bool = 1
			if screen_name_bool == 0:
				print ("---------------------------------------")
				print ("NO USER WITH GIVEN SCREEN NAME IS FOUND")
				print ("---------------------------------------")
			elif screen_name_bool == 1:
				print ("------------------------------------------------")
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('usersFilterUsingScreenName.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("-------------------------------------------------------")
						print ("FILTERED USERS HAVE SAVED IN usersFilterUsingScreenName.csv")
						print ("-------------------------------------------------------")
		elif choice == "2":
			name_bool = 0
			mylist = []
			Name = raw_input("ENTER NAME OF USER 	")
			for users_row in all_user_data:
				if(users_row["name"] == Name):
					print ("		DETAIL OF USER -")
					userPrint(users_row)
					mylist.append(users_row)
					name_bool = 1
			if name_bool == 0:
				print ("--------------------------------")
				print ("NO USER WITH GIVEN NAME IS FOUND")
				print ("--------------------------------")
			elif name_bool == 1:
				print ("---------------------------------------------------")
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('usersFilterUsingName.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("-------------------------------------------------")
						print ("FILTERED USERS HAVE SAVED IN usersFilterUsingName.csv")
						print ("-------------------------------------------------")				
		elif choice == "3":
			id_bool = 0
			mylist = []
			ID = raw_input("ENTER ID OF USER 	")
			for users_row in all_user_data:
				if (users_row["user_id"] == ID):
					print ("		DETAIL OF USER -")
					userPrint(users_row)
					mylist.append(users_row)
					id_bool = 1
			if(id_bool == 0):
				print ("------------------------------")
				print ("NO USER WITH GIVEN ID IS FOUND")
				print ("------------------------------")
			elif id_bool == 1:
				print ("-------------------------------------------------")
				answer = raw_input("WANT TO SAVE THIS FILTERED DATA AS CSV FILE(y/n)")
				if(answer == "y" or answer == "Y" or answer == "yes" or answer == "YES" or answer == "Yes"):
					keys = mylist[0].keys()
					with open('usersFilterUsingUserID.csv', 'wb') as output_file:
						dict_writer = csv.DictWriter(output_file, keys)
						dict_writer.writeheader()
						dict_writer.writerows(mylist)
						print ("---------------------------------------------------")
						print ("FILTERED USERS HAVE SAVED IN usersFilterUsingUserID.csv")
						print ("---------------------------------------------------")
		else :
			print ("----------------------------------")
			print ("	PLEASE ENTER CORRECT KEY")
			print ("----------------------------------")
	else:
		print ("------------------------------")
		print("PLEASE ENTER CORRECT KEY.")
		print ("------------------------------")
def main():
	while(1):
		print ("1.EXTRACT AND SAVE DATA FROM TWITTER STREAMING")
		print ("2.EXTRACT SAVED INFO AND GENERATE CSV FILES FROM DATABASE USING FILTERS")
		print ("3.GENERATE CSV FILES OF ALL SAVED TWEETS OR ALL SAVED USERS")
		print ("4.EXIT")
		print (" 	-----ENTER YOUR CHOICE-----")
		choice = raw_input("")
		if choice == "1":
			STREAMHANDLING()
		elif choice == "2":
			FILTERSANDCSVHANDLING()
		elif choice == "3":
			print ("		1.GENERATE CSV FILES OF ALL TWEETS")
			print ("		2.GENERATE CSV FILES OF ALL USERS")
			print (" 	-----ENTER YOUR CHOICE-----")
			choice = raw_input("")
			if choice == "1":
				all_tweets_data = db.tweets.find()
				keys = all_tweets_data[0].keys()
				with open('tweets.csv', 'wb') as output_file:
					dict_writer = csv.DictWriter(output_file, keys)
					dict_writer.writeheader()
					dict_writer.writerows(all_tweets_data)
					print ("-----------------------------------------")
					print ("ALL TWEETS HAVE SAVED IN tweets.csv")
					print ("-----------------------------------------")
			elif choice == "2":
				all_user_data = db.users.find()
				keys = all_user_data[0].keys()
				with open('users.csv', 'wb') as output_file:
					dict_writer = csv.DictWriter(output_file, keys)
					dict_writer.writeheader()
					dict_writer.writerows(all_user_data)
					print ("-----------------------------------------")
					print ("ALL USERS HAVE SAVED IN users.csv")
					print ("-----------------------------------------")
			else :
				print("PLEASE ENTER CORRECT CHOICE")
		elif choice == "4":
			print ("EXIT")
			break
		else :
			print (" PLEASE ENTER CORRECT KEY")
main()