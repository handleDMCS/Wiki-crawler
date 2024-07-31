import requests
from bs4 import BeautifulSoup
import pdfplumber
import os
import time
from updata import insert_db, insert_error

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
def crawler_web(url, collection, error_collection):
    try:
        # Gửi yêu cầu GET đến trang web
        web_response = requests.get(url)

        # Kiểm tra nếu yêu cầu thành công
        if web_response.status_code == 200:
            print(f"Tiến hành truy xuất trang web: {url}")

            # Phân tích nội dung HTML của trang
            soup = BeautifulSoup(web_response.content, 'html.parser')

            # Trích xuất dữ liệu (ví dụ: tất cả các đoạn văn bản)
            paragraphs = soup.find_all('p')
            if paragraphs:
                data = {
                    "URL": url,
                    "Title": soup.title.string if soup.title else "",
                    "Content": "\n".join(p.get_text() for p in paragraphs),
                }
                insert_db(data, collection, error_collection)
                print("Xong")
            else:
                print(f"Trong web: {url} không có dữ liệu cần dùng!!!")
        else:
            insert_error(url, f"Status: {web_response.status_code}", error_collection)
            print(f'Không thể truy cập trang web: {url}. Mã trạng thái: {web_response.status_code}')

    except requests.exceptions.ConnectionError as e:
        insert_error(url, f"Không thể kết nối: {e}", error_collection)
    except UnicodeEncodeError as e:
        insert_error(url,  f"Lỗi mã hóa Unicode: {e}", error_collection)
    except requests.exceptions.TooManyRedirects as e:
        insert_error(url, f"Lỗi TooManyRedirects: {e}", error_collection)
    except requests.exceptions.ChunkedEncodingError as e:
        insert_error(url,  f"Lỗi ChunkedEncodingError: {e}", error_collection)
    except requests.exceptions.ReadTimeout as e:
        insert_error(url, f"Lỗi ReadTimeout: {e}", error_collection)
    except requests.exceptions.InvalidURL as e:
        insert_error(url, f"Lỗi InvalidURL: {e}", error_collection)
    except Exception as e:
        insert_error(url, f"Lỗi khác: {e}", error_collection)

def read_pdf(file_path):
    '''
    Đọc nội dung từ file pdf
    '''
    table = []
    # Open the PDF file
    with pdfplumber.open(file_path) as pdf:
        # Loop through each page and extract text
        for page in pdf.pages:
#             text += page.extract_text() + "\n"
            texts = page.extract_text().split('\n')
            table.append(texts)
    return table

def download_pdf(url, output_path, error_collection):
    '''
    Tải file pdf từ link
    '''
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        # print(output_path)
        with open(output_path, 'wb') as file:
            file.write(response.content)
        print(f"Tải xuống thành công: {output_path}")
    except requests.RequestException as e:
        insert_error(url, f"Lỗi khi tải xuống: {e}", error_collection)
    except OSError as e:
        insert_error(url, f"Lỗi hệ thống: {e}", error_collection)

@timing_decorator
def crawler_pdf(url, output_path, collection, error_collection):
    '''
    Đẩy dữ liệu đã crawl lên trên MongoDB
    '''
    try: 
        # print(output_path)
        download_pdf(url, output_path, error_collection)
        if os.path.isfile(output_path) and output_path.endswith('.pdf'):
            content = read_pdf(output_path)
            for j in content:
                text = " ".join(i for i in j)
            info_pdf = {
                "URL": url,
                "Title": " ".join(i for i in content[0][0:3]),
                "Content_web":text
            }
            insert_db(info_pdf, collection, error_collection)
    except FileNotFoundError as e:
        insert_error(url, f"Lỗi hệ thống: {e}", error_collection)