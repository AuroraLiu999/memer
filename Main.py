

from pymongo import MongoClient
from getpass import getpass

# 连接到 MongoDB
client = MongoClient("mongodb://localhost:27017/")  # 默认连接到本地 MongoDB
db = client["user_db"]  # 使用或创建名为 "user_db" 的数据库
users_collection = db["users"]  # 使用或创建名为 "users" 的集合

def signup(username, password):
    print("=== USER SIGNUP ===")
    #username = input("Please enter username: ")
    #password = input("Please enter password: ")
    is_signup_succesful  = False
    # 检查用户名是否已存在
    if users_collection.find_one({"username": username}):
        print("Username already exists, please enter another username: ")
        return is_signup_succesful

    # 插入新用户
    user_data = {"username": username, "password": password}
    users_collection.insert_one(user_data)
    print("SUCCESSFULLY SIGNED UP!")
    return is_signup_succesful

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

def main():
    while True:
        print("\n1. Signup\n2. Login\n3. Exit")
        choice = input("Please choose your option by enter '1' or '2' or '3': ")

        if choice == "1":
            signup()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()

