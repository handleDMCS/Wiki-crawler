import json
import requests
from bs4 import BeautifulSoup

# URL của trang web bạn muốn crawl
with open('links_list.txt', 'r') as file:
    web_list = file.read().splitlines()

def crawler(id,url):
    # Gửi yêu cầu GET đến trang web
    web_response = requests.get(url)

    # Kiểm tra nếu yêu cầu thành công
    if web_response.status_code == 200:
        print(f"Tiến hành truy xuất trang web: {url}")

        # Phân tích nội dung HTML của trang
        soup = BeautifulSoup(web_response.content, 'html.parser')

        # Trích xuất dữ liệu (ví dụ: tất cả các đoạn văn bản)
        paragraphs = soup.find_all('p')
        if (paragraphs):
            data = {
                "ID": id,
                "URL": url,
                "Title": soup.title.string if soup.title else "",
                "Content": "\n".join(p.get_text() for p in paragraphs),
            }
            try:
                with open("data.json", "r", encoding="utf-8") as json_file:
                    existing_data = json.load(json_file)
            except FileNotFoundError:
                existing_data = []

            # Append the new data to the existing list
            existing_data.append(data)

            # Save the updated data back to the JSON file
            with open("data.json", "w", encoding="utf-8") as json_file:
                json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

            print("Xong")
        else:
            print(f"Trong web: {url} không có ")
    else:
        print(f'Không thể truy cập trang web: {url}. Mã trạng thái: {web_response.status_code}')

for i, url in enumerate(web_list):
    crawler(i, url)
