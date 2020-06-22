import re
import requests
from bs4 import BeautifulSoup

idlist_new = set()
idlist = set()

def make_urllist(target):
  
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
 
    return idlist,idlist_new
