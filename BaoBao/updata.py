import os
import argparse
from pymongo import MongoClient
from crawler import crawler_web, crawler_pdf

output_dir = "downloaded_pdfs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Khởi tạo đối tượng
parser = argparse.ArgumentParser(description='Crawl data từ Web links')

# Thêm các đối số
parser.add_argument("--web_links", type=str, help="Đường dẫn của file chứa các link web", default=r".\webs_list.txt")
parser.add_argument("--pdf_links", type=str, help="Đường dẫn của file chứa các link tải PDF", default=r'.\pdf_list.txt')
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
with open(args.web_links, 'r') as file:
    web_list = file.read().splitlines()

with open(args.pdf_links, 'r') as file:
    pdf_list = file.read().splitlines()

list_data = []
# for i, url in enumerate(web_list):
#     crawler_web(i, url,list_data)

crawler_pdf(pdf_list, list_data, output_dir)

# Chèn dữ liệu vào collection
if len(list_data) > 0:
    collection.insert_many(list_data)
    print("Đã thêm xong dữ liệu vào trong database")
else:
    print("Dữ liệu trống")
