from generate_data import generate_data_point
import json

DATA_PER_PAGE = 5
FILE_NAME = 'articles_list.txt'
JSON_FILE_NAME = "progress.json"
LANG = "vi"

def create_dataset(titles_list):
    with open(JSON_FILE_NAME, 'r', encoding='utf-8') as json_file:
        progress = json.load(json_file)
    for (index, title) in enumerate(titles_list):
        fail_cnt = 0
        print(f'\r{progress[title]} / {DATA_PER_PAGE} Fails : {fail_cnt}', end="")
        while(progress[title] < DATA_PER_PAGE):
            try:
                generate_data_point(page_title=title, language=LANG)
                progress[title] += 1
                print(f'\r{progress[title]} / {DATA_PER_PAGE} Fails : {fail_cnt}', end="")
                with open(JSON_FILE_NAME, 'w', encoding='utf-8') as json_file:
                    json.dump(progress, json_file, ensure_ascii=False, indent=4)                
            except Exception as e:
                fail_cnt += 1
                with open("error_log.txt", "w") as file:
                    file.write(f"An error occurred: {e}")
                print(f'\r{progress[title]} / {DATA_PER_PAGE} Fails : {fail_cnt}', end="")
        print(f'\n{index+1}. {title}\n')

with open(FILE_NAME, 'r', encoding='utf-8') as file:
    content = file.read().splitlines()
    create_dataset(titles_list=content)
