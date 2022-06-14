import requests
import re
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}

base_url = "https://www.mcbbs.net/"

r = requests.get("https://www.mcbbs.net/forum-news-1.html", headers=headers)
bs = BeautifulSoup(r.text, "html.parser")
list = bs.findAll("tbody", id=re.compile("normalthread_*"))

for i in list:
    thread_id = re.compile(r"\d+").search(i["id"]).group()
    type = i.tr.th.em.text
    title = i.tr.th.find("a", class_="s xst").text
    url = base_url + i.tr.th.find("a", class_="s xst")["href"]
    print(thread_id + "> " + type + " " + title + "\n" + url)
