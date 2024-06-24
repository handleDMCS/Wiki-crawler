import json
import requests
from pymongo import MongoClient

def get_wikipedia_page_content(page_title, language="en"):
    url = f"https://{language}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "revisions",
        "titles": page_title,
        "rvslots": "main",
        "rvprop": "content",
        "format": "json"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    return data

def insert_data(data):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:2717/')
    
    # Select the database
    db = client['mydatabase']
    
    # Select the collection
    collection = db['mycollection']
    
    # Insert data into the collection
    result = collection.insert_one(data)
    
    print(f'Data inserted with id: {result.inserted_id}')

# Page title for the Vietnamese Wikipedia page

# if content:
#     insert_data(content)
# else:
#     print("No content found for the specified page.")