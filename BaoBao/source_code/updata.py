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