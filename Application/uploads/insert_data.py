from pymongo import MongoClient # 这是在import什么？之后都用到了哪些相关的函数？？？？？？？？？？？
from bson.objectid import ObjectId # 这是在import什么？之后都用到了哪些相关的函数？？？？？？？？？？？

# MongoDB connection details
mongo_uri = "mongodb://localhost:27017"  # Replace with your MongoDB URI # connection_string_local # 之前都是connection_string_local，为什么这次改了？？？？？？？？？？？？？？
database_name = "MemeGenSample"  # Replace with your database name
collection_name = "Meme" # Replace with your collection name

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# Username to use for all entries
username = "None"

# Generate and insert data
for i in range(1, 44):  # From 1 to 43 (inclusive)
    filename = f"meme{i}.PNG"
    document = {
        "_id": ObjectId(),  # Automatically generate a new ObjectId
        "username": username,
        "filename": filename
    }
    # Insert the document into the collection
    collection.insert_one(document)
    print(f"Inserted: {filename}")

print("All documents inserted successfully!")