from pymongo import MongoClient
from getpass import getpass



connection_string_local = "mongodb://localhost:27017/"
client = MongoClient(connection_string_local)
db = client["Meme_Generator"]


user_collection = db["Users"]

def signup(newUserName, newUserPassword):
    
    search_result = user_collection.find_one({"name": newUserName})
    if search_result is None:
        insert_result = user_collection.insert_one({
            "name": newUserName,
            "password": newUserPassword
        })
        print("New user id:", insert_result.inserted_id)
        return insert_result.inserted_id 
    else:
        print("Username already exist")
        return None


def login(newUserName, newUserPassword):

    search_result = user_collection.find_one({"name": newUserName})
    if search_result is None:
        return None
    else:
        if search_result["password"] == newUserPassword:
            return search_result["_id"]
        return None



signup_res = signup("abc", "112233")
assert signup_res is not None
signup_res = signup("abc", "112233")
assert signup_res is None
login_res = signup("abc", "112233")
assert login_res is not None
login_res = signup("abc", "11233")
assert login_res is None
user_collection.delete_one({"_id": signup_res})

