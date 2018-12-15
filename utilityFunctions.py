
import unicodecsv as csv

#function for saving the data in CSV File
def saveInCSV(all_data, keys, name):
	with open(name, 'wb') as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(all_data)

#Function for printing the tweet data
def tweetPrint(tweet_Data):
	print ("-----------------------------------------------------------")
	print ("")
	print ("tweet_id 				 :	" + (tweet_Data["tweet_id"] if tweet_Data["tweet_id"] != None else "NULL"))
	print ("")
	print ("tweet text 				 :	" + (tweet_Data["text"] if tweet_Data["text"] != None else "NULL"))
	print ("")
	print("tweet made by(screen name):	" + (tweet_Data["user_screen_name"] if tweet_Data["user_screen_name"] != None else "NULL"))
	print ("")
	print ("tweet made by(name)		 :	" + (tweet_Data["name"] if tweet_Data["name"] != None else "NULL"))
	print ("")
	print ("hashtags 				 :	")
	print (tweet_Data["hashtags"] if tweet_Data["hashtags"] != None else "NULL")
	print ("")
	print ("retweet count   		 :	" + str(tweet_Data["retweet_count"] if tweet_Data["retweet_count"] != None else "NULL"))
	print ("")
	print ("favorite count 			 :	" + str(tweet_Data["favorite_count"] if tweet_Data["favorite_count"] != None else "NULL"))
	print ("")
	print ("reply count 			 :	" + str(tweet_Data["reply_count"] if tweet_Data["reply_count"] != None else "NULL"))
	print ("")
	print ("quote_count 			 :	" + str(tweet_Data["quote_count"] if tweet_Data["quote_count"] != None else "NULL"))
	print ("")
	print ("link_to_count 			 :	" + str(tweet_Data["link_to_count"] if tweet_Data["link_to_count"] != None else "NULL"))
	print ("")
	print ("Tweet time 				 :	" )
	print (tweet_Data["created"] if tweet_Data["created"] != None else "NULL")
	print ("")
	print ("-----------------------------------------------------------")





#Function for printing the user details
def userPrint(user_Data):
	print (user_Data["about_user"])
	print ("-----------------------------------------------------------")
	print ("")
	print ("user_id 				 :	" + (user_Data["user_id"] if "user_id" in user_Data else "NULL") )
	print ("")
	print ("name 					 :	" + user_Data["name"])
	print ("")
	print("screen name 				 :	" + (user_Data["user_screen_name"] if user_Data["user_screen_name"] != None else "NULL"))
	print ("")
	print ("About User 				 :	" + (user_Data["about_user"] if user_Data["about_user"] != None else "NULL"))
	print ("")
	print ("followers count   		 :	" + str(user_Data["followers"] if user_Data["followers"] != None else "NULL"))
	print ("")
	print ("following count   		 :	" + str(user_Data["following"] if user_Data["following"] != None else "NULL"))
	print ("")
	print ("friends					 :	" + str(user_Data["friends"] if user_Data["friends"] != None else "NULL"))
	print ("")
	print ("favourites count		 :	" + str(user_Data["favourites_count"] if user_Data["favourites_count"] != None else "NULL"))
	print ("")
	print ("listed_count			 :	" + str(user_Data["listed_count"] if user_Data["listed_count"] != None else "NULL"))
	print ("")
	print ("location				 :	" + (user_Data["location"] if user_Data["location"] != None else "NULL"))
	print ("")
	print ("user creation time			 :	" )
	print (user_Data["user_creation_time"] if user_Data["user_creation_time"] != None else "NULL")
	print ("")
	print ("-----------------------------------------------------------")

