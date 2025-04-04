from pymongo import MongoClient
from werkzeug.utils import secure_filename
from datetime import datetime
import os 

# Connect to MongoDB

# Local MongoDB connection string (defaulte port 27017)
connection_string_local = "mongodb://localhost:27017/"

# Create MongoDB client instance
client = MongoClient(connection_string_local)

# Access database named "MemeGenSample"
db = client["MemeGenSample"]

# Define collections (similar to tables in relational databases)

# Store users' information
user_collection = db["MemeUser"]

# Store Memes
meme_collection = db["Meme"]


def signup(username, password):
    """
    Register a new user.
    
    Args:
        username (str): username
        password (str): password
        
    Returns:
        ObjectId: The MongoDB _id
        None: If username already exists
    """

    # Check if username already exists
    search_result = user_collection.find_one({"name": username})
    if search_result is None:

        # Create a new Mongo record
        insert_result = user_collection.insert_one({
            "name": username,
            "password": password
        })
        print("New user's id:", insert_result.inserted_id)
        return insert_result.inserted_id
    else:
        print("Username Exist")
        return None


def login(username, password):
    """
    Verify a user.
    
    Args:
        username (str): username
        password (str): password
        
    Returns:
        ObjectId: The MongoDB _id
        None: If verification fails
    """

    # Find user in database
    search_result = user_collection.find_one({"name": username})
    print("!!!!Running login!!!")
    print(search_result)

    # User not found
    if search_result is None:
        return None
    
    # Check passwords
    else:
        if search_result['password'] == password:
            return search_result['_id']
        return None


def upload_meme(username, filename):
    """
    Upload a meme to MongoDB.
    
    Args:
        username (str): username
        filename (str): filename
        
    Returns:
        str: filename in MongoDB
    """

    # Format: username_timestamp_originalfilename
    unique_filename = f"{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{secure_filename(filename)}"
    
    # Create Mongo record in database
    insert_result = meme_collection.insert_one({
        'username': username,
        'filename': unique_filename,
        'upload_time': datetime.now(),
    })
    return unique_filename # Return filename


def get_image_names(username):
    
    """
    Get all memes uploaded by a user.
    
    Args:
        username (str): username
        
    Returns:
        
    """

    # Get all memes
    memes = meme_collection.find({'username': username}).sort('upload_time', -1)
    
    result = []
    
    # Iterate through each meme 
    for meme in memes:
        meme_info = {
            'filename': meme['filename'],
            
            'original_name': meme['filename'].split('_')[-1],
            
            'upload_time': meme['upload_time'].strftime('%Y-%m-%d %H:%M')
        }
        
        result.append(meme_info)
    
    return result