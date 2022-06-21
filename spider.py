import requests
import re
import csv
import configparser
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


def send_msg_tg(text):
    config = configparser.ConfigParser()
    config.read("config.ini")
    if config["tg"].getboolean("send_msg"):
        params = {
            "chat_id": config["tg"]["chat_id"],
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        requests.get(
            "https://api.telegram.org/bot%s/sendMessage" % (config["tg"]["bot_token"]),
            params=params,
        )


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
        for i in data_new:
            send_msg_tg("[#%s] <b>%s</b>\n%s" % (data[i][0], data[i][1], data[i][2]))
            writer.writerow([i] + data[i])

    csvfile.close()


if __name__ == "__main__":
    main()
