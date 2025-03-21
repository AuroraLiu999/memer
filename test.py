from pymongo import MongoClient
from getpass import getpass

# 连接到 MongoDB
connection_string_atlas = "mongodb+srv://auroraliu999:Lmy060912%40@cluster0.q6nk2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
connection_string_local = "mongodb://localhost:27017/"
client = MongoClient(connection_string_local)  # 默认连接到本地 MongoDB
db = client["user_db"]  # 使用或创建名为 "user_db" 的数据库
users_collection = db["users"]  # 使用或创建名为 "users" 的集合

def save_info(image_data, image_text):
    # when the user wants to save a meme
    # This should save the image_data in an appropriate folder
    # Save the text in mongodb

    pass

def generate_image(image_data, image_text):
    pass


def login(username, password):
    print("=== USER LOGIN ===")
    #username = input("Please enter username: ")
    #password = input("Please enter password: ")

    # 查找用户
    user = users_collection.find_one({"username": username, "password": password})
    is_login_succesful = False
    if user:
        print("Successfully logged in! Welcome back,{}.".format(username))
        return is_login_succesful
    else:
        print("Username or password is wrong, please try again!")
        return is_login_succesful



# login("liu muyun", "123hahaha")
def signup(username, password):
    print("=== USER  SIGNUP ===")
    #username = input("Please enter username: ")
    #password = input("Please enter password: ")

    # 查找用户
    user = users_collection.find_one({"username": username, "password": password})
    is_login_succesful = False
    if user:
        print("Successfully logged in! Welcome back,{}.".format(username))
        return is_login_succesful
    else:
        print("Username or password is wrong, please try again!")
        return is_login_succesful