from collections import OrderedDict
import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Thời gian chạy của {func.__name__} là: {elapsed_time:.6f} giây")
        return result
    return wrapper

@timing_decorator
def remove_duplicates(arr):
    return list(OrderedDict.fromkeys(arr))

# Mở tệp TXT
with open(r'D:\Projects\Wiki-crawler\BaoBao\web_folder\all_web_list.txt', 'r', encoding='utf-8') as file:
    web_list_1 = file.read().splitlines()

with open(r'D:\Projects\Wiki-crawler\BaoBao\web_folder\web_list_6.txt', 'r', encoding='utf-8') as file:
    web_list_2 = file.read().splitlines()

print("Các phần tử bị hàm remove_duplicates check trùng:", remove_duplicates(web_list_1 + web_list_2))