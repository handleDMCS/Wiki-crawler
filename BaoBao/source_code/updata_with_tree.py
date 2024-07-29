import os
import argparse
from pymongo import MongoClient
from crawler import crawler_web, crawler_pdf, add_error_url
import time
import json
from scan_link import get_link
from tree import TreeNode, print_tree, split_url_to_path, get_url, save_tree_to_mongodb

# start = time.time()


# Khởi tạo đối tượng
parser = argparse.ArgumentParser(description='Crawl data từ Web links')

# Thêm các đối số
# parser.add_argument("--web_links", type=str, default=r'.\web_folder\web_list_7.txt', 
#                     help="Đường dẫn của file chứa các link web")#, 
#                     # default=r".\webs_list.txt")
# parser.add_argument("--pdf_links", type=str, 
#                     help="Đường dẫn của file chứa các link tải PDF")
#                     # default=r'.\pdf_folder\all_pdf_list.txt')
"""
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
                    help="Tên collection", default="test_v1")

# Phân tích các đối số
args = parser.parse_args()

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

# Khoi tao cay
root = TreeNode('Root')

print(args.web_links)
print(args.pdf_links)

list_data = []
links_list = []
pdfs_list = []
dis_list = []
"""

def insert_error(url, error, error_collection):
    item = {
        "URL": url,
        "Error":error
    }
    print(error)
    error_collection.insert_one(item)

def insert_db(data, collection, error_collection):
    try:
        collection.insert_one(data)
        print("Đã thêm xong dữ liệu vào trong database")
    except UnicodeEncodeError as e:
        insert_error(data['URL'], e, error_collection)

'''
if args.web_links != None:
    # URL của trang web bạn muốn crawl
    with open(args.web_links, 'r') as file:
        web_list = file.read().splitlines()

    for url in web_list:
        get_link(url, links_list, pdfs_list, dis_list)

    for url in links_list:
        path_list = split_url_to_path(url)
        root.add_child(path_list)
        crawler_web(url,list_data,dis_list)

if args.pdf_links != None:
    with open(args.pdf_links, 'r') as file:
        pdf_list = file.read().splitlines()

    for url in pdf_list:
        # Từng file 1
        pdf_filename = url.split('/')[-1]
        output_path = os.path.join(output_dir, pdf_filename)
        crawler_pdf(url, list_data, output_path, dis_list)

if args.pdf_links == None and args.web_links == None:
    print(f"Lỗi pdf_links: {args.pdf_links} và web_links: {args.web_links}")
    print("Thoát!!!!")
    exit()

# Chèn dữ liệu vào collection
if len(list_data) > 0:
    for item in list_data:
        try:
            collection.insert_one(item)
        except UnicodeEncodeError as e:
            # print(item)
            url = item['URL']
            data = {
                "URL": url,
                "Error":f"Lỗi khi tải xuống {e}"
            }
            dis_list.append(data)
            # list_data = [item for item in list_data if item["URL"] != url]
            print(f"Lỗi khi tải xuống: {url} - {e}")
        print("Đã thêm xong dữ liệu vào trong database")
else:
    print("Dữ liệu trống")

# add_error_url(dis_list)
end = time.time()
print(f"Time loss: {end - start}s")

tree_dict = root.to_dict()
with open('tree_structure.json', 'w') as json_file:
    json.dump(tree_dict, json_file, indent=4)

print("Cấu trúc cây:")
root.print_tree()

save_tree_to_mongodb(root, db)
print("Đã lưu cây vào MongoDB!")
'''