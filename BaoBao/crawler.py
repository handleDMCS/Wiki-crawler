import requests
from bs4 import BeautifulSoup
import pdfplumber
import os

def crawler_web(id, url, list):
    # Gửi yêu cầu GET đến trang web
    web_response = requests.get(url)

    # Kiểm tra nếu yêu cầu thành công
    if web_response.status_code == 200:
        print(f"Tiến hành truy xuất trang web: {url}")

        # Phân tích nội dung HTML của trang
        soup = BeautifulSoup(web_response.content, 'html.parser')

        # Trích xuất dữ liệu (ví dụ: tất cả các đoạn văn bản)
        paragraphs = soup.find_all('p')
        if (paragraphs):
            data = {
                "ID": id,
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
        print(f'Không thể truy cập trang web: {url}. Mã trạng thái: {web_response.status_code}')

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

def download_pdf(url, output_path):
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        with open(output_path, 'wb') as file:
            file.write(response.content)
        print(f"Tải xuống thành công: {output_path}")
    except requests.RequestException as e:
        print(f"Lỗi khi tải xuống: {url} - {e}")

def crawler_pdf(links_list, list_pdf, output_dir):
    for i, url in enumerate(links_list):
        pdf_filename = url.split('/')[-1]
        output_path = os.path.join(output_dir, pdf_filename)
        print(output_path)
        download_pdf(url, output_path)
        try:
            content = read_pdf(output_path)
        except FileNotFoundError:
            continue
        for j in content:
            text = " ".join(i for i in j)
        info_pdf = {
            "ID": i,
            "URL_web": url,
            "Title": " ".join(i for i in content[0][0:3]),
            "Content_web":text
        }
        list_pdf.append(info_pdf)