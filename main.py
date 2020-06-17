import re
import requests
from bs4 import BeautifulSoup

# decleare
list = set()
target = "https://freelance.levtech.jp/project/search/?pref%5B0%5D=13&district%5B0%5D=1&district%5B1%5D=2&district%5B2%5D=3&area%5B0%5D=1&area%5B1%5D=2&area%5B2%5D=3&area%5B3%5D=4&area%5B4%5D=5&area%5B5%5D=6&area%5B6%5D=7&area%5B7%5D=8&area%5B8%5D=9&area%5B9%5D=10&area%5B10%5D=11&area%5B11%5D=12&area%5B12%5D=13&area%5B13%5D=14&area%5B14%5D=15&area%5B15%5D=16&sala=7"

# bs4 analyze
r = requests.get(target)
soup = BeautifulSoup(r.content, "html.parser")

#get lastpage number
last = soup.find("a",rel="last")
last_url = last.get('href')
regex = re.compile('\d+')

for line in last_url.splitlines():
  match = regex.findall(line)
lastnum = int(match[0]) + 1

#make detail list
for num in range(2,lastnum):
    print(num)