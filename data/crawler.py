import json
import requests

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