import pymongo,json,datetime
import unicodecsv as csv
from tweepy import OAuthHandler,Stream
# from tweepy.streaming import StreamListener


from authentication import authenticateIntoTwitter
from mongodbFunctions import *
from utilityFunctions import *
from classStdOutListner import *



#Function for Handling Twitter Streaming
def STREAMHANDLING(auth, db):
	keywords = [] # List for Filtered Keywords
	number_of_words = input("Enter number of Target Words 	")
	for  i in range(number_of_words):
		keywords.append(raw_input("Enter a Target word 	"))
	StreamListenObject = StdOutListner(db)
	try:
		stream = Stream(auth , StreamListenObject)
		stream.filter(track=keywords)
	except KeyboardInterrupt:
		# ON CTRL+C, this section will execute
		print ("Disconnected from Twitter Stream")
		stream.disconnect()
		return

#Function For tweet and user data from Database
def FILTERSANDCSVHANDLING(db):
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
					saveInCSV(mylist, keys, "tweetFilterUsingUserName.csv")
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
					saveInCSV(mylist, keys, "tweetFilterUsingUserScreenName.csv")
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
					saveInCSV(mylist, keys, "tweetFilterUsingTweetText.csv")
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
					saveInCSV(mylist, keys, "tweetFilterUsingRetweetCount.csv")
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
					saveInCSV(mylist, keys, "tweetFilterUsingFavoriteCount.csv")
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
					saveInCSV(mylist, keys, "tweetFilterUsingReplyCount.csv")
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
					saveInCSV(mylist, keys, "tweetFilterUsingQuoteCount.csv")
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
					saveInCSV(mylist, keys, "tweetFilterUsingTweetID.csv")
					print ("FILTERED TWEETS HAVE SAVED IN tweetFilterUsingTweetID.csv")
					print ("----------------------------------------------------")
		elif choice == "9":
			return
		else:
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
					saveInCSV(mylist, keys, "usersFilterUsingScreenName.csv")
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
					saveInCSV(mylist, keys, "usersFilterUsingName.csv")
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
					saveInCSV(mylist, keys, "usersFilterUsingUserID.csv")
					print ("FILTERED USERS HAVE SAVED IN usersFilterUsingUserID.csv")
					print ("---------------------------------------------------")
		else :
			print ("----------------------------------")
			print ("	PLEASE ENTER CORRECT KEY")
	else:
		print ("------------------------------")
		print("PLEASE ENTER CORRECT KEY.")


def getChoice():
	print ("1.EXTRACT AND SAVE DATA FROM TWITTER STREAMING")
	print ("2.EXTRACT SAVED INFO AND GENERATE CSV FILES FROM DATABASE USING FILTERS")
	print ("3.GENERATE CSV FILES OF ALL SAVED TWEETS OR ALL SAVED USERS")
	print ("4.EXIT")
	print (" 	-----ENTER YOUR CHOICE-----")
	choice = raw_input("")
	return choice


def generateCSVFromDatabase(db):
	print ("		1.GENERATE CSV FILES OF ALL TWEETS")
	print ("		2.GENERATE CSV FILES OF ALL USERS")
	print (" 	-----ENTER YOUR CHOICE-----")
	choice = raw_input("")
	if choice == "1":
		all_tweets_data = db.tweets.find()
		keys = all_tweets_data[0].keys()
		saveInCSV(all_tweets_data, keys, "tweets.csv")
		print ("ALL TWEETS HAVE SAVED IN tweets.csv")
		print ("-----------------------------------------")
	elif choice == "2":
		all_user_data = db.users.find()
		keys = all_user_data[0].keys()
		saveInCSV(all_user_data, keys, "users.csv")
		print ("ALL TWEETS HAVE SAVED IN users.csv")
		print ("-----------------------------------------")
	else :
		print("PLEASE ENTER CORRECT CHOICE")


def main():
	auth = authenticateIntoTwitter()
	db = connectToDatabase(getMongoClient(), "admin")
	while(1):
		choice = getChoice()
		if choice == "1":
			STREAMHANDLING(auth, db)
		elif choice == "2":
			FILTERSANDCSVHANDLING(db)
		elif choice == "3":
			generateCSVFromDatabase(db)
		elif choice == "4":
			print ("EXIT")
			break
		else :
			print (" PLEASE ENTER CORRECT KEY")



if __name__ == "__main__":
	main()