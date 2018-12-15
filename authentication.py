from tweepy import OAuthHandler
#These Four values can be taken by making an account on twitter apps
#Enter the access_token , acces_token_secret,consumer_key and consumer_secret
access_token = "your access token"
access_token_secret = "your access token secret"
consumer_key = "your consumer key"
consumer_secret = "your consumer secret"

#Function to authenticate into twitter
def authenticateIntoTwitter():
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	return auth