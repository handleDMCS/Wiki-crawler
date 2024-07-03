import requests
from bs4 import BeautifulSoup

# URL của trang web bạn muốn crawl
links_list = []

def add_list(list, value):
    if value not in list:
        list.append(value)

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
            if href and href.startswith("http") and ('b.link' not in href) and ("youtu" not in href) and ("facebook" not in href):
                add_list(links_list, href)
            if not href.startswith("http"):
                add_list(links_list, url + href.lstrip('/'))
        print(f"Truy xuất xong trang web: {url}")
    else:
        print(f"Không thể truy xuất trang web: {url}. Mã trạng thái: {response.status_code}")

# URL của trang web bạn muốn crawl
with open('web_list.txt', 'r') as file:
    web_list = file.read().splitlines()

for url in web_list:
    get_link(url, links_list)
    
# Mở file ở chế độ ghi
with open("links_list.txt", "a", encoding="utf-8") as file:
    for item in links_list:
        file.write(f"{item}\n")
