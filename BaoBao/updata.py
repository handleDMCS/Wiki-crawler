from pymongo import MongoClient

# Kết nối tới MongoDB (thay đổi các thông tin kết nối theo cấu hình của bạn)
client = MongoClient("mongodb://localhost:27017/")

# Chọn database (nếu database chưa tồn tại, nó sẽ được tạo tự động)
db = client['mydatabase']

# Chọn collection (nếu collection chưa tồn tại, nó sẽ được tạo tự động)
collection = db['mycollection']

# Dữ liệu crawl được (có thể là một danh sách các dictionary)
data = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "San Francisco"},
    {"name": "Charlie", "age": 35, "city": "Los Angeles"}
]

# Chèn dữ liệu vào collection
collection.insert_many(data)

print("Dữ liệu đã được chèn vào MongoDB thành công!")
