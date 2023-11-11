import requests
import re
import csv
import configparser
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}
base_url = "https://www.mcbbs.net/"


def get_data():
    data = {}
    r = requests.get(base_url + "forum-news-1.html", headers=headers)
    bs = BeautifulSoup(r.text, "html.parser")
    list = bs.findAll("tbody", id=re.compile("normalthread_*"))

    for i in list:
        thread_id = re.compile(r"\d+").search(i["id"]).group()
        type = i.tr.th.em.text.strip("[]")
        title = i.tr.th.find("a", class_="s xst").text
        url = base_url + i.tr.th.find("a", class_="s xst")["href"]
        data[thread_id] = [type, title, url]
    return data

def sc_send(api_url, text, desp='', key='[SENDKEY]'):
    postdata = urllib.parse.urlencode({'text': text, 'desp': desp}).encode('utf-8')
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    request = urllib.request.Request(api_url + key + '.send', data=postdata, headers=headers)
    response = urllib.request.urlopen(request)
    result = response.read().decode('utf-8')
    return result


def main():
    try:
        csvfile = open("data.csv", "r+", newline="", encoding="utf-8")
    except FileNotFoundError:
        csvfile = open("data.csv", "w+", newline="", encoding="utf-8")
    reader = csv.reader(csvfile)

    thread_id_old = [row[0] for row in reader]
    data = get_data()
    data_new = []

    for thread_id in data.keys():
        if thread_id in thread_id_old:
            break
        data_new.append(thread_id)

    if data_new != []:
        writer = csv.writer(csvfile)
        data_new.reverse()
        tmp=""
        for i in data_new:
            tmp+="**%s** [%s](%s)  \n" % (data[i][0], data[i][1], data[i][2])
            writer.writerow([i] + data[i])
        config = configparser.ConfigParser()
        config.read("config.ini")
        api_url = config["sct"]["api_url"]
        print(config["sct"].getboolean("send_msg"))
        if config["sct"].getboolean("send_msg"):
            print(sc_send(api_url,"MCBBS幻翼块讯",tmp,config["sct"]["sendkey"]))
    csvfile.close()


if __name__ == "__main__":
    main()
