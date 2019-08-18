#! /usr/bin/python

import io
import sys
import requests

from bs4 import BeautifulSoup

url = "http://www.createdebate.com/browse/debates"
num_pages = 696
offset =0
browse_perpage = 96

def get_debates_list(response):
    soup = BeautifulSoup(response.text, "html.parser")
    ans = []
    debate_list=soup.find("div", style = "border-bottom:1px solid #E0E0E0;")
    soup = BeautifulSoup(str(debate_list), "html.parser")
    debates = soup.find_all("div", style = "clear:left;")
    for i in debates:
        soup2 = BeautifulSoup(str(i),"html.parser")
        title = soup2.find("div", style = "float:left;width:280px;padding-left:10px;")
        if (title is None):
            continue
        link = soup2.find("a")
        if (link is None):
            continue
        link ="http:{}".format(link["href"])
        ans.append((title.text,link))
    return ans

def get_all_debates():
    offset = 0
    with io.open("debates_info.txt", "w+", encoding='utf-8') as f:
        f.write("\t".join(["Debate_Topic", "Debate_URL"]))
        f.write("\n")
        f.flush()
        for i in range(num_pages):
            data = {
            "browse_who":"all",
            "browse_action":"mostheated",
            "browse_type":"alltypes",
            "browse_time":"alltime",
            "browse_category":"alltopics",
            "browse_offset":offset,
            "browse_perpage":browse_perpage,
            "browse_endStatus":"open",
            }
            r = requests.post(url, data = data)
            ans = get_debates_list(r)
            for iter in ans:
                debate_url = iter[1]
                debate_topic = debate_url.split('/')[-1]
                f.write("\t".join([debate_topic, debate_url]))
                f.write("\n")
                f.flush()
            offset += browse_perpage

    return all_debates