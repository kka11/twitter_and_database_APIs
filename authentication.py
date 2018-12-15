#These Four values can be taken by making an account on twitter apps
#Enter the access_token , acces_token_secret,consumer_key and consumer_secret
from tweepy import OAuthHandler
access_token = "971294476911235072-BMt5RNb3kQQh4GXQP8LiDmJYzK2DTw2"
access_token_secret = "ubP96v7FFCkYvUbUetck1C6JhfFVSKCGO9oGk0tfzA7gP"
consumer_key = "OHLLZdOQ78IhPluSJoyW5e5ex"
consumer_secret = "n6jaLVEjUOFruAWKINIlAe9CKadBvGtrHnH8EJ9zIpgAw0QrKp"

#Function to authenticate into twitter
def authenticateIntoTwitter():
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	return auth