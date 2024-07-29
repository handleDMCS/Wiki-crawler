import requests
from bs4 import BeautifulSoup
import os
import time
from updata import insert_error
from crawler import crawler_web, crawler_pdf
from tree import split_url_to_path

OUTPUT_DIR = "downloaded_pdfs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Hàm để kiểm tra và lưu link vào file txt
def save_link_to_file(link, check, file_path=r'./link_folder/links.txt'):
    # Kiểm tra xem file có tồn tại không
    if not os.path.exists(file_path):
        print(f"Lỗi file {file_path} không tồn tại!!")

    # Đọc nội dung file và kiểm tra xem link đã tồn tại chưa
    with open(file_path, 'r') as file:
        links = file.readlines()
        links = [l.strip() for l in links] 

    if link not in links:
        # Ghi link mới vào file
        with open(file_path, 'a') as file:
            file.write(link + '\n')
        print(f"Link '{link}' đã được thêm vào file.")
        check = 0
    else: 
        check +=1
    
    return check

def check_link(link):
    """
    Kiểm tra các từ khoá có thế gây lỗi hoặc không cần thiết.
    """
    forbidden_keywords = ['b.link', "youtu", "ebook", "javascript", "buymeacoffee", "email", "#"]
    return not any(keyword in link for keyword in forbidden_keywords)

def add_tree(root, url):
    path_list = split_url_to_path(url)
    root.add_child(path_list)

def get_link(url, check, root, collection, error_collection):
    try:
       # Gửi một yêu cầu GET đến trang web
        response = requests.get(url)

        # Kiểm tra nếu yêu cầu thành công
        if response.status_code == 200:
            # Phân tích nội dung của yêu cầu với BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Tìm tất cả các thẻ anchor (a)
            links = soup.find_all('a')
            crawler_web(url, collection, error_collection)
            # Trích xuất các thuộc tính href từ các thẻ anchor
            for link in links:
                href = link.get('href')
                if not isinstance(href, str):
                    continue
                if href and check_link(href):
                    if not href.startswith("http"):
                        href = url + href.lstrip('/')
                    if url not in href: 
                        temp = split_url_to_path(href)
                        if len(temp) > 4:
                            temp = temp[:4]
                            href_new = ''
                            for i in range(len(temp)):
                                if i == len(temp)-1:
                                    href_new += temp[i]
                                else:
                                    href_new += temp[i]+'/'
                        href = href_new
                    check = save_link_to_file(href, check)
                    if check < 1:
                        add_tree(root, href)
                        get_link(href, check, root, collection, error_collection)    

                    if '.pdf' in href:
                        pdf_filename = url.split('/')[-1]
                        output_path = os.path.join(OUTPUT_DIR, pdf_filename)
                        crawler_pdf(href, output_path, collection, error_collection)
                    else:
                        crawler_web(href, collection, error_collection)
            print(f"Truy xuất xong trang web: {url}")
        else:
            insert_error(url, f"Mã trạng thái: {response.status_code}", error_collection)
    except requests.exceptions.ConnectionError as e:
        insert_error(url, f"Không thể kết nối: {e}", error_collection)
    except UnicodeEncodeError as e:
        insert_error(url,  f"Lỗi mã hóa Unicode: {e}", error_collection)
    except requests.exceptions.TooManyRedirects as e:
        insert_error(url, f"Lỗi TooManyRedirects: {e}", error_collection)
    except requests.exceptions.ChunkedEncodingError as e:
        insert_error(url, f"Lỗi ChunkedEncodingError: {e}", error_collection)
    except requests.exceptions.ReadTimeout as e:
        insert_error(url, f"Lỗi ReadTimeout: {e}", error_collection)
    except requests.exceptions.InvalidURL as e:
        insert_error(url, f"Lỗi InvalidURL: {e}", error_collection)
    except Exception as e:
        insert_error(url, f"Lỗi khác: {e}", error_collection)

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Thời gian chạy của {func.__name__} là: {elapsed_time:.6f} giây")
        return result
    return wrapper