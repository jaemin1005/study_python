import requests
from bs4 import BeautifulSoup

# 크롤링할 페이지의 URL
url = 'https://news.ycombinator.com/'  # 이 URL은 예시입니다. 실제 페이지 URL로 변경하세요.

# 페이지 요청
response = requests.get(url)
response.raise_for_status()

# HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 모든 <a> 태그를 찾고, 텍스트를 가져오기
for a_tag in soup.find_all('a'):
        print('Text:', a_tag.get_text())
        print('URL:', a_tag.get('href'))