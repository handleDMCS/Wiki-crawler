import requests
import argparse
from bs4 import BeautifulSoup

# Khởi tạo đối tượng
parser = argparse.ArgumentParser(description='Crawl data từ Web links')

# Thêm các đối số
parser.add_argument("--web_list", type=str, help="Đường dẫn của file chứa các link web trang chủ", default=r".\web_list.txt")
parser.add_argument("--save", type=str, help="Đường dẫn lưu các link đã scan được link", default=r'.\webs_list.txt')

# Phân tích các đối số
args = parser.parse_args()


# URL của trang web bạn muốn crawl
links_list = []

def add_list(list, value):
    if value not in list:
        list.append(value)

def check_link(link):
    """
    Kiểm tra các từ khoá có thế gây lỗi hoặc không cần thiết.
    """
    forbidden_keywords = ['b.link', "youtu", "ebook", "javascript", "buymeacoffee", "email"]
    return not any(keyword in link for keyword in forbidden_keywords)

def get_link(url, links_list):
    # Gửi một yêu cầu GET đến trang web
    response = requests.get(url)

    # Kiểm tra nếu yêu cầu thành công
    if response.status_code == 200:
        # Phân tích nội dung của yêu cầu với BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Tìm tất cả các thẻ anchor (a)
        links = soup.find_all('a')

        # Trích xuất các thuộc tính href từ các thẻ anchor
        for link in links:
            href = link.get('href')
            if not isinstance(href, str) or href == url:
                continue
            if href and check_link(href):
                if href.startswith("http"):
                    if (url in href):
                        add_list(links_list, href)
                else:
                    add_list(links_list, url + href.lstrip('/'))
        print(f"Truy xuất xong trang web: {url}")
    else:
        print(f"Không thể truy xuất trang web: {url}. Mã trạng thái: {response.status_code}")

# URL của trang web bạn muốn crawl
with open(args.web_list, 'r') as file:
    web_list = file.read().splitlines()

for url in web_list:
    get_link(url, links_list)
    
# Mở file ở chế độ ghi
with open(args.save, "a", encoding="utf-8") as file:
    for item in links_list:
        file.write(f"{item}\n")
