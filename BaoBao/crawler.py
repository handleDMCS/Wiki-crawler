import json
import requests
import argparse
from pymongo import MongoClient
from bs4 import BeautifulSoup

# Khởi tạo đối tượng
parser = argparse.ArgumentParser(description='Crawl data từ Web links')

# Thêm các đối số
parser.add_argument("--links_list", type=str, help="Đường dẫn của file chứa các link web", default=r".\links_list.txt")
parser.add_argument("--save", type=str, help="Đường dẫn lưu dữ liệu", default=r'.\data.json')
# parser.add_argument("--db_name", type=str, required=True, help="Tên cơ sở dữ liệu (MongoDB)")
# parser.add_argument("--user_name", type=str, required=True, help="Tên người dùng")
# parser.add_argument("--pw", type=str, required=True, help="Mật khẩu")
# parser.add_argument("--IP", type=str, required=True, help="Địa chỉ IP của server")
# parser.add_argument("--port", type=str, required=True, help="Cổng PORT")

# Phân tích các đối số
args = parser.parse_args()

# Mongo Database
# Kết nối tới MongoDB
# con = f'mongodf://{args.user_name}:{args.pw}@{args.IP}:{args.port}/{args.db_name}'
con = "mongodb://localhost:27017/"
client = MongoClient(con)

# Chọn database (nếu database chưa tồn tại, nó sẽ được tạo tự động)
db = client['dulieuvanban']

# Chọn collection (nếu collection chưa tồn tại, nó sẽ được tạo tự động)
collection = db['tiengviet']

# URL của trang web bạn muốn crawl
with open(args.links_list, 'r') as file:
    web_list = file.read().splitlines()

def crawler(id, url, list):
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
           
            # Append the new data to the existing list
            list.append(data)
            print("Xong")
        else:
            print(f"Trong web: {url} không có ")
    else:
        print(f'Không thể truy cập trang web: {url}. Mã trạng thái: {web_response.status_code}')

list_data = []
for i, url in enumerate(web_list):
    crawler(i, url,list_data)

# Chèn dữ liệu vào collection
print(len(list_data))
if len(list_data) > 0:
    collection.insert_many(list_data)
    print("Đã thêm xong dữ liệu vào trong database")
else:
    print("Dữ liệu trống")