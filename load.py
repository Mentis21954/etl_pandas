import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
artists = db['artists']

def load_to_dabase(artist_info):
    artists.insert_one(artist_info)
