import re
import requests
import time
import export
from bs4 import BeautifulSoup

### START -- an exception(First page) -- ###
# decleare
idlist_new = set()
idlist = set()
target = "https://freelance.levtech.jp/project/search/?pref%5B0%5D=13&district%5B0%5D=1&district%5B1%5D=2&district%5B2%5D=3&area%5B0%5D=1&area%5B1%5D=2&area%5B2%5D=3&area%5B3%5D=4&area%5B4%5D=5&area%5B5%5D=6&area%5B6%5D=7&area%5B7%5D=8&area%5B8%5D=9&area%5B9%5D=10&area%5B10%5D=11&area%5B11%5D=12&area%5B12%5D=13&area%5B13%5D=14&area%5B14%5D=15&area%5B15%5D=16&sala=7"

#idlist, idlist_new = common_process.make_urllist(target)

# bs4 analyze
r = requests.get(target)
soup = BeautifulSoup(r.content, "html.parser")

# Overall column
li_all = soup.find_all("li",class_="prjList__item js-link")

# new-tag distribution
for li in li_all: 
    detail_link = li.find("a",class_ = "js-link_rel")
    if li.find("p",class_ = "prjLabel__txt"):
        idlist_new.add(detail_link.get("href"))
    else:
        idlist.add(detail_link.get("href"))

### END -- an exception(First page) -- ###

#get lastpage number
last = soup.find("a",rel="last")
last_url = last.get('href')
regex = re.compile('\d+')

for line in last_url.splitlines():
  match = regex.findall(line)
lastnum = int(match[0]) + 1

# #make detail list//lastnumに書き換え
for num in range(2,lastnum):
    time.sleep(1)

    target = "https://freelance.levtech.jp/project/search/p" + str(num) + "/?pref%5B0%5D=13&district%5B0%5D=1&district%5B1%5D=2&district%5B2%5D=3&area%5B0%5D=1&area%5B1%5D=2&area%5B2%5D=3&area%5B3%5D=4&area%5B4%5D=5&area%5B5%5D=6&area%5B6%5D=7&area%5B7%5D=8&area%5B8%5D=9&area%5B9%5D=10&area%5B10%5D=11&area%5B11%5D=12&area%5B12%5D=13&area%5B13%5D=14&area%5B14%5D=15&area%5B15%5D=16&sala=7"
    r = requests.get(target)
    soup = BeautifulSoup(r.content, "html.parser")

    # Overall column
    li_all = soup.find_all("li",class_="prjList__item js-link")

    # new-tag distribution
    for li in li_all:
        if not "募集終了" in li.text:
            detail_link = li.find("a",class_ = "js-link_rel")
            if li.find("p",class_ = "prjLabel__txt"):
                idlist_new.add(detail_link.get("href"))
            else:
                idlist.add(detail_link.get("href"))

export.export_csv(idlist_new,"new")
export.export_csv(idlist,"normal")