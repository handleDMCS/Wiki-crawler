from scan_link import get_link
import tree
from pymongo import MongoClient
import argparse

parser = argparse.ArgumentParser(description='Crawl data từ Web links')

parser.add_argument("--file_name", type=str, default=r"./web_folder/ml_base.txt", 
                    help="Tên file ")
parser.add_argument("--db_name", type=str, default="dulieutiengviet", 
                    help="Tên cơ sở dữ liệu (MongoDB)")
parser.add_argument("--user_name", type=str, 
                    default="dulieutiengviet", help="Tên người dùng")
parser.add_argument("--pw", type=str, 
                    default="1231231234", help="Mật khẩu")
parser.add_argument("--IP", type=str, 
                    default='116.101.70.243', help="Địa chỉ IP của server")
parser.add_argument("--port", type=str, 
                    default=27017, help="Cổng PORT")
parser.add_argument("--collect", type=str,
                    help="Tên collection", default="tiengviet")

args = parser.parse_args()
with open(args.file_name, 'r') as file:
    urls = file.readlines()
    urls = [item.strip() for item in urls] 

# Mongo Database
# Kết nối tới MongoDB
con = f'mongodb://{args.user_name}:{args.pw}@{args.IP}:{args.port}/{args.db_name}'
# con = "mongodb://localhost:27017/"
client = MongoClient(con)

# Chọn database (nếu database chưa tồn tại, nó sẽ được tạo tự động)
db = client[args.db_name]

# Chọn collection (nếu collection chưa tồn tại, nó sẽ được tạo tự động)
collection = db[args.collect] # Lưu dữ liệu chính
error_collection = db['Error URL'] # Lưu các đường dẫn bị lỗi
collection_tree = db["Tree URL"]

# Khoi tao cay
root = tree.TreeNode('Root')
check = 0
for url in urls:
    get_link(url=url,urls=urls,
             check=check,root=root,
             collection=collection,
             error_collection=error_collection,
             collection_tree=collection_tree)