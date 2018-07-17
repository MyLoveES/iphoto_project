from pymongo import MongoClient
client = MongoClient('mongodb://106.15.191.61:27017/')
collection = client.get_database("iphoto").get_collection("share")
editionCollection = client.get_database("iphoto").get_collection("edition")