import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument('--headless')  # 브라우저 창을 표시하지 않음
chrome_service = Service('/usr/local/bin/chromedriver')

# Crawling 시작
def start_crawling(base_url: str):
        robots_url = urljoin(base_url, '/robots.txt')
        allow_paths, disallowed_paths = check_robots(robots_url)

        crawling_paths = check_crawling(base_url, allow_paths, disallowed_paths)

        for path in crawling_paths:
                a_list = crawling_page(path)
                for a_href in a_list:
                        start_crawling(a_href)
        
# robots.txt를 확인하여, allow, disallow를 확인한다.
def check_robots(robots_url: str):
        response = requests.get(robots_url)
        if response.status_code == 200:
                robots_txt = response.text
                # 줄 단위로 읽어 'Allow' 규칙을 찾기
                allowed_paths = [line.split(': ')[1] for line in robots_txt.splitlines() if line.startswith('Allow')]
                disallowed_paths = [line.split(': ')[1] for line in robots_txt.splitlines() if line.startswith('Disallow')]
                return allowed_paths, disallowed_paths
        else:
                return [], []

# allow와 disallow를 이용하여 허용되는 url list를 만든다.
def check_crawling(url: str, allow_paths: str, disallow_paths: str):
        url_list = []
        
        if not '/' in disallow_paths:
                url_list.append(url)
        
        for path in allow_paths:
                url_list.append(urljoin(url, path))

        return url_list

# a tag만 가져오는 크롤링
def crawling_page(url: str):
        a_list = []

        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        driver.get(url)
    

        time.sleep(10)

        page_source = driver.page_source

        obj = {
                "main": [],
                "sub": [],
                "etc": [],
        }

        soup = BeautifulSoup(page_source, 'html.parser')    

        title = soup.title.string if soup.title else 'No Title'

        for a_tag in soup.find_all('a'):
                a_list.append(a_tag.get('href'))
                print('Text:', a_tag.get_text())
        for h1_tag in soup.find_all('h1'):
                obj["main"].append(h1_tag.get_text())
        for h2_tag in soup.find_all('h2'):
                obj["sub"].append(h2_tag.get_text())
        for h3_tag in soup.find_all('h3'):
                obj["etc"].append(h3_tag.get_text())

        # filename = get_unique_filename(title)
        # with open(filename, 'w', encoding='utf-8') as json_file:
        #         json.dump(obj, json_file, ensure_ascii=False, indent=4)

        return a_list        

def get_unique_filename(title: str) -> str:
    title = sanitize_filename(title)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f'{title}_{timestamp}.json'

def sanitize_filename(title: str) -> str:
    forbidden_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in forbidden_chars:
        title = title.replace(char, '')
    return title

# 크롤링할 페이지의 URL
start_url = 'https://news.ycombinator.com/'
start_crawling(start_url)


