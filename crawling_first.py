import requests
from bs4 import BeautifulSoup

url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0105&date=20220305'
html = requests.get(url)
print(html.text)
# print(html.text)
soup = BeautifulSoup(html.text, 'html.parser')
title_list = soup.select('div.info-movie > a > strong')
for i in title_list:
    print(i.text.strip())