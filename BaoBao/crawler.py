import json
import requests
from bs4 import BeautifulSoup


# Định nghĩa URL của trang web cần scrape
url = 'https://machinelearningcoban.com/page2/'

# Gửi yêu cầu GET đến trang web
response = requests.get(url)

# Kiểm tra nếu yêu cầu thành công
if response.status_code == 200:
    # Phân tích nội dung HTML của trang
    soup = BeautifulSoup(response.content, 'html.parser')

    # Trích xuất dữ liệu (ví dụ: tất cả các đoạn văn bản)
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        print(p.get_text())
else:
    print(f'Không thể truy cập trang. Mã trạng thái: {response.status_code}')
