
import unicodecsv as csv

def saveInCSV(all_data, keys, name):
	with open(name, 'wb') as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(all_data)



def tweetPrint(tweet_Data):
	print ("-----------------------------------------------------------")
	print 
	print ("tweet_id 				 :	" + tweet_Data["tweet_id"])
	print ("")
	print ("tweet text 				 :	" + tweet_Data["text"])
	print ("")
	print("tweet made by(screen name):	" + tweet_Data["user_screen_name"])
	print ("")
	print ("tweet made by(name)		 :	" + tweet_Data["name"])
	print ("")
	print ("hashtags 				 :	")
	print (tweet_Data["hashtags"])
	print ("")
	print ("retweet count   		 :	" + str(tweet_Data["retweet_count"]))
	print ("")
	print ("favorite count 			 :	" + str(tweet_Data["favorite_count"]))
	print ("")
	print ("reply count 			 :	" + str(tweet_Data["reply_count"]))
	print ("")
	print ("quote_count 			 :	" + str(tweet_Data["quote_count"]))
	print ("")
	print ("link_to_count 			 :	" + str(tweet_Data["link_to_count"]))
	print ("")
	print ("Tweet time 				 :	" )
	print (tweet_Data["created"])
	print ("")
	print ("-----------------------------------------------------------")





#Function for printing the user details
def userPrint(user_Data):
	print ("-----------------------------------------------------------")
	print ("")
	print ("user_id 				 :	" + user_Data["user_id"])
	print ("")
	print ("name 					 :	" + user_Data["name"])
	print ("")
	print("screen name 				 :	" + user_Data["user_screen_name"])
	print ("")
	print ("About User 				 :	" + user_Data["about_user"])
	print ("")
	print ("followers count   		 :	" + str(user_Data["followers"]))
	print ("")
	print ("following count   		 :	" + str(user_Data["following"]))
	print ("")
	print ("friends					 :	" + str(user_Data["friends"]))
	print ("")
	print ("favourites count		 :	" + str(user_Data["favourites_count"]))
	print ("")
	print ("listed_count			 :	" + str(user_Data["listed_count"]))
	print ("")
	print ("location				 :	" + user_Data["location"])
	print ("")
	print ("user creation time			 :	" )
	print (user_Data["user_creation_time"])
	print ("")
	print ("-----------------------------------------------------------")

