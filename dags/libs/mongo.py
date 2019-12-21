import pymongo

# init mongo config
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["youtube"]
collection_sub_channel = db["sub_channel"]
