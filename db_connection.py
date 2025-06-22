from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
# Replace with your MongoDB Atlas connection string

username = os.getenv("MONGO_PWD")
password = os.getenv("MONGO_USER")
def create_connection():
    client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.wsh3nhc.mongodb.net/?retryWrites=true&w=majority&appName=cluster0")
    # Select database and collection
    return client


# Insert data
def insert_data(data,client):
    db = client['train_data']
    collection = db['train_data']
    data['updated_at'] = datetime.now()
    result = collection.insert_one(data)
    print(f"Inserted document ID: {result.inserted_id}")
    return result.inserted_id

def close_connection(client):
    client.close()
    return

def clear_collection(client):
    db = client['train_data']
    collection = db['train_data']
    
    result = collection.delete_many({})
    print(f"Deleted {result.deleted_count} documents from 'train_data' collection.")

def clear_entry(client,date):
    db = client['train_data']
    collection = db['train_data']
    result = collection.delete_many({date: {"$exists": True}})
    return result

def update_progress(client,value):
    db = client['train_data']
    collection = db['progress']
    collection.delete_many({})
    id = collection.insert_one({"progress":value})
    return id

def get_progress(client):
    db = client['train_data']
    collection = db['progress']
    try:
        result = collection.find({"progress": {"$exists": True}})
        for doc in result:
            for key in doc.keys():
                if(key == "progress"):
                    return doc[key]
    except Exception as e:
        raise e
    return "Scraping not running or not found"
