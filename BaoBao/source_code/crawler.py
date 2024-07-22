import requests
from bs4 import BeautifulSoup
import pdfplumber
import os
import json

def add_error_url(dis_list):
    # Đường dẫn đến file JSON
    file_path = './error_url_list.json'

    if os.path.exists(file_path):
        # Nếu file JSON tồn tại, đọc nội dung và thêm các phần tử mới vào
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            # Kiểm tra xem data có phải là một list không
            if isinstance(data, list):
                data.extend(dis_list)
            else:
                print("Nội dung file JSON không phải là một list. Không thể thêm các phần tử mới.")
            
            # Ghi lại nội dung cập nhật vào file JSON
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            print("Đã thêm các phần tử mới vào file JSON.")
        except json.JSONDecodeError:
            print("File JSON không hợp lệ.")
    else:
        # Nếu file JSON không tồn tại, tạo mới và lưu danh sách hiện tại vào
        with open(file_path, 'w') as f:
            json.dump(dis_list, f, indent=4)
        print("Đã tạo file mới và lưu danh sách hiện tại vào.")

def crawler_web(url, list, dis_list):
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

                # Append the new data to the existing list
                list.append(data)
                print("Xong")
            else:
                print(f"Trong web: {url} không có dữ liệu cần dùng!!!")
        else:
            data = {
                "url":url,
                "Error": f"Status: {web_response.status_code}"
                }
            dis_list.append(data)
            print(f'Không thể truy cập trang web: {url}. Mã trạng thái: {web_response.status_code}')

    except requests.exceptions.ConnectionError:
        data = {
            "url":url,
            "Error": f"Không thể kết nối!"
            }
        dis_list.append(data)
        print(f'Không thể kết nối đến trang web: {url}')
    except UnicodeEncodeError as e:
        data = {
            "url":url,
            "Error": f"Lỗi mã hóa Unicode: {e}"
            }
        dis_list.append(data)
        print(f'Lỗi mã hóa Unicode: {e}')
    except requests.exceptions.TooManyRedirects as e:
        data = {
            "url":url,
            "Error": f"Lỗi TooManyRedirects: {e}"
            }
        dis_list.append(data)
        print(f'Lỗi TooManyRedirects: {e}')
    except requests.exceptions.ChunkedEncodingError as e:
        data = {
            "url":url,
            "Error": f"Lỗi ChunkedEncodingError: {e}"
            }
        dis_list.append(data)
        print(f'Lỗi ChunkedEncodingError: {e}')

def read_pdf(file_path):
    table = []
    # Open the PDF file
    with pdfplumber.open(file_path) as pdf:
        # Loop through each page and extract text
        for page in pdf.pages:
#             text += page.extract_text() + "\n"
            texts = page.extract_text().split('\n')
            table.append(texts)
    return table

def download_pdf(url, output_path, dis_list):
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        print(output_path)
        with open(output_path, 'wb') as file:
            file.write(response.content)
        print(f"Tải xuống thành công: {output_path}")
    except requests.RequestException as e:
        data = {
            "url":url,
            "Error": f"Lỗi khi tải xuống: {e}"
            }
        dis_list.append(data)
        print(f"Lỗi khi tải xuống: {url} - {e}")

def crawler_pdf(links_list, list_pdf, output_dir, dis_list):
    for url in links_list:
        pdf_filename = url.split('/')[-1]
        output_path = os.path.join(output_dir, pdf_filename)
        print(output_path)
        download_pdf(url, output_path, dis_list)
        try:
            content = read_pdf(output_path)
        except FileNotFoundError:
            continue
        for j in content:
            text = " ".join(i for i in j)
        info_pdf = {
            "URL_web": url,
            "Title": " ".join(i for i in content[0][0:3]),
            "Content_web":text
        }
        list_pdf.append(info_pdf)