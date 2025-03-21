from pymongo import MongoClient
from getpass import getpass
# from Application.helper_functions import *
from gridfs import GridFS

# 连接到 MongoDB
# connection_string_atlas = "mongodb+srv://auroraliu999:Lmy060912%40@cluster0.q6nk2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
connection_string_local = "mongodb://localhost:27017/"
client = MongoClient(connection_string_local)  # 默认连接到本地 MongoDB
db = client["MemeGenSample"]  # 先选择使用哪个数据库

"""
模拟signup
"""
user_collection = db["MemeUser"] # 再从指定的库选择使用哪张表
meme_collection = db["Meme"]

def signup(username, password):
    search_result = user_collection.find_one({"username": username})
    if search_result is None:
        insert_result = user_collection.insert_one({
            "username": username,
            "password": password
        })
        print("New user id:", insert_result.inserted_id)
        return insert_result.inserted_id
    else:
        print("Username Exist")
        return None

def login(username, password):

    search_result = user_collection.find_one({"username": username})
    if search_result is None:
        print("Username does not exist")
        return None
    else:
        if search_result['password'] == password:
            return search_result['_id']
        return None

def upload_meme(username, filename):
    insert_result = meme_collection.insert_one({
        "username": username,
        "filename": filename
    })
    return insert_result.inserted_id


# new_user = signup("abc","123")
# assert new_user is not None
# signup_res = signup("abc","123")
# assert signup_res is None
# login_res = login("abc","123")
# assert login_res is not None
# login_res = login("abc","321")
# assert login_res is None
# user_collection.delete_one({'_id': new_user})


def put_meme_in_db():
    # 初始化 GridFS
    fs = GridFS(db)

    # 遍历图片文件
    for i in range(1, 44):
        try:
            # 读取图片文件
            with open(f'meme{i}.jpg', 'rb') as f:
                image_data = f.read()

            # 将图片存入GridFS
            file_id = fs.put(image_data, filename=f'meme{i}.jpg')
            print(f"Image meme{i}.jpg stored with file_id: {file_id}")

        except FileNotFoundError:
            print(f"File meme{i}.jpg not found, skipping...")
        except Exception as e:
            print(f"An error occurred with meme{i}.jpg: {e}")

        meme_collection.insert_one({"meme1.jpg": "hey"})

put_meme_in_db()