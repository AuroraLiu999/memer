from pymongo import MongoClient
import random

# 连接到 MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["media_db"]

# 集合
images_collection = db["images"]
stickers_collection = db["stickers"]
filters_collection = db["filters"]
texts_collection = db["texts"]
colors_collection = db["colors"]
emojis_collection = db["emojis"]

def upload_media():
    print("=== UPLOAD PICTURE OR GIF ===")
    file_path = input("Please enter the file path of the photo or animated image: ")
    print(f"Chosen Folder: {file_path}")
    # 模拟文件上传和显示
    print("File uploaded and it's presenting.")

    # 编辑选项
    while True:
        print("\nOptions: 1. Fliter 2. Crop 3. Text 4. Emoji 5. Color 6. Done")
        choice = input("Please choose your option by entering the number: ")

        if choice == "1":
            filters = list(filters_collection.find())
            print("Fliters you can choose from:")
            for i, filter in enumerate(filters):
                print(f"{i + 1}. {filter['name']}")
            filter_choice = int(input("Please choose your fliter: ")) - 1
            print(f"Fliter applied: {filters[filter_choice]['name']}")
        elif choice == "2":
            print("Cropping is enabled.")
        elif choice == "3":
            texts = list(texts_collection.find())
            print("Styles you can choose from:")
            for i, text in enumerate(texts):
                print(f"{i + 1}. {text['style']}")
            text_choice = int(input("Please choose your style: ")) - 1
            print(f"Style applied: {texts[text_choice]['style']}")
        elif choice == "4":
            stickers = list(stickers_collection.find())
            print("Emojis you can choose from:")
            for i, sticker in enumerate(stickers):
                print(f"{i + 1}. {sticker['name']}")
            sticker_choice = int(input("Please choose your emoji: ")) - 1
            print(f"Emoji added: {stickers[sticker_choice]['name']}")
        elif choice == "5":
            colors = list(colors_collection.find())
            print("Colors you can choose from:")
            for i, color in enumerate(colors):
                print(f"{i + 1}. {color['name']}")
            color_choice = int(input("PLease choose your color: ")) - 1
            print(f"Color applied: {colors[color_choice]['name']}")
        elif choice == "6":
            print("Done editting.")
            break
        else:
            print("Invalid option, please try again.")

    # 下载和分享
    print("\n1. Download 2. Share")
    action = input("Please choose your option by entering the number: ")
    if action == "1":
        print("Meme downloaded.")
    elif action == "2":
        print("Meme shared.")

def auto_emoji():
    print("=== Automatically bring up meme ===")
    emojis = list(emojis_collection.find())
    emoji = random.choice(emojis)
    print(f"Meme brought: {emoji['name']}")

    # 下载和分享
    print("\n1. Downoad 2. Share")
    action = input("Please choose your option by entering the number: ")
    if action == "1":
        print("Meme downloaded.")
    elif action == "2":
        print("Meme shared.")

def fetch_image():
    print("=== Automatically bring up picture ===")
    images = list(images_collection.find())
    image = random.choice(images)
    print(f"Picture brought: {image['name']}")

    # 编辑选项
    while True:
        print("\nOptions: 1. Fliter 2. Crop 3. Text 4. Emoji 5. Color 6. Done")
        choice = input("Please choose your option by entering the number: ")

        if choice == "1":
            filters = list(filters_collection.find())
            print("Fliters you can choose from:")
            for i, filter in enumerate(filters):
                print(f"{i + 1}. {filter['name']}")
            filter_choice = int(input("PLease choose your fliter: ")) - 1
            print(f"Fliter applied: {filters[filter_choice]['name']}")
        elif choice == "2":
            print("Cropping is enabled.")
        elif choice == "3":
            texts = list(texts_collection.find())
            print("Styles you can choose from:")
            for i, text in enumerate(texts):
                print(f"{i + 1}. {text['style']}")
            text_choice = int(input("Please choose your style: ")) - 1
            print(f"Style applied: {texts[text_choice]['style']}")
        elif choice == "4":
            stickers = list(stickers_collection.find())
            print("Emojis you can choose from:")
            for i, sticker in enumerate(stickers):
                print(f"{i + 1}. {sticker['name']}")
            sticker_choice = int(input("Please choose your emoji: ")) - 1
            print(f"Emoji applied: {stickers[sticker_choice]['name']}")
        elif choice == "5":
            colors = list(colors_collection.find())
            print("Colors you can choose from:")
            for i, color in enumerate(colors):
                print(f"{i + 1}. {color['name']}")
            color_choice = int(input("Please choose your color: ")) - 1
            print(f"Color applied: {colors[color_choice]['name']}")
        elif choice == "6":
            print("Done editting.")
            break
        else:
            print("Invalid option, please try again.")

    # 下载和分享
    print("\n1. Download 2. Share")
    action = input("Please choose your option by entering the number:  ")
    if action == "1":
        print("Picture downloaded.")
    elif action == "2":
        print("Picture shared.")

def main():
    while True:
        print("\n=== MENU ===")
        print("1. Upload picture or GIF")
        print("2. Automatically bring up meme")
        print("3. Automatically bring up picture")
        print("4. Exit")
        choice = input("Please choose your option by entering the number: ")

        if choice == "1":
            upload_media()
        elif choice == "2":
            auto_emoji()
        elif choice == "3":
            fetch_image()
        elif choice == "4":
            print("Exit program.")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()