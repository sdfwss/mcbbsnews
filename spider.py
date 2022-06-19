import requests
import re
import csv
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}

base_url = "https://www.mcbbs.net/"

try:
    csvfile = open("data.csv","r",newline='',encoding="utf-8-sig")
except FileNotFoundError:
    csvfile = open("data.csv","w+",newline='',encoding="utf-8-sig")
reader = csv.reader(csvfile)

thread_id_old = [row[0] for row in reader]
data = {}

r = requests.get("https://www.mcbbs.net/forum-news-1.html", headers=headers)
bs = BeautifulSoup(r.text, "html.parser")
list = bs.findAll("tbody", id=re.compile("normalthread_*"))

for i in list:
    thread_id = re.compile(r"\d+").search(i["id"]).group()
    type = i.tr.th.em.text.strip("[]")
    title = i.tr.th.find("a", class_="s xst").text
    url = base_url + i.tr.th.find("a", class_="s xst")["href"]
    #writer.writerow([thread_id,type,title,url])
    #print(thread_id + "> " + type + " " + title + "\n" + url)
    data[thread_id]=[type,title,url]

data_new = []
for key in data.keys():
    if key in thread_id_old: break
    data_new.append(key)

if data_new != []:
    csvfile = open("data.csv","a",newline='',encoding="utf-8-sig")
    writer = csv.writer(csvfile)
    data_new.reverse() 
    for i in data_new:
        writer.writerow([i,data[i]])

csvfile.close()