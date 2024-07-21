# Mảng dữ liệu với các từ điển
data = [
    {
        "URL": "http://example.com/page1",
        "Title": "Page 1",
        "Content": "This is the content of page 1."
    },
    {
        "URL": "http://example.com/page2",
        "Title": "Page 2",
        "Content": "This is the content of page 2."
    },
    {
        "URL": "http://example.com/page3",
        "Title": "Page 3",
        "Content": "This is the content of page 3."
    }
]

# In mảng trước khi xóa
print("Mảng trước khi xóa phần tử:", data)


# URL của phần tử cần xóa
url_to_remove = "http://example.com/page2"

data = [item for item in data if item["URL"] != url_to_remove]

# In mảng sau khi xóa
print("Mảng sau khi xóa phần tử:", data)

# Đường dẫn tới file JSON
json_file_path = "output.json"

# Ghi dữ liệu vào file JSON
import json
with open(json_file_path, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f"Dữ liệu đã được lưu vào file {json_file_path}")
