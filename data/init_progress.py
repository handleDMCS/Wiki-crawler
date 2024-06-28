import json

JSON_FILE_NAME = 'progress.json'
FILE_NAME = 'articles_list.txt'

with open(FILE_NAME, 'r', encoding='utf-8') as file:
    titles = file.read().splitlines()
    json_dict = {title: 0 for title in titles}

with open(JSON_FILE_NAME, 'w', encoding='utf-8') as json_file:
    json.dump(json_dict, json_file, ensure_ascii=False, indent=4)