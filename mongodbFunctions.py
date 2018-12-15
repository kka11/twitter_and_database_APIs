import pymongo

#Creating a MongClient for Connecting to MongoDB
#If Your Database is not on localhost than, pass a url in MongoClient as parameter
def getMongoClient():
	return pymongo.MongoClient()

# Connecting to admin Database
# If database name is not passsed, then default database name will be admin
def connectToDatabase(client, databaseName = "admin"):
	return client.databaseName